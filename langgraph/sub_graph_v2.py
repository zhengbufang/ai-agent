import operator
from typing import List

from langgraph.graph import StateGraph,START,END
from typing_extensions import TypedDict
from typing import (
    Annotated,
    Any,
    Literal,
    cast,
    Dict
)

class StartState(TypedDict):
    source:str
    json_source:List[str]
    target_source:str

class JsonStartState(TypedDict):
    json_source:List[str]

class TargetStartState(TypedDict):
    target_source:str


def convert_source(state):
    print("1111")


def json_source_state(state):
    source = state['state']
    return {"source":"你是一个","json_source":["1","2","3"]}

def target_source_state(state):

    return {"source":"我是哈哈哈","target_source":["4","5","6"]}

json_builder =  StateGraph(JsonStartState)
json_builder.add_node("convert_node",json_source_state)
json_builder.add_edge(START,"convert_node")
json_builder.add_edge("convert_node",END)

target_builder =  StateGraph(TargetStartState)
target_builder.add_node("convert_node",target_source_state)
target_builder.add_edge(START,"convert_node")
target_builder.add_edge("convert_node",END)


entry_builder =  StateGraph(StartState)
entry_builder.add_node("start_node",convert_source)
entry_builder.add_node("json_node",json_builder.compile())
entry_builder.add_node("target_node",target_builder.compile())


entry_builder.add_edge(START,"start_node")
entry_builder.add_edge("start_node","json_node")
entry_builder.add_edge("start_node","target_node")
entry_builder.add_edge("json_node",END)
entry_builder.add_edge("target_node",END)

app = entry_builder.compile()
graph_png = app.get_graph(xray=1).draw_mermaid_png()
with open("sub_graph.png", "wb") as f:
    f.write(graph_png)

print(app.invoke({"source":""}, debug=False))