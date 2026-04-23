from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from pydantic import BaseModel, Field
from trustcall import create_extractor

from model import get_model

#trustcall 支持从LLM输出中，高效提取符合预定义模式（pydantic,/JSON Schema）的结构化数据，确保记忆数据的类型安全与一致性

class UserProfile(BaseModel):
    username: str =Field(description="用户的首选姓名")
    inter: list[str] = Field(description="用户的兴趣列表")

model = get_model()

trustcall = create_extractor(model,
                 tools=[UserProfile], #将pydantic模式作为工具传递
                 tool_choice="UserProfile") #强制TrustCall 使用UserProfile 工具进行输出

conversation = [HumanMessage(content="嗨喽，我是Bob,请问你是那位"),
                AIMessage(content="Bob你好，我是你的AI助手小deepseek"),
                HumanMessage(content="deepseek你好，很高兴认识你,我喜欢足球和网球，你了"),
                AIMessage(content="噢耶，我喜欢篮球和乒乓球")]

prompt = "从以下对话中，提取用户资料信息"
result = trustcall.invoke({"messages":[SystemMessage(content=prompt)]+conversation})
print(result["responses"][0])

#输出 username='Bob' inter=['足球', '网球']
