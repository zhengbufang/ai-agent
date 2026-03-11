from langchain_core.messages import HumanMessage
from langgraph.graph import MessagesState, StateGraph,END
from langgraph.prebuilt import ToolNode

from model import get_model
from langchain_core.tools import tool
from typing import Literal

@tool(name_or_callable="search_city_weather",description="查询某个城市天气")
def search_city_weather(query:str):
  if query == "shanghai":
      return "shanghai is cool"
  elif query == "beijing":
      return "beijing is wekkk"
  return "weather is beautiful"

tool = [search_city_weather]

#封装成工具节点
tool_node = ToolNode(tool)

# 大模型绑定工具
agent = get_model().bind_tools(tool)

#大模型调用节点
def call_agent(state:MessagesState):
    response = agent.invoke(state['messages'])
    print("call_agent_response:",response)
    return {"messages": [response]}

# 路由下一个要去的结点 如果大模型说要走工具调用则转到工具调用节点,如果不需要则说明大模型已经结束了回答，直接结束
def route_next_node(state:MessagesState) -> Literal["tool_node", END]:
    print("route_next_message:",state['messages'])
    last_message = state['messages'][-1]
    if last_message.tool_calls:
        return "tool_node"
    return END

graph = StateGraph(MessagesState)
graph.add_node("agent",call_agent)
graph.add_node("tool_node",tool_node)

#从agent调用开始
graph.set_entry_point("agent")

graph.add_conditional_edges("agent",route_next_node,"tool_node")

#工具调用后 还要给到大模型去进行回答
graph.add_edge("tool_node","agent")

app = graph.compile()
graph_png = app.get_graph(xray=1).draw_mermaid_png()
with open("../self_graph.png", "wb") as f:
    f.write(graph_png)

response = app.invoke({"messages": [{"role":"user","content":"北京的天气如何"}]})

print("="*50)
print(type(response))
print(response)



