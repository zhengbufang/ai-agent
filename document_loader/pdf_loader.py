from langchain_community.document_loaders import PyPDFLoader

pdf_loader = PyPDFLoader(file_path="C:\\Users\\zhengbufang\\Desktop\\new\\智能化学生信息管理系统_简洁报告.pdf",)
doc = pdf_loader.load()
# print(doc)
print(type(doc[0]))
print(doc[0].metadata)
# for e in doc:
#     print(e.page_content)


#1.导入相关依赖
# 2.定义PyPDFLoader对象,加载在线的pdf文件
py_pdfLoader = PyPDFLoader(file_path="https://arxiv.org/pdf/2302.03803")
# 3.加载
docs = py_pdfLoader.load()
print(len(docs))
for doc in docs:
    print(doc)