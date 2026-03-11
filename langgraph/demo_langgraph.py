from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph, MessagesState



def start_node():
    print("開始節點")

def plan_node(state:MessagesState):
    print("plan")

def end_node(state:MessagesState):
    print("plan")

def weather_node(state:MessagesState,config:RunnableConfig):
    city = config.get("configurable",{}).get("city",None)
    print(f"{city}天氣是25攝氏度")

def rag_node(state:MessagesState):
    print("這裏正在調用向量數據庫")
    print("檢索到的答案是：哈哈哈哈")

def plan_route(state:MessagesState,config:RunnableConfig):
    question = config.get("configurable",{}).get("question",None)
    if "天氣" in question:
        return "weather"
    elif "疫苗" in question:
        return "rag"
    return END

graph = StateGraph(MessagesState)
graph.add_node("plan",plan_node)
graph.add_node("weather",weather_node)
graph.add_node("rag",rag_node)

graph.set_entry_point("plan")
graph.add_conditional_edges("plan",plan_route)

#会死循环
#graph.add_edge("weather","plan")
graph.add_edge("weather",END)
graph.add_edge("rag",END)

app = graph.compile(checkpointer=MemorySaver())

if __name__ == "__main__":
    response = app.invoke({"messages": [HumanMessage(content="北京天气如何")]},
                         config={"configurable": {"thread_id": 42,"question":"北京天氣如何","city":"北京"}})
    print(response)



