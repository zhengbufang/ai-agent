import uuid

from langchain_core.runnables import RunnableConfig
from langchain_core.stores import InMemoryStore
from langgraph.checkpoint.memory import MemorySaver
from langgraph.func import entrypoint
from langgraph.store.base import BaseStore
from langgraph.types import StreamWriter

from typing import Any
store = InMemoryStore()

checkpointer = MemorySaver()

#@entrypoint 定义工作流的边界和入口点，简化Graph API开发，需要定义节点，边，状态的繁杂流程
# 注意一定要传入checkpointer= 否则会报错

@entrypoint(checkpointer=checkpointer)
def my_workflow(user_input:dict,   #用户输入
                *,
                previous: Any=None,  #用于先前状态的可注入参数
                store: BaseStore,    #长期内存存贮的可注入参数
                writer:StreamWriter, #自定义工作流写入
                config:RunnableConfig
                ) -> str:
    """ 复杂演示入口点参数的工作流"""

    api_key = config["configurable"].get("api_key",None)
    writer(f"工作流‘{config["metadata"]["thread_id"]}' 以API版本启动：{api_key}")

    return f"工作流处理的输入：{user_input}"

config = {"configurable":{"thread_id":"12312"}}
result = my_workflow.invoke({"message": "hello 你好"},config)
print(result)

#工作流处理的输入：{'message': 'hello 你好'}