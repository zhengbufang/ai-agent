from typing import TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph,END
from langgraph.types import interrupt, Command

from langgraph.interrupt import checkpointer


class State(TypedDict):
    name:str
    age:int
    route:int

def start_node(state:State):
    print("起始节点")
    return {"route":1}

#条件控制
def route_node(state:State):
    if state["route"] == 1:
        return "human"
    return "final_node"

#获取人类得输入
def human_node(state:State):
    result = interrupt("请输入您的年龄：")
    return {"name":"模拟从数据库中查出来得","age":int(result)}

def final_node(state:State):
    print("最终节点")

memory = MemorySaver()

builder = StateGraph(State)
builder.add_node("start",start_node)
builder.add_node("human",human_node)
builder.add_node("final",final_node)

builder.set_entry_point("start")
builder.add_conditional_edges("start",route_node)
builder.add_edge("human","final")
builder.add_edge("final",END)

graph = builder.compile(checkpointer=memory)

graph.invoke(input={},config={"configurable":{"thread_id": "1"}})

