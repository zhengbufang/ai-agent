import asyncio

from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import  ChatPromptTemplate
from langchain_openai import ChatOpenAI

from model import get_model

# ChatPromptTemplate示例
model = get_model()


prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个程序语言大师"),
    ("user", "{question}"),
])

#使用format()
async def invoke_lcel():
    chat_template = ChatPromptTemplate.from_messages([
        ("system","你是一个{pro}"),
        ("user","{user_input}"),
    ])

    # 这种方式运行会报错
    # chat_template_2 = ChatPromptTemplate.from_messages([
    #     {"role":"system","content":"你是一个{pro}"},
    #     {"role":"user","content":"{input}"}
    # ])
    chain = chat_template | model
    async for chunk in chain.astream({"pro":"旅游攻略师","user_input":"分别说说甘孜和阿坝环线的区别"}):
        print(chunk.content,end="",flush=True)

async def invoke_prompt():
    messages = ChatPromptTemplate.from_messages([("system", "你是情绪疏导师"), ("human", "{question}")])

    chain = messages | model
    async for chunk in chain.astream({"question":"30岁搞Java开发，在2026年失业了如何合理安排利用时间,重新就业和缓解失业焦虑"}):
        print(chunk.content,end="",flush=True)

#使用format()
async def invoke_lcel_v2():
    chat_template = ChatPromptTemplate.from_messages([
        ("system","你是一个{pro}"),
        ("user","{user_input}"),
    ])

    # 用json会报错
    #json_parser = JsonOutputParser()

    str_parser = StrOutputParser()
    chain = chat_template | model | str_parser
    result = chain.invoke({"pro":"旅游攻略师","user_input":"分别说说甘孜和阿坝环线的区别"})
    print(result)
    print(type(result))

# async def llm_chain():
#     chat_template = ChatPromptTemplate.from_messages([
#         ("system","你是一个婚姻心理学专家"),
#         ("human","{question}")
#     ])
#     chain = LLMChain(llm=model,prompt=chat_template)
#     invoke = chain.invoke({"question": "为什么现在大量的单身，30岁还不结婚"})
#     print(invoke["text"])


if __name__ == '__main__':
    asyncio.run(invoke_prompt())