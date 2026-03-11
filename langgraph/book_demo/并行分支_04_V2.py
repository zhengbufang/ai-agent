import operator
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph,END

from langgraph.common import image_graph

#如某分支包含多个步骤（节点后B需要执行b_2）
class GlobalState(TypedDict):
   char: Annotated[list, operator.add]

def a_node(state:GlobalState):
    print("a_node:",state["char"])
    return {"char":["a"]}
def b_node(state:GlobalState):
    print("b_node:", state["char"])
    return {"char":["b"]}

def b_2_node(state:GlobalState):
    print("b_2_node:", state["char"])
    return {"char":["b_2"]}

def c_node(state:GlobalState):
    print("c_node:", state["char"])
    return {"char":["c"]}
def d_node(state:GlobalState):
    print("d_node:", state["char"])
    return {"char":["d"]}

graph = StateGraph(GlobalState)
graph.add_node("a",a_node)
graph.add_node("b",b_node)
graph.add_node("c",c_node)
graph.add_node("d",d_node)

graph.add_node("b_2",b_2_node)

graph.set_entry_point("a")
graph.add_edge("a","b")
graph.add_edge("a","c")
graph.add_edge("b","b_2")
graph.add_edge(["b_2","c"],"d")  # 强制节点在b_2和c执行完成后 才会调用
graph.add_edge("d",END)


app = graph.compile()
image_graph(app,"并行分支_v2.png")
invoke = app.invoke({"char": []})
print(invoke)
