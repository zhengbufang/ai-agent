import operator
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph,END

from langgraph.common import image_graph


class GlobalState(TypedDict):
   char: Annotated[list, operator.add]

def a_node(state:GlobalState):
    print("a_node:",state["char"])
    return {"char":["a"]}
def b_node(state:GlobalState):
    print("b_node:", state["char"])
    return {"char":["b"]}
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

graph.set_entry_point("a")
graph.add_edge("a","b")
graph.add_edge("a","c")
graph.add_edge("b","d")
graph.add_edge("c","d")
graph.add_edge("d",END)

app = graph.compile()
image_graph(app,"并行分支.png")
invoke = app.invoke({"char": []})
print(invoke)
