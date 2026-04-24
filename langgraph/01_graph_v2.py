import os

import dotenv
from langchain_core.messages import HumanMessage,AnyMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode
from langgraph.graph import END, StateGraph, MessagesState, add_messages
from model import get_model
from typing_extensions import TypedDict
from typing import (
    Annotated,
    Any,
    Literal,
    cast,
    Dict
)

# 在节点函数返回更新state数据



dotenv.load_dotenv()
os.environ['LANGSMITH_TRACING'] = os.getenv("LANGSMITH_TRACING")
os.environ['LANGSMITH_ENDPOINT'] = os.getenv("LANGSMITH_ENDPOINT")
os.environ['LANGSMITH_API_KEY'] = os.getenv("LANGSMITH_API_KEY")
os.environ['LANGSMITH_PROJECT'] = os.getenv("LANGSMITH_PROJECT")

class MyState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    llm_calls: int

@tool(name_or_callable="search_weather",description="查询天气得工具")
def search_weather(city:str):
    if "上海" in city.lower() or "shanghai" in city.lower():
        return "50度,晴转多云"
    return "-3度,暴雨转小雨"

tools = [search_weather]

#定义工具节点
tool_node = ToolNode(tools)

model = get_model().bind_tools(tools)


#路由边
def route_condition_edge(state:MyState):
    messages = state['messages']

    #获取最后一条消息
    last_message = messages[-1]
    # 如果大模型调用了工具 则转到工具节点
    if last_message.tool_calls:
        return "tools"
    return END

# 定义调用模型的函数
def call_model(state: MyState):
    messages = state['messages']
    new_llm_calls = state.get('llm_calls', 0) + 1
    print("call_model进来了")
    response = model.invoke(messages)
    # 返回列表，因为这将被添加到现有列表中
    return {"messages": [response],"llm_calls": new_llm_calls}

#初始化图
workflow = StateGraph(MyState)
workflow.add_node("agent",call_model)
workflow.add_node("tools",tool_node)


# workflow.set_entry_point("agent")
# workflow.add_conditional_edges("agent",route_condition_edge)
# workflow.add_edge("tools","agent")

#设置入口边
workflow.set_entry_point("agent")
workflow.add_conditional_edges(
    # 首先，定义起始节点。我们使用`agent`。
    # 这意味着这些边是在调用`agent`节点后采取的。
    "agent",
    # 接下来，传递决定下一个调用节点的函数。
    route_condition_edge,
)

# 添加从`tools`到`agent`的普通边。
# 这意味着在调用`tools`后，接下来调用`agent`节点。
workflow.add_edge("tools", 'agent')

# 初始化内存以在图运行之间持久化状态  后续应改为持久化得记忆  比如mongodb redis
checkpointer = MemorySaver()

app = workflow.compile(checkpointer=checkpointer)


def update_state(current_state: MyState, updates: Dict[str, Any]) -> MyState:
    # 创建一个新的状态字典
    new_state = current_state.copy()
    # 更新状态字典中的值
    new_state.update(updates)
    return new_state

if __name__ == "__main__":
    final_state = app.invoke({"messages":[HumanMessage(content="上海天气如何")]},
               config={"configurable": {"thread_id": 42}})

    # 从 final_state 中获取最后一条消息的内容
    result = final_state["messages"][-1].content
    print(result)
    print("============= ",final_state.get("llm_calls"))
    # final_state = app.invoke(
    #     {"messages": [HumanMessage(content="我问的那个城市?")]},
    #     config={"configurable": {"thread_id": 42}}
    # )
    # result = final_state["messages"][-1].content
    # print("============= ", final_state.get("llm_calls"))
    # print(result)




