import asyncio
import os

import dotenv
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from model import get_model
from langchain_core.documents import Document


# async def only_llm(user_question:str):
#     model = get_model()
#     template = """
#     用户问题 {user_input}
#     请用一句话总结
#     """
#
#     prompt = PromptTemplate.from_template(template=template)
#     chain = prompt | model
#
#     async for chunk in chain.astream({"user_input":user_question}):
#         print(chunk.content,flush=True,end="")

# 外挂RAG功能 从向量检索数据并给大模型参考回答
async def rag_llm(user_question:str):
    model = get_model()
    template = """
    已知知识：{knowledge}
    用户问题:{user_input}
    请用一句话总结
    """
    # data = await get_rag_data(user_question)

    data = await get_rag_data_v2(user_question)

    prompt = PromptTemplate.from_template(template=template)
    chain = prompt | model
    async for chunk in chain.astream({"user_input":user_question,"knowledge":data}):
        print(chunk.content,flush=True,end="")

async def get_rag_data(user_question) -> str:
    document = Document(
        page_content="湖南新冠接种系统是深圳三代人科技有限公司在2021年开发上线的。",
    )
    document2 = Document(
        page_content="北京新冠接种系统是河北世创在2025年和沈苏共同开发上线的。",
    )

    document_4 = Document(
        page_content=" 医疗保健：降低处方药价格，扩大医疗保险覆盖范围。",
    )
    document_5 = Document(
        page_content="教育：提供免费的社区大学教育。。",
    )
    document_6 = Document(
        page_content="科技：增加对半导体产业的投资以减少对外国供应链的依赖。。",
    )
    document_7 = Document(
        page_content="外交政策：继续支持乌克兰对抗俄罗斯的侵略。",
    )
    document_8 = Document(
        page_content="枪支管制：呼吁国会通过更严格的枪支管制法律。",
    )
    document_9 = Document(
        page_content="移民改革：提出全面的移民改革方案。",
    )
    document_10 = Document(
        page_content="社会正义：承诺解决系统性种族歧视问题。",
    )
    documents = [
        document,
        document2,
        document_4,
        document_5,
        document_6,
        document_7,
        document_8,
        document_9,
        document_10
    ]
    ai_embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    #得提前向量好，只需通过问题查向量  不是通过程序去向量数据然后再查询  这里知识演示露出
    # 生产这里应该换成真实部署的向量数据库 而且得提前向量好，只需通过问题查向量 这不是这种集成的内存向量数据库Chroma
    db = Chroma.from_documents(documents, ai_embeddings, persist_directory="./chroma_db_rag")
    search = db.similarity_search(user_question, k=3)
    print("向量召回数量：",len(search))
    return search[0].page_content

async def get_rag_data_v2(user_question) -> str:
    # 文件加载成文档
    loader = TextLoader(file_path="D:\\pythoncode\\ai-agent\\vector\\llm\\rag.txt", encoding="utf-8")
    doc = loader.load()
    # 文档切成块
    spliter = RecursiveCharacterTextSplitter(chunk_size=100,chunk_overlap=0)
    spit_doc = spliter.split_documents(doc)

    # 嵌入模型
    ai_embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    #向量数据库 向量化
    db = Chroma.from_documents(spit_doc, ai_embeddings, persist_directory="./chroma_db_rag")

    # 向量查询 返回前三条
    # search = db.similarity_search(user_question, k=3)
    search = db.similarity_search(
        query=user_question,k=3
    )
    print("向量召回数量：",len(search))
    if len(search) > 0:
        return search[0].page_content
    return ""

if __name__ == "__main__":
    dotenv.load_dotenv()
    os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY1")
    os.environ['OPENAI_BASE_URL'] = os.getenv("OPENAI_BASE_URL")
    # asyncio.run(rag_llm("深圳三代人在2021年做了什么？"))  两个方法都能正确检索出来

    asyncio.run(rag_llm("人工智能是什么？"))   #大模型没有用向量召回得数据  而且召回得数据不准


