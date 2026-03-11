
from typing import TypedDict

from langgraph.graph import StateGraph,START,END


class StreamState(TypedDict):
    desc:str
    common:str

def first_update_node(state:StreamState):
    pass
    # return {"desc":state["desc"]+" first_update_node "}

def second_update_node(state:StreamState):
    pass
    # return {"desc":state["desc"]+" second_update_node "}

def third_update_node(state:StreamState):
    return {"desc":state["desc"]+" third_update_node "}

def common_update_node(state:StreamState):
    pass
    # return {"common":state["desc"]+" common_update_node "}

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

#stream_mode="values" 每个节点执行都会返回最新的状态键
#包含所有已定义的的状态变量及当前值的整个状态对象会作为一个完整数据块输出
# 就是某个节点有更新状态键，就会把所有一定义的状态键作为一个完整的数据块在流中执行
for chunk in app.stream({"desc": "desc1", "common": "common1"}, stream_mode="values"):
    print(chunk)

#输出
# {'desc': 'desc1', 'common': 'common1'}
# {'desc': 'desc1 third_update_node ', 'common': 'common1'}
