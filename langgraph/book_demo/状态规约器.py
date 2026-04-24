# 状态规约器 用于多个节点并行更新同一个状态键时，合并策略的场景
# 下面流程时线性的，所以看不出效果，可以参考sub_graph.py子图 状态source


import operator
import uuid
from dataclasses import dataclass

from typing import Dict, Any, Optional,Annotated

from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import MessagesState, StateGraph,END

#自定义规约器函数
def reducer_extend_unqiue(left:list[str] | None,right:list[str] | None) -> list[str]:
    """
      自定义规约函数，用于合并字符串列表，并进行去重
    """
    existing_items = left if left else [] #如过left 为None 则初始化为空列表

    new_items = right if right else []  # 如过left 为None 则初始化为空列表

    combined_items = existing_items + new_items

    return list(set(combined_items)) #使用set 去重并转换为list 返回

class GlobalState(MessagesState):
    question :str
    user_id:str
    # source: Annotated[list, operator.add]
    source: Annotated[list[str], reducer_extend_unqiue]

@dataclass
class PrivateState:
    timeout: int
    secret_key: str

def global_node(state:GlobalState):
    gluid = uuid.uuid4()
    print("global uid:",gluid,state['question'])
    return {'user_id':gluid}

#规约演示节点 并发更新user_id
def reduce_node(state:GlobalState):
    uid = uuid.uuid4()
    print("reduce uid:",uid)
    return {'user_id':uid}

def private_node(state:GlobalState,config:RunnableConfig):
    get = config.get("configurable").get("private_config")
    print("private_node get:",get)
    # print("private_config timeout:",private_config.timeout)
    # print("private_config secret_key:",private_config.secret_key)

def final_node(state:GlobalState,config:RunnableConfig):
    print("final_node question:",state['question'])
    print("final_node user_id:", state['user_id'])




graph = StateGraph(GlobalState)
graph.add_node("global",global_node)
graph.add_node("reduce",reduce_node)
graph.add_node("private",private_node)
graph.add_node("final",final_node)

graph.set_entry_point("global")
graph.add_edge("global","reduce")
graph.add_edge("reduce","private")
graph.add_edge("private","final")
graph.add_edge("private",END)

graph_compile = graph.compile()

invoke = graph_compile.invoke({"messages": [HumanMessage(content="哈哈哈")], "question": "错过了就是错过了"},
                              config={"configurable":{"private_config":{"timeout":100,"secret_key":"secret_key"}}})



