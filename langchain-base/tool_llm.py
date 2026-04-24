import json

from langchain_community.tools import MoveFileTool
from langchain_core.messages import HumanMessage
from langchain_core.utils.function_calling import convert_to_openai_function
from model import get_model
from langchain.tools import tool

model = get_model()

# 工具调用不知道为什么没生效
def tool_v1():
    messages = [HumanMessage(content="将文件a移动到桌面")]

    tools = [MoveFileTool()]

    functions = [convert_to_openai_function(i) for i in tools]

    response = model.invoke(input=messages, functions=functions)
    # response = model.invoke(input=[HumanMessage(content="今天天气如何")],functions=functions)
    print(response)

def tool_v2():
    messages = [HumanMessage(content="将文件a移动到桌面")]

    tools = [MoveFileTool()]

    chain = model.bind_tools(tools)

    response = chain.invoke(messages)
    print(response)


@tool(name_or_callable="weather",description="查询某个地方的天气，查询某个时间的天气")
def weather(name:str,date:str):
    return f"{name}26摄氏度 时间为{date}"

if __name__ == "__main__":

    chain = model.bind_tools([weather])
    response =  chain.invoke("说说深圳明天的天气")

    if("tool_calls" in response.response_metadata["finish_reason"]):
        for tool_call in response.tool_calls:
            if tool_call['name'] == weather.name:
                result = weather.invoke(tool_call)
                print(result.content)
