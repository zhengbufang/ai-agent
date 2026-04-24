import uuid

from langchain_core.runnables import RunnableConfig
from langchain_core.stores import InMemoryStore
from langgraph.checkpoint.memory import MemorySaver
from langgraph.func import task, entrypoint
from langgraph.store.base import BaseStore
from langgraph.types import StreamWriter, RetryPolicy
from typing import Any

#@task 用于定义langgraph工作流中的各工作单元，它的调用返回结果是一个python的future对象

retry_policy = RetryPolicy(max_attempts=2,retry_on=TimeoutError)

@task(name="api_data_fetcher",retry=retry_policy)
def data_fetcher(user_input:str,   #用户输入
                ) -> dict:
    """ 从带有重试策略的API 获取数据"""
    import time,random
    time.sleep(random.random())  #模拟网络延迟
    if random.random() < 0.3:  #模拟30%的延迟概率
        raise TimeoutError("API请求超时")
    return {"status":"success","data":f"来自{user_input}的数据"}

@entrypoint(checkpointer=MemorySaver())
def my_workflow(user_input:str):
    api_result = data_fetcher(user_input=user_input).result()
    return {"workflow_result":"数据已处理","api_response":api_result}

config = {"configurable":{"thread_id":"12312"}}
result = my_workflow.invoke("http://www.baidu.com",config)
print(result)

#工作流处理的输入：{'message': 'hello 你好'}