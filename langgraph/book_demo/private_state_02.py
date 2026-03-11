# 你这个问题问到了 LangGraph 1.0 状态管理的核心关键点！确实，LangGraph 节点的主入参只能是全局状态，
# 但要给节点传递「自定义类入参」+「私有状态」，核心思路是：
# 全局状态只存「必要共享数据」；
# 节点的「自定义类私有参数」通过 LangGraph 的 config 配置参数传递（而非全局状态）；
# 节点内部从 config 中提取私有参数，作为节点私有状态使用。
import uuid
from dataclasses import dataclass

from typing import Dict, Any, Optional

from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import MessagesState, StateGraph,END


class GlobalState(MessagesState):
    question :str
    user_id:str

@dataclass
class PrivateState:
    timeout: int
    secret_key: str

def global_node(state:GlobalState):
    print(state['question'])
    return {'user_id':uuid.uuid4()}

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
graph.add_node("private",private_node)
graph.add_node("final",final_node)

graph.set_entry_point("global")
graph.add_edge("global","private")
graph.add_edge("private","final")
graph.add_edge("private",END)

graph_compile = graph.compile()

invoke = graph_compile.invoke({"messages": [HumanMessage(content="哈哈哈")], "question": "错过了就是错过了"},
                              config={"configurable":{"private_config":{"timeout":100,"secret_key":"secret_key"}}})
