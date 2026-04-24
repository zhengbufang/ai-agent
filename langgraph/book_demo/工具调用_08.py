from typing import Annotated

from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode

#运行会报错





# #ToolNode
# @tool(name_or_callable="query_weather",description="查询具体城市天气的工具")
# def query_weather(city:Annotated[str,"城市"]):
#     if city.startswith("北京"):
#         return "风和日丽"
#     elif city.startswith("上海"):
#         return "晴转多云"
#     elif city.startswith("西藏"):
#         return "暴雪转小雪"
#     return "未查询到具体天气"
#
# @tool(name_or_callable="query_bank_money",description="查询银行账户还有多少钱的工具")
# def query_bank_money(card_no:Annotated[str,"银行卡卡号"]):
#     if card_no.startswith("42"):
#         return 10000
#     elif card_no.startswith("43"):
#         return 1500000
#     elif card_no.startswith("44"):
#         return 2000000
#
# tools = [query_bank_money,query_weather]
# tool_node = ToolNode(tools)
#
# #手动调用工具
# # 构造单个工具调用请求的AI message
# # 模拟大模型给我门返回需要调用工具的结果
# messages_with_tool_call = AIMessage(content="",tool_calls=[
#     {
#         "name":"query_bank_money",
#         "args":{"card_no":"4302155315452123"},
#         "id":"tool_call_id", #工具id 唯一标志
#         "type":"tool_call" #固定类型为工具调用
#     }
# ])
#
# state = MessagesState(messages=[{"content": "查询43021321321账户余额", "tool_calls": [{"name": "query_bank_money", "args": {"card_no":"43021321321"}, "id":"123"}]}])
# config = RunnableConfig()
# config["configurable"] = {"tools": [t.name for t in tools]}
#
# result = tool_node.invoke(state,config=config)
# print(result)


@tool
def multiply(a: int, b: int) -> int:
    """两数相乘"""
    return a * b
tools = [multiply]

# 2. 定义工具节点
tool_node = ToolNode(tools)

# 3. 正确调用方式
## 方式A：直接调用 ToolNode.invoke（需手动传 Config）
state = MessagesState(messages=[{"content": "3*4", "tool_calls": [{"name": "multiply", "args": {"a":3,"b":4}, "id":"123"}]}])
# 关键：构造正确的 Config
config = RunnableConfig()
config["configurable"] = {"tools": [t.name for t in tools]}  # 必须是 configurable → tools 层级
result = tool_node.invoke(state, config=config)
print(result)