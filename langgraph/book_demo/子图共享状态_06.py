from typing import TypedDict

from langgraph.graph import StateGraph,END

from langgraph.common import image_graph

#演示子图和主图共享同一个数据状态

class GlobalState(TypedDict):
    node_name: str


def parent_node(state:GlobalState):
    print("parent_node")
    return {"node_name":"parent_node"}

def parent_sec_node(state:GlobalState):
    print("parent_sec_node")
    return {"node_name":"parent_sec_node"}

def parent_third_node(state:GlobalState):
    print("parent_third_node")
    return {"node_name":"parent_third_node"}


def sub_node(state:GlobalState):
    print("sub_node get parent_node_name:",state["node_name"])

def sub_sec_node(state:GlobalState):
    print("sub_sec_node")

parent_graph = StateGraph(GlobalState)


sub_graph = StateGraph(GlobalState)
sub_graph.add_node("sub_node",sub_node)
sub_graph.add_node("sub_sec_node",sub_sec_node)
sub_graph.set_entry_point("sub_node")
sub_graph.add_edge("sub_node","sub_sec_node")
sub_graph.add_edge("sub_sec_node",END)

parent_graph.add_node("parent_node",parent_node)
parent_graph.add_node("parent_sec_node",parent_sec_node)
parent_graph.add_node("parent_third_node",parent_third_node)
parent_graph.add_node("sub_graph",sub_graph.compile())

parent_graph.set_entry_point("parent_node")
parent_graph.add_edge("parent_node","parent_sec_node")
parent_graph.add_edge("parent_sec_node","parent_third_node")
parent_graph.add_edge("parent_third_node","sub_graph")
parent_graph.add_edge("sub_graph",END)

app = parent_graph.compile()
image_graph(app,"子图共享状态.png")
invoke = app.invoke({"node_name": "这是nodename"})
print(invoke)