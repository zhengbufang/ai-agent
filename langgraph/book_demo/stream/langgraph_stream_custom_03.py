
from typing import TypedDict

from langgraph.graph import StateGraph,START,END
from langgraph.types import StreamWriter


class StreamState(TypedDict):
    desc:str
    common:str

# 自定义流
def first_update_node(state:StreamState,writer:StreamWriter):
    writer({"custom_key":"自定义的value"})
    return {"desc":state["desc"]+" first_update_node "}

def second_update_node(state:StreamState):
    pass

def third_update_node(state:StreamState):
    pass

def common_update_node(state:StreamState):
    return {"common":state["common"]+" common_update_node "}

graph = StateGraph(StreamState)
graph.add_node("first",first_update_node)
graph.add_node("second",second_update_node)
graph.add_node("third",third_update_node)
graph.add_node("common",common_update_node)

graph.add_edge(START,"first")
graph.add_edge("first","second")
graph.add_edge("second","third")
graph.add_edge("third","common")
graph.add_edge("common",END)
app = graph.compile()

#节点执行过程中随时使用StreamWriter将任意数据发送到流中
for chunk in app.stream({"desc": "desc1", "common": "common1"}, stream_mode="custom"):
    print(chunk)

# 输出 {'custom_key': '自定义的value'}