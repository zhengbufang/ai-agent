from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from typing import Annotated
from typing_extensions import TypedDict
from operator import add

class State(TypedDict):
    foo: int
    bar: Annotated[list[str], add]

def node_a(state: State):
    return {"foo": "a", "bar": ["a"]}

def node_b(state: State):
    return {"foo": "b", "bar": ["b"]}


workflow = StateGraph(State)
workflow.add_node(node_a)
workflow.add_node(node_b)
workflow.add_edge(START, "node_a")
workflow.add_edge("node_a", "node_b")
workflow.add_edge("node_b", END)

checkpointer = MemorySaver()
graph = workflow.compile(checkpointer=checkpointer)

config = {"configurable": {"thread_id": "1"}}
result = graph.invoke({"foo": ""}, config)
print(result)

# 获取最新的状态快照
stateSnapshot = graph.get_state(config)
print(stateSnapshot)
print("="*50)


#获取状态历史
print(list(graph.get_state_history(config)))
print("*"*50)


#重播还可以回放先前的图执行。如果我们在调用图时带有thread_id和checkpoint_id，那么我们将*从一个与checkpoint_id对应的检查点回放*图。
config2 = {"configurable": {"thread_id": "1","checkpoint_id":stateSnapshot.config.get("configurable",{}).get("checkpoint_id",{})}}
print(graph.get_state_history(config2))

#更新状态
# 现在假设图的当前状态是 {"foo": 1, "bar": ["a"]}
state = graph.update_state(config, {"foo": 2, "bar": ["b"]})
print(state.values())

# 调用后那么图的新状态将是：{"foo": 2, "bar": ["a", "b"]}