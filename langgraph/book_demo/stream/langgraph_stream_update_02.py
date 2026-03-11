
from typing import TypedDict

from langgraph.graph import StateGraph,START,END


class StreamState(TypedDict):
    desc:str
    common:str

def first_update_node(state:StreamState):
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

#仅传输每个节点对状态所做的特定更新
for chunk in app.stream({"desc": "desc1", "common": "common1"}, stream_mode="updates"):
    print(chunk)

#输出
# {'first': {'desc': 'desc1 first_update_node '}}
# {'second': None}
# {'third': None}
# {'common': {'common': 'common1 common_update_node '}}