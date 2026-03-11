from typing import TypedDict

from langgraph.graph import StateGraph,END

from langgraph.common import image_graph

#演示子图和主图不共享同一个数据状态时
# 没有共享的状态键时，父图不能直接将已编译的子图作为节点添加，
# 而需要创建一个节点函数作为中介，
# 在该节点手动调用子图，并将父图状态转换为子图


class GlobalState(TypedDict):
    node_name: str
    sub_result: str

def parent_node(state:GlobalState):
    print("parent_node")
    return {"node_name":"parent_node"}

def parent_sec_node(state:GlobalState):
    print("parent_sec_node")
    return {"node_name":"parent_sec_node"}

def parent_third_node(state:GlobalState):
    print("parent_third_node")
    return {"node_name":"parent_third_node"}



class SubState(TypedDict):
    sub_node_name:str

def sub_node(state:SubState):
    print("sub_nod get:",state["sub_node_name"])

def sub_sec_node(state:SubState):
    print("sub_sec_node 更新数据")
    return {"sub_node_name":"这是子图处理的结果"}





sub_graph = StateGraph(SubState)
sub_graph.add_node("sub_node",sub_node)
sub_graph.add_node("sub_sec_node",sub_sec_node)
sub_graph.set_entry_point("sub_node")
sub_graph.add_edge("sub_node","sub_sec_node")
sub_graph.add_edge("sub_sec_node",END)
sub_app = sub_graph.compile()

#中介函数通过数据的状态转换  把父图的数据交给子图去做处理  并最终返回给父图 多了一层数据转换
def sub_handle(state: GlobalState):
    parent_node = state["node_name"]
    result = sub_app.invoke({"sub_node_name": parent_node})
    return {"sub_result":result["sub_node_name"]}

parent_graph = StateGraph(GlobalState)
parent_graph.add_node("parent_node",parent_node)
parent_graph.add_node("parent_sec_node",parent_sec_node)
parent_graph.add_node("parent_third_node",parent_third_node)
parent_graph.add_node("sub_handle",sub_handle)




parent_graph.set_entry_point("parent_node")
parent_graph.add_edge("parent_node","parent_sec_node")
parent_graph.add_edge("parent_sec_node","parent_third_node")
parent_graph.add_edge("parent_third_node","sub_handle")
parent_graph.add_edge("sub_handle",END)



app = parent_graph.compile()
invoke = app.invoke({"node_name": "这是parent_node_name"})
print(invoke)