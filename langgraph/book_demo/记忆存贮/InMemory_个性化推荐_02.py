import json
import uuid

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig
from langchain_core.stores import InMemoryBaseStore
from langgraph.store.base import BaseStore
from langgraph.store.memory import InMemoryStore
from langgraph.graph import MessagesState, StateGraph,START,END

from model import get_model

#内存的短期记忆
memory_story = InMemoryStore()

model = get_model()

recomment_prompt = ChatPromptTemplate.from_messages([
    ("system","你是一个乐于助人的推荐引擎。根据用户资料，提供个性化的产品推荐"),
    ("human","{user_profile_summary}")
])

recomment_chain = recomment_prompt | model | (lambda x:{"messages":[AIMessage(content=x.content)]})

#调用大模型推荐产品
def recomment_products(state:MessagesState,config:RunnableConfig,store:BaseStore):
    """根据用户存贮的偏好向用户推荐产品"""
    user_id = config["configurable"]["user_id"]
    namespace = ("user_info",user_id)
    user_profile_record = store.get(namespace,"profile")
    user_profile = user_profile_record.value if  user_profile_record else {}

    user_profile_summary = format_user_profile_summary(user_profile)

    return recomment_chain.invoke({"user_profile_summary":user_profile_summary})


#格式化记忆中的产品数据
def format_user_profile_summary(user_profile:dict) -> str:
    """将用户资料字典格式化为字符串以进行提示注入"""
    name = user_profile.get("name","用户")
    product = ",".join(user_profile.get("preferred_product_categories",["产品"]))
    return f"用户名{name}。他们偏好的产品类别是：{product}"


def extract_preference_updates(state:MessagesState):
    """从最新的用户消息中提取用户偏好更新"""
    latest_message = state["messages"][-2].content
    extract_prompt = ChatPromptTemplate.from_messages([
    ("system","从用户消息中提取用户的产品类别偏好，以JSON字典形式返回，外层不要包裹'''json''',"
              "键为‘preferred_product_categories',值为类别列表。如果没有表达偏好，则放回一个空字典。"),
    ("human","{user_message}")
    ])

    extract_chain = extract_prompt | model
    preferred_json = extract_chain.invoke({"user_message":latest_message})
    try:
        print("************ 提取的偏好:", preferred_json.content)
        preferences = json.loads(preferred_json.content)
        return preferences
    except Exception  as e:
        print("提取参数错误:",e)
        return {}

def update_user_profile_node(state:MessagesState,config:RunnableConfig,store:BaseStore):
    """在当前会话中触发的记忆存贮中更新用户资料"""
    user_id = config["configurable"]["user_id"]
    namespace = ("user_info", user_id)
    user_profile_record = store.get(namespace, "profile")
    user_profile = user_profile_record.value if user_profile_record else {}
    preferences_update = extract_preference_updates(state)

    update_profile = user_profile.copy() #创建副本以避免修改原始字典

    #合并列表
    if "preferred_product_categories" in preferences_update: #合并或更新偏好
        update_profile["preferred_product_categories"] = (
            list(set(update_profile.get("preferred_product_categories",{})+preferences_update["preferred_product_categories"])))

    #保存更新后的资料
    store.put(namespace,"profile",update_profile)
    return {}


if __name__ == "__main__":
    graph = StateGraph(MessagesState)
    graph.add_node("recommend_products", recomment_products)
    graph.add_node("update_profile", update_user_profile_node)

    graph.add_edge(START, "recommend_products")
    graph.add_edge("recommend_products", "update_profile")
    graph.add_edge("update_profile", END)

    graph_app = graph.compile(store=memory_story)

    user_id = "user_id_1"
    config = {"configurable": {"user_id": user_id}}

    memory_story.put(("user_info", user_id), "profile", {
        "name": "张三", "preferred_product_categories": ["电子产品", "书籍"]})

    result = graph_app.invoke({"messages": [HumanMessage(content="你好")]}, config=config)

    print("初始推荐：")
    print(result["messages"][-1].content)
    print("=" * 50)

    user_message = "我最近对户外装备和运动鞋感兴趣"
    result = graph_app.invoke({"messages": result["messages"] + [HumanMessage(content=user_message)]}, config=config)

    # 检查更新后的用户资料，
    update_profile = memory_story.get(("user_info", user_id), "profile").value

    print("更新后的用户资料：")
    print(json.dumps(update_profile, ensure_ascii=False, indent=2))
    print("=" * 50)

    result = graph_app.invoke({"messages": [HumanMessage(content="我又来了")]}, config=config)
    print("基于更新后资料的推荐：")
    print(result["messages"][-1].content)
