import asyncio

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate

from model import get_model

model = get_model()

async def more_chat_model(question="你是谁"):
    prompt = ChatPromptTemplate.from_messages([
        ("system","你是一个通用助手"),
        ("user","{question}"),
    ])
    while True:
        chain = prompt | model
        response = []
        async for chunk in chain.astream({"question":question}):
            response.append(chunk.content)
            print(chunk.content,end="",flush=True)

        print("\n")
        user_input = input("请输入你的问题(按q退出): ")
        if user_input == "q":
            break

        #核心 把大模型回答的问题追加到提示词,然后再问大模型
        prompt.append(AIMessage(content=str(response)))
        prompt.append(HumanMessage(content=user_input))

if __name__ == "__main__":
    asyncio.run(more_chat_model(question="说说公积金"))