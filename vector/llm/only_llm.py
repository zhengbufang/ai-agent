import asyncio

from langchain_core.prompts import PromptTemplate
from model import get_model

async def only_llm(user_question:str):
    model = get_model()
    template = """
    用户问题 {user_input}
    请用一句话总结
    """

    prompt = PromptTemplate.from_template(template=template)
    chain = prompt | model

    async for chunk in chain.astream({"user_input":user_question}):
        print(chunk.content,flush=True,end="")

if __name__ == "__main__":
    asyncio.run(only_llm("北京有什么建筑？"))


