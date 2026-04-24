import uuid

from langchain_core.messages import HumanMessage, ToolMessage
from langgraph.graph import MessagesState, StateGraph,END
from langgraph.prebuilt import ToolNode

from langgraph.types import Command
from sqlalchemy import Uuid

from model import get_model
from langchain_core.tools import tool, InjectedToolCallId
from typing import Literal, Annotated


#从self_graph_01 copy 修改

class WeatherState(MessagesState):
    weather:str

# @tool(name_or_callable="search_city_weather",description="查询某个城市天气")
# def search_city_weather(query:str):
#   if query == "shanghai":
#       return "shanghai is cool"
#   elif query == "beijing":
#       return "5-13度,晴转多云"
#   return "小雨转中雨"

#tool_call_id 注意必须要用这个LLM注入进来的，不然汇会报错   用于注入工具调用ID的注解。
# 核心是「LLM 发起的工具调用请求」和「工具返回的 ToolMessage」在 tool_call_id 或消息结构上不匹配，
@tool(name_or_callable="search_city_weather",description="查询某个城市天气")
def search_city_weather(query:str,tool_call_id:Annotated[str,InjectedToolCallId]):

  #工具函数直接返回Command对象
  return Command(update={
      "messages": [ToolMessage(content="5-13度,晴转多云",tool_call_id=tool_call_id)],
      "weather":"晴转多云,5-13度"  #更新weather状态键
  })

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

graph = StateGraph(WeatherState)
graph.add_node("agent",call_agent)
graph.add_node("tool_node",tool_node)

#从agent调用开始
graph.set_entry_point("agent")

graph.add_conditional_edges("agent",route_next_node,"tool_node")

#工具调用后 还要给到大模型去进行回答
graph.add_edge("tool_node","agent")

app = graph.compile()
response = app.invoke({"messages": [{"role":"user","content":"beijing的天气如何"}]})

print("="*50)
print(type(response))
print(response)



