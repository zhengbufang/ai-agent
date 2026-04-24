from typing import TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START,END
from langgraph.types import interrupt, Command

# 1. 定义状态
class State(TypedDict):
    user_name: str
    user_age: int
    final_message: str

# 2. 定义节点
def get_name(state: State):
    """直接设置一个示例姓名，模拟已有信息"""
    return {"user_name": "小明"}

def ask_age(state: State):
    """中断，等待用户输入年龄"""
    # interrupt 会暂停图执行，并向外抛出 value，等待 resume
    age = interrupt("请输入您的年龄：")  # 这里会抛出中断，等待外部恢复时传入值
    return {"user_age": int(age)}

def greet(state: State):
    """根据年龄生成问候语"""
    age = state["user_age"]
    message = f"{state['user_name']}，您今年 {age} 岁，欢迎！"
    return {"final_message": message}

# 3. 构建图
builder = StateGraph(State)
builder.add_node("get_name", get_name)
builder.add_node("ask_age", ask_age)
builder.add_node("greet", greet)

builder.add_edge(START, "get_name")
builder.add_edge("get_name", "ask_age")
builder.add_edge("ask_age", "greet")
builder.add_edge("greet", END)

# 设置记忆功能
memory = MemorySaver()

graph = builder.compile(checkpointer=memory)

# 4. 执行图并处理中断
# 首次执行：到达 ask_age 节点时触发中断
thread_config = {"configurable": {"thread_id": "1"}}

# 第一次运行，会停在 ask_age 节点
try:
    result = graph.invoke({}, config=thread_config)
except Exception as e:
    # 实际不会抛出异常，而是返回一个包含中断信息的对象
    pass

# 查看当前状态，可以看到中断信息
state_snapshot = graph.get_state(thread_config)
print("中断信息：", state_snapshot.tasks[0].interrupts[0].value)
# 输出：中断信息： 请输入您的年龄：

# 5. 恢复执行，提供用户输入
user_input = "25"  # 模拟人工输入
result = graph.invoke(Command(resume=user_input), config=thread_config)

print(result["final_message"])