from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command, interrupt
from langgraph.checkpoint.memory import MemorySaver
from IPython.display import Image, display

class State(TypedDict):
    input: str
    user_feedback: str

def step_1(state):
    print("---Step 1---")
    pass

def human_feedback(state):
    print("---human_feedback---")
    feedback = interrupt("Please provide feedback:")
    return {"user_feedback": feedback}

def step_3(state):
    print("---Step 3---")
    pass

builder = StateGraph(State)
builder.add_node("step_1", step_1)
builder.add_node("human_feedback", human_feedback)
builder.add_node("step_3", step_3)
builder.add_edge(START, "step_1")
builder.add_edge("step_1", "human_feedback")
builder.add_edge("human_feedback", "step_3")
builder.add_edge("step_3", END)

# 设置记忆功能
memory = MemorySaver()

# 添加
graph = builder.compile(checkpointer=memory)

# 查看
display(Image(graph.get_graph().draw_mermaid_png()))


# 输入
initial_input = {"input": "hello world"}

# 线程
config = {"configurable": {"thread_id": "1"}}

# 运行图表直到第一次中断。
for event in graph.stream(initial_input, config, stream_mode="updates"):
    print(event)
    print("\n")