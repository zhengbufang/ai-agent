from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

text="LangChain框架特性\n\n多模型集成(GPT/Claude)\n记忆管理功能\n链式调用设计。文档分析场景示例：需要处理PDF/Word等格式。"

#举例1 一般chunk_size要调的比较大4000，避免切太碎会语义不连贯
# text_spit = RecursiveCharacterTextSplitter(chunk_size=30,
#                                chunk_overlap=0,
#                                 add_start_index=True)
#直接切分
# split_text = text_spit.split_text(text)
# for e in split_text:
#     print(e)
#     print("-------")

#举例 2 转化为document对象
# documents = text_spit.create_documents(split_text)
# for document in documents:
#     print(document)
#     print("-------")

#举例3：使用create_documents()方法演示，将本地文件内容加载成字符串，进行拆分

#  RecursiveCharacterTextSplitter：最常用
# 文档切分器中较常用的是 RecursiveCharacterTextSplitter (递归字符文本切分器) ，遇到 特定字符 时进行
# 分割。默认情况下，它尝试进行切割的字符包括 ["\n\n", "\n", " ", ""] 。
# 具体为：根据第一个字符进行切块，但如果任何切块太大，则会继续移动到下一个字符继续切块，以此
# 类推。
# 此外，还可以考虑添加，。等分割字符。
# 特点：
# 保留上下文：优先在自然语言边界（如段落、句子结尾）处分割， 减少信息碎片化 。

# with open("C:\\Users\\zhengbufang\\Desktop\\新建文本文档 (2).txt", encoding="utf-8") as f:
#     state_of_the_union = f.read() #返回的是字符串
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=100,
#                                chunk_overlap=20,
#                                length_function=len)
# texts = text_splitter.create_documents([state_of_the_union])
# for text in texts:
#     print(text.page_content)

# 举例4：使用split_documents()方法演示，利用PDFLoader加载文档，对文档的内容用递归切割器切割
# 2.定义PyPDFLoader加载器
# pdf_loader = PyPDFLoader(file_path="C:\\Users\\zhengbufang\\Desktop\\new\\智能化学生信息管理系统_简洁报告.pdf",)
# # 3.加载和切割文档对象
# docs = pdf_loader.load() # 返回Document对象构成的list
#
# # 4.定义切割器
# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=200,
#     chunk_overlap=0,
#     length_function=len,
#     add_start_index=True,
# )
#
# documents = text_splitter.split_documents(docs)
# for document in documents:
#     print(document.page_content)
#     print("-"*50)

# 举例 05 自定义分隔符
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=30,
    chunk_overlap=10, # 增加重叠字符
    separators=["\n\n", "\n", "。", "！", "？", "……", "，", ""], # 添加中文标点
    length_function=len,
    keep_separator=True #保留句尾标点（如 ……），避免切割后丢失语气和逻辑
)
split_text = text_splitter.split_text(text)
for e in split_text:
    print(e)
    print("====================")
