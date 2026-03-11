from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.graph.state import CompiledStateGraph
from typing import Dict, Any, Generator
import os
import asyncio

from model import get_model

# --------------------------
# 1. 初始化FastAPI应用
# --------------------------
app = FastAPI(title="LangGraph Agent SSE API", version="1.0")

# --------------------------
# 2. 配置LLM（使用OpenAI，需替换为自己的API Key）
# --------------------------
# 方式1：直接设置环境变量（推荐在.env文件中配置）
os.environ["OPENAI_API_KEY"] = "your-openai-api-key"  # 替换为你的API Key
# 方式2：如果用国内代理，可添加base_url
# os.environ["OPENAI_BASE_URL"] = "https://api.openai.com/v1"

# 初始化大模型
llm = get_model()


# --------------------------
# 3. 定义Agent状态（LangGraph核心）
# --------------------------
class AgentState(BaseModel):
    """Agent的状态定义，包含输入问题、思考过程、工具调用结果、最终回答"""
    question: str  # 用户输入的问题
    thought: str = ""  # Agent的思考过程
    tool_result: str = ""  # 工具调用结果
    answer: str = ""  # 最终回答


# --------------------------
# 4. 定义工具函数
# --------------------------
@tool
def calculate(num1: float, num2: float, operation: str) -> str:
    """简单的计算工具，支持加减乘除"""
    if operation == "add":
        result = num1 + num2
    elif operation == "subtract":
        result = num1 - num2
    elif operation == "multiply":
        result = num1 * num2
    elif operation == "divide":
        if num2 == 0:
            return "错误：除数不能为0"
        result = num1 / num2
    else:
        return f"错误：不支持的运算类型{operation}，仅支持add/subtract/multiply/divide"
    return f"{num1} {operation} {num2} = {result}"


# --------------------------
# 5. 定义LangGraph节点函数
# --------------------------
async def think_node(state: AgentState) -> Dict[str, Any]:
    """思考节点：分析用户问题，决定是否需要调用工具"""
    yield f"data: 🔍 Agent正在思考你的问题：{state.question}\n\n"
    await asyncio.sleep(1)  # 模拟思考延迟

    # 简单判断是否需要调用计算工具
    if any(word in state.question for word in ["计算", "加", "减", "乘", "除"]):
        thought = "用户的问题需要调用计算工具来解决"
    else:
        thought = "用户的问题不需要调用工具，直接回答即可"

    yield f"data: 💡 思考结果：{thought}\n\n"
    yield {"thought": thought}


async def tool_node(state: AgentState) -> Dict[str, Any]:
    """工具调用节点：调用计算工具"""
    yield f"data: 🛠️ 开始调用计算工具...\n\n"
    await asyncio.sleep(1)

    # 简单解析计算指令（实际场景建议用函数调用解析）
    try:
        # 示例：解析"计算10加20" → num1=10, num2=20, operation=add
        question = state.question.replace("计算", "").strip()
        if "加" in question:
            num1, num2 = question.split("加")
            operation = "add"
        elif "减" in question:
            num1, num2 = question.split("减")
            operation = "subtract"
        elif "乘" in question:
            num1, num2 = question.split("乘")
            operation = "multiply"
        elif "除" in question:
            num1, num2 = question.split("除")
            operation = "divide"
        else:
            tool_result = "无法解析计算指令，请使用格式：计算X加/减/乘/除Y"
            yield f"data: ❌ {tool_result}\n\n"
            yield {"tool_result": tool_result}

        # 调用工具
        num1 = float(num1.strip())
        num2 = float(num2.strip())
        tool_result = calculate.invoke({"num1": num1, "num2": num2, "operation": operation})
        yield f"data: ✅ 工具调用结果：{tool_result}\n\n"
    except Exception as e:
        tool_result = f"工具调用失败：{str(e)}"
        yield f"data: ❌ {tool_result}\n\n"

    yield {"tool_result": tool_result}


async def answer_node(state: AgentState) -> Dict[str, Any]:
    """回答节点：生成最终回答"""
    yield f"data: 📝 开始生成最终回答...\n\n"
    await asyncio.sleep(1)

    # 构建回答提示
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个乐于助人的助手，根据思考过程和工具结果回答用户问题"),
        ("user", "问题：{question}\n思考过程：{thought}\n工具结果：{tool_result}\n请给出简洁清晰的回答")
    ])

    # 生成回答
    chain = prompt | llm
    response = await chain.ainvoke({
        "question": state.question,
        "thought": state.thought,
        "tool_result": state.tool_result
    })
    answer = response.content
    yield f"data: 🎯 最终回答：{answer}\n\n"

    yield {"answer": answer}


# --------------------------
# 6. 定义LangGraph路由函数
# --------------------------
def should_call_tool(state: AgentState) -> str:
    """路由函数：决定下一步执行工具节点还是直接回答节点"""
    return "tool_node" if "需要调用计算工具" in state.thought else "answer_node"


# --------------------------
# 7. 构建LangGraph图
# --------------------------
def build_agent_graph() -> CompiledStateGraph:
    """构建Agent的状态图"""
    graph = StateGraph(AgentState)

    # 添加节点
    graph.add_node("think_node", think_node)
    graph.add_node("tool_node", tool_node)
    graph.add_node("answer_node", answer_node)

    # 设置起始节点
    graph.set_entry_point("think_node")

    # 添加边（路由）
    graph.add_conditional_edges(
        "think_node",
        should_call_tool,
        {
            "tool_node": "tool_node",
            "answer_node": "answer_node"
        }
    )

    # 工具节点执行完后到回答节点
    graph.add_edge("tool_node", "answer_node")

    # 回答节点执行完后结束
    graph.add_edge("answer_node", END)

    return graph.compile()


# 编译Agent图
agent_graph = build_agent_graph()


# --------------------------
# 8. 定义FastAPI SSE接口
# --------------------------
class AgentRequest(BaseModel):
    """请求体模型"""
    question: str


async def agent_sse_generator(question: str) -> Generator[str, None, None]:
    """SSE生成器：流式返回Agent执行过程"""
    # 初始化状态
    initial_state = AgentState(question=question)

    # 执行Agent图并流式返回结果
    async for event in agent_graph.astream(initial_state):
        # event是节点执行结果，这里我们直接返回节点中的流式输出
        for node_name, node_output in event.items():
            if isinstance(node_output, Generator):
                async for chunk in node_output:
                    yield chunk


@app.post("/agent/chat/sse")
async def agent_chat_sse(request: AgentRequest):
    """Agent聊天SSE接口：流式返回思考、工具调用、回答过程"""
    return StreamingResponse(
        agent_sse_generator(request.question),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"  # 禁用nginx缓冲，确保流式输出
        }
    )


# --------------------------
# 9. 启动服务
# --------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)