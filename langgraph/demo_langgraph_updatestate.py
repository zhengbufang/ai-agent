
from langchain_core.messages import HumanMessage, AnyMessage
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph, MessagesState, add_messages
from typing_extensions import TypedDict
from typing import (
    Annotated,
    Any,
    Literal,
    cast,
    Dict
)

class UpdateState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    pass_node:list[str]


def start_node(state:UpdateState):
    print("start_node:",state.get("pass_node", []))
    new_state = state.copy()
    new_state.get("pass_node", []).append("start_node")
    return new_state

def plan_node(state:UpdateState):
    print("plan_node:",state.get("pass_node", []))

    new_state = state.copy()
    new_state.get("pass_node", []).append("plan_node")
    return new_state

def end_node(state:UpdateState):
    print("end_node:",state.get("pass_node", []))
    new_state = state.copy()
    new_state.get("pass_node", []).append("end_node")
    return new_state

def weather_node(state:UpdateState,config:RunnableConfig):
    print("weather_node:", state.get("pass_node", []))
    new_state = state.copy()
    new_state.get("pass_node", []).append("weather_node")
    return new_state

def rag_node(state:UpdateState):
    print("這裏正在調用向量數據庫")
    print("檢索到的答案是：哈哈哈哈")
    new_state = state.copy()
    new_state.get("pass_node", []).append("rag_node")
    return new_state

def plan_route(state:UpdateState,config:RunnableConfig):
    question = config.get("configurable",{}).get("question",None)
    if "天氣" in question:
        return "weather"
    elif "疫苗" in question:
        return "rag"
    return END

graph = StateGraph(UpdateState)
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
    # "pass_node":[] 需要初始化
    response = app.invoke({"messages": [HumanMessage(content="北京天气如何")],"pass_node":[]},
                         config={"configurable": {"thread_id": 42,"question":"北京天氣如何","city":"北京"}})
    print(response)
 


