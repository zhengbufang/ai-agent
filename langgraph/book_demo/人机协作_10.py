import uuid
from typing import TypedDict, Literal

from langgraph.checkpoint.mongodb import MongoDBSaver
from langgraph.graph import StateGraph
from langgraph.types import Command, interrupt


#人机协作，在需要人工验证的场景中，可以对工作流进行中断，，设置存档点引入人工审查，批准或反馈

# 注意事项，1 必须配置存档点，完全依赖持久化机制来保存和暂停执行时的图状态，
# 2 thread_id必须要一直同一个会话，人机环路工作流本质上依赖线程的概念，以维护不同对话或工作流执行的独立上下文和持久状态

DB_URI = "localhost:27017"


class State(TypedDict):
    topic:str
    proposed_action_details:str

def propose_action(state:State):
    """ 提出一个需要人工审批的操作"""
    return {
        **state, # 解包操作 会把state的键值对copy到这里  然后输出state原有的+proposed_action_details键值对
        "proposed_action_details":f"基于主题‘{state['topic']}’的操作提议"
    }


def human_approval_node(state:State) -> Command[Literal["execute_action","revise_action"]] :
    """ 在执行关键行动前，请求人工审批 """
    approval_request = interrupt({
        "question":"Approve the execution of the following action?",
        "action_details":state["proposed_action_details"] #待审批操作的详情
    })

    if approval_request["user_response"] == "approve": ###用户批准
        return Command(goto="execute_action")
    else:
        return Command(goto="revise_action")

def execute_action(state:State):
    """执行已批准的操作"""
    return {
        **state,  # 解包操作 会把state的键值对copy到这里  然后输出state原有的+proposed_action_details键值对
        "proposed_action_details": f"已执行操作:‘{state['proposed_action_details']}’"
    }

def revise_action(state:State):
    """修改已被拒绝的操作"""
    return {
        **state,  # 解包操作 会把state的键值对copy到这里  然后输出state原有的+proposed_action_details键值对
        "proposed_action_details": f"修改后的操作:‘{state['proposed_action_details']}’（已调整）"
    }



with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:
    graph = StateGraph(State)
    graph.add_node("node_proposing_action", propose_action)
    graph.add_node("human_approval", human_approval_node)
    graph.add_node("execute_action", execute_action)
    graph.add_node("revise_action", revise_action)

    graph.add_edge("node_proposing_action", "human_approval")
    graph.add_edge("revise_action", "human_approval")

    graph.set_entry_point("node_proposing_action")
    app = graph.compile(checkpointer=checkpointer)
    thread_id = uuid.uuid4()
    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }
    app.invoke({"topic":"重要决策"},config=config)
    print(app.get_state(config))
    print("="*10)

    #拒绝提议
    app.invoke(Command(resume={"user_response":"deny"}), config=config)
    print(app.get_state(config))
    print("=" * 30)

    # 批准提议  resume接受人工操作的值穿传递给langgraph
    app.invoke(Command(resume={"user_response": "approve"}), config=config)
    print(app.get_state(config))
    print("=" * 50)
