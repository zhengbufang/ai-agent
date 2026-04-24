import os

import dotenv
from langchain_community.document_loaders import UnstructuredMarkdownLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
# 从“向量存储组件”的代码实现中可以看到，向量数据库本身已经包含了实现召回功能的函数方法
# ( similarity_search )。该函数通过计算原始查询向量与数据库中存储向量之间的相似度来实现召回。
# LangChain还提供了 更加复杂的召回策略 ，这些策略被集成在Retrievers（检索器或召回器）组件中。
# Retrievers（检索器）是一种用于从大量文档中检索与给定查询相关的文档或信息片段的工具。检索器
dotenv.load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY1")
os.environ['OPENAI_BASE_URL'] = os.getenv("OPENAI_BASE_URL")

# 1 加载文档 转换为document对象
# loader = TextLoader(file_path='09-ai1.txt',encoding="utf-8")
# docs = loader.load()
#
# # 2 切分文档 document
# spit = RecursiveCharacterTextSplitter(chunk_size=100,chunk_overlap=0)
# documents = spit.split_documents(docs)
#
# # 3 定义嵌入模型
# ai_embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
#
# #4 将文档存储到向量数据库中
# db = Chroma.from_documents(documents,ai_embeddings,
#                                        persist_directory="./chroma_db_retriever")
#5.从向量数据库中得到检索器  Retriever 一般和 VectorStore 配套实现，通过 as_retriever() 方法获取。
# 注意只会返回满足阈值分数的文档，不会获取文档的得分。如果想查询文档的得分是否满足阈值，可以
# 使用向量数据库的 similarity_search_with_relevance_scores 查看

# retriever = db.as_retriever(search_kwargs={#这里设置返回的文档数
#                                            "score_threshold": 0.1},
#                             search_type="similarity_score_threshold")
# #6.使用检索器检索
# invoke = retriever.invoke("经济政策？")
# print(len(docs))
# for doc in docs:
#     print(f"⭐{doc}")


# 2.定义文档
document_1 = Document(
    page_content="经济复苏：美国经济正在从疫情中强劲复苏，失业率降至历史低点。！",
)
document_2 = Document(
    page_content="基础设施：政府将投资1万亿美元用于修复道路、桥梁和宽带网络。",
)
document_3 = Document(
    page_content="气候变化：承诺到2030年将温室气体排放量减少50%。",
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
    document_1,
    document_2,
    document_3,
    document_4,
    document_5,
    document_6,
    document_7,
    document_8,
    document_9,
    document_10
]
ai_embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
db = Chroma.from_documents(documents,ai_embeddings,persist_directory="./chroma_db_retriever_v2")
# docs_with_scores = db.similarity_search_with_relevance_scores("经济政策")
# for doc, score in docs_with_scores:
#     print(f"\n相似度分数: {score:.4f}")
#     print(f"📌 内容: {doc.page_content}")
retriever = db.as_retriever(search_kwargs={#这里设置返回的文档数
                                               "score_threshold": 0.1},
                                search_type="similarity_score_threshold")
docs = retriever.invoke("经济政策？")
for doc in docs:
    print(f"⭐{doc}")

