from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
import os
import dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter

dotenv.load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY1")
os.environ['OPENAI_BASE_URL'] = os.getenv("OPENAI_BASE_URL")
# 初始化嵌入模型
embeddings_model = OpenAIEmbeddings(model="text-embedding-ada-002")

#举例01
# text = "What was the name mentioned in the conversation?"
#
# # 生成一个嵌入向量
# embedded_query = embeddings_model.embed_query(text = text)
#
# # 使用embedded_query[:5]来查看前5个元素的值
# print(embedded_query[:5])
# print(len(embedded_query))


#举例 02 将一个文档向量化
#先加载文件转换为文档
pdf_loader = PyPDFLoader(file_path="C:\\Users\\zhengbufang\\Desktop\\new\\智能化学生信息管理系统_简洁报告.pdf",)
doc = pdf_loader.load()

# 文档切分
split = RecursiveCharacterTextSplitter()
documents = split.split_documents(doc)
print(len(documents))

# 文档切分后进行向量化
embed_documents = embeddings_model.embed_documents([doc.page_content for doc in documents])
# 表示的是每一个chrunk的embedding的维度
print(len(embed_documents))
print(len(embed_documents[0]))
print(embed_documents[0][:10])
