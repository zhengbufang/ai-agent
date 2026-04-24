from langchain_community.document_loaders import TextLoader

text_loader = TextLoader(file_path="C:\\Users\\zhengbufang\\Desktop\\新建文本文档.txt", encoding="utf-8")

# page_content：真正的文档内容
# metadata：文档内容的原数据
doc = text_loader.load()
# for e in doc:
#     print(e.page_content)
print(doc)
