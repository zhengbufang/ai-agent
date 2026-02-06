# SemanticChunking（语义分块）是 LangChain 中一种更高级的文本分割方法，它超越了传统的基于字
# 符或固定大小的分块方式，而是根据 文本的语义结构 进行智能分块，使每个分块保持 语义完整性 ，从而
# 提高检索增强生成(RAG)等应用的效果。
import os

import dotenv
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings

with open("C:\\Users\\zhengbufang\\Desktop\\新建文本文档 (2).txt",encoding="utf-8") as f:
    local_text = f.read()

os.environ['OPENAI_API_KEY'] = "sk-4399942285ba4508bdb43a3534bb45aa"
os.environ['OPENAI_BASE_URL'] = "https://dashscope.aliyuncs.com/compatible-mode/v1"

dotenv.load_dotenv()

embed_model = OpenAIEmbeddings(
    model="text-embedding-v4"
)

text_splitter = SemanticChunker(
    embeddings=embed_model,
    breakpoint_threshold_type="percentile",#断点阈值类型：字面值["百分位数", "标准差", "四分位距", "梯度"] 选其一
    breakpoint_threshold_amount=65.0 #断点阈值数量 (极低阈值 → 高分割敏感度)
)

docs = text_splitter.create_documents(texts = [local_text])
print(len(docs))
for doc in docs:
    print(doc)
    print("-"*100)