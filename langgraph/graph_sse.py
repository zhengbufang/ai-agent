from langchain_core.tools import tool
from typing import Literal
# 导入创建react代理的函数
from langgraph.prebuilt import create_react_agent
from langchain.agents import create_agent
from model import get_model


@tool
def query_weather(city: Literal["上海", "北京"]):
    """获取指定城市的天气."""
    if city == "上海":
        # 返回纽约的天气信息
        return "It might be cloudy in nyc"
        # 如果城市是旧金山
    elif city == "北京":
        # 返回旧金山的天气信息
        return "It's always sunny in sf"
        # 如果城市不是nyc或sf
    else:
        # 抛出一个断言错误
        raise AssertionError("Unknown city")

tools = [query_weather]

model = get_model()

# 使用模型和工具创建一个react代理
graph = create_agent(model, tools)

# 定义输入消息，询问旧金山的天气
inputs = {"messages": [("human", "what's the weather in 上海")]}
# 异步迭代代理的输出流，模式为"values"
# for chunk in graph.stream(inputs, stream_mode="values"):
for chunk in graph.stream(inputs, stream_mode="updates"):
    # 打印最后一条消息的格式化内容
    chunk["messages"][-1].pretty_print()

####如果我们只想获取最终结果，我们可以使用相同的方法，并跟踪我们收到的最后一个值