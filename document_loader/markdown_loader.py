from langchain_community.document_loaders import UnstructuredMarkdownLoader

# pip install markdown
markdown_loader = UnstructuredMarkdownLoader(
    file_path="#",
    mode="elements",
    strategy="fast"
)

docs = markdown_loader.load()
print(len(docs)) # 16
# 4.打印
for doc in docs:
    print(doc)

