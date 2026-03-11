
from typing import TypedDict, Annotated

from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph,START,END
from langgraph.prebuilt import InjectedState
from langgraph.types import StreamWriter

from model import get_model


class JokeState(TypedDict):
    joke:str
    topic:str

def generate_joke(state:JokeState):
    llm = get_model()
    invoke = llm.invoke([HumanMessage(f"给我生成一个{state["topic"]}的笑话，限制100字")])
    return {"joke":invoke.content}

#消息流
graph = StateGraph(JokeState)
graph.add_node("generate_joke",generate_joke)
graph.add_edge(START,"generate_joke")
graph.add_edge("generate_joke",END)
app = graph.compile()

#消息流 字符字符单个输出
for message_chunk,metadata in app.stream({"topic": "猴子"}, stream_mode="messages"):
    print(message_chunk.content,end="|",flush=True)

#