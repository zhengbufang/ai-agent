
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

#组合流 多种模式同时处理
for chunk,metedata in app.stream({"desc": "desc1", "common": "common1"}, stream_mode=["custom","updates"]):
    print(chunk+" **** "+str(metedata))

# stream_mode="custom" 输出 {'custom_key': '自定义的value'}

# stream_mode=["custom","updates"]  输出
# ('custom', {'custom_key': '自定义的value'})
# ('updates', {'first': {'desc': 'desc1 first_update_node '}})
# ('updates', {'second': None})
# ('updates', {'third': None})
# ('updates', {'common': {'common': 'common1 common_update_node '}})