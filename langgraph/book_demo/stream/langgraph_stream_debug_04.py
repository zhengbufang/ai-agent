
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

#debug模式 在图执行的每个步骤提供详细数据
for chunk in app.stream({"desc": "desc1", "common": "common1"}, stream_mode="debug"):
    print(chunk)

# {'step': 1, 'timestamp': '2026-03-11T13:20:45.124899+00:00', 'type': 'task', 'payload': {'id': 'c996c56d-144b-5192-9e01-f7ef739b241f', 'name': 'first', 'input': {'desc': 'desc1', 'common': 'common1'}, 'triggers': ('branch:to:first',)}}
# {'step': 1, 'timestamp': '2026-03-11T13:20:45.125176+00:00', 'type': 'task_result', 'payload': {'id': 'c996c56d-144b-5192-9e01-f7ef739b241f', 'name': 'first', 'error': None, 'result': {'desc': 'desc1 first_update_node '}, 'interrupts': []}}
# {'step': 2, 'timestamp': '2026-03-11T13:20:45.125470+00:00', 'type': 'task', 'payload': {'id': '5744335d-846a-57e2-61c1-7d501ce6dba4', 'name': 'second', 'input': {'desc': 'desc1 first_update_node ', 'common': 'common1'}, 'triggers': ('branch:to:second',)}}
# {'step': 2, 'timestamp': '2026-03-11T13:20:45.125691+00:00', 'type': 'task_result', 'payload': {'id': '5744335d-846a-57e2-61c1-7d501ce6dba4', 'name': 'second', 'error': None, 'result': {}, 'interrupts': []}}
# {'step': 3, 'timestamp': '2026-03-11T13:20:45.125944+00:00', 'type': 'task', 'payload': {'id': '8faeb6c9-6fd0-92eb-a6a6-783de530103f', 'name': 'third', 'input': {'desc': 'desc1 first_update_node ', 'common': 'common1'}, 'triggers': ('branch:to:third',)}}
# {'step': 3, 'timestamp': '2026-03-11T13:20:45.126106+00:00', 'type': 'task_result', 'payload': {'id': '8faeb6c9-6fd0-92eb-a6a6-783de530103f', 'name': 'third', 'error': None, 'result': {}, 'interrupts': []}}
# {'step': 4, 'timestamp': '2026-03-11T13:20:45.126258+00:00', 'type': 'task', 'payload': {'id': '7bdd181b-9e5c-b8c5-8a1d-d939c5c076ea', 'name': 'common', 'input': {'desc': 'desc1 first_update_node ', 'common': 'common1'}, 'triggers': ('branch:to:common',)}}
# {'step': 4, 'timestamp': '2026-03-11T13:20:45.126415+00:00', 'type': 'task_result', 'payload': {'id': '7bdd181b-9e5c-b8c5-8a1d-d939c5c076ea', 'name': 'common', 'error': None, 'result': {'common': 'common1 common_update_node '}, 'interrupts': []}}
