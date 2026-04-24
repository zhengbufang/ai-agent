# 将文本向量化之后，下一步就是进行向量的存储。这部分包含两块：
# 向量的存储 ：将非结构化数据向量化后，完成存储
# 向量的查询 ：查询时，嵌入非结构化查询并检索与嵌入查询“最相似”的嵌入向量。即具有相似性检索能力
import os

import dotenv
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

dotenv.load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY1")
os.environ['OPENAI_BASE_URL'] = os.getenv("OPENAI_BASE_URL")

#用Chroma数据库示例  内存模式

pdf_loader = PyPDFLoader(file_path="C:\\Users\\zhengbufang\\Desktop\\new\\智能化学生信息管理系统_简洁报告.pdf",)

splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", "。", "！", "？", "……", "，", ""], chunk_size=100,
                                          keep_separator=True,chunk_overlap=5)
document = pdf_loader.load_and_split(splitter)

ai_embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

#举例01
# db = Chroma.from_documents(document, ai_embeddings)
# # 查询：使用相似度查找
# query = "时间范围是多少？"
# docs = db.similarity_search(query)
# print(docs[0].page_content)

#    注意：Chroma主要有两种存储模式： 内存模式 和 持久化模式 。当使用persist_directory参数时，数据
#    会保存到指定目录；如果没有指定，则默认使用内存存储。

#举例02
db_path = "./chroma_db"
db_vector = Chroma.from_documents(document, ai_embeddings, persist_directory=db_path)
query = "时间范围是多少？"
docs = db_vector.similarity_search(query)
print(docs[0].page_content)

