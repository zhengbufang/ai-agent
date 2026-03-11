#langgraph 对map_reduce的支持
import operator
from typing import TypedDict, Annotated

from langgraph.graph import StateGraph,END
from langgraph.types import Send

from langgraph.common import image_graph


class DataState(TypedDict):
    datas:list[str]  #定义一个需要被处理的数据列表
    final_result:str

def spit_node(state:DataState):
    pass
# 数据拆分
def spit_data(state:DataState):
    datas = state["datas"]
    send_list = []
    for data in datas:
        send_list.append(Send("handle_data",{"data":data})) #用于动态路由到多个map示例
    return send_list

# 数据计算
class HandleData(TypedDict):
    data:str

#把每个元数据用 *加工
def handle_data(state:HandleData):
    datas = state["data"]
    print("handle_data:",datas)
    return {"result":["*"+datas+"*"]}  #返回中间结果

#数据合并
class ReduceData(TypedDict):
    result:Annotated[list,operator.add]

def reduct_data(state:ReduceData):
    datas = state["result"]
    print("reduct_data:",datas)
    return {"final_result":datas}

graph =StateGraph(DataState)
graph.add_node("spit_node",spit_node)
graph.add_node("handle_data",handle_data)
graph.add_node("reduce_data",reduct_data)

graph.set_entry_point("spit_node")
graph.add_conditional_edges("spit_node",spit_data,["handle_data"])
graph.add_edge("handle_data","reduce_data")
graph.add_edge("reduce_data",END)

app = graph.compile()
image_graph(app,"map_reduce.png")
invoke = app.invoke({"datas": ["A", "B", "C"]})
print(invoke)