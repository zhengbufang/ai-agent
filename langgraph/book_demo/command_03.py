from langgraph.graph import MessagesState, StateGraph,END
from langgraph.types import Command
from narwhals import Boolean

#command demo
# 允许单个节点中整合状态更新和流程控制逻辑，一般情况下节点负责更新状态，
# 边负责控制流程跳转，但在实际应用中，需要节点同时完成这两项功能

class SelfState(MessagesState):
    question:str
    start:Boolean
    command:Boolean

def start_node(state:SelfState):
    print("进入start_node")
    return {"start":True}

def second_node(state:SelfState):
    print("进入second_node")


def end_node(state:SelfState):
    print("进入end_node")

def command_node(state:SelfState):
    print("进入command_node")
    if "end" in state['question']:
        return Command(goto="end",update={"question":"end"})
    return Command(goto="second", update={"question": "second"})

graph = StateGraph(SelfState)

graph.add_node("start",start_node)
graph.add_node("command",command_node)
graph.add_node("second",second_node)
graph.add_node("end",end_node)


graph.set_entry_point("start")
graph.add_edge("start","command")
graph.add_edge("second","end")
graph.add_edge("end",END)

app = graph.compile()

invoke = app.invoke({"question":"endd"})
print("-"*50)
print(invoke)
