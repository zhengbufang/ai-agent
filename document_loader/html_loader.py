from langchain_community.document_loaders import UnstructuredHTMLLoader

html_loader = UnstructuredHTMLLoader(
    file_path="#",
    mode="elements",
    strategy="fast"
)

docs = html_loader.load()
print(len(docs)) # 16
# 4.打印
for doc in docs:
    print(doc)

