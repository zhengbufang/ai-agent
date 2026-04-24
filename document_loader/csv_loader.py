from langchain_community.document_loaders.csv_loader import CSVLoader

# source_column
# 参数指定文件加载的列，保存在source变量中。
# csv_loader = CSVLoader(file_path="C:\\Users\\zhengbufang\\Desktop\\11.csv",
#                        source_column='姓名')
csv_loader = CSVLoader(file_path="C:\\Users\\zhengbufang\\Desktop\\11.csv",)
doc = csv_loader.load()
print(doc)

# for item in doc:
#     print(item.page_content)
#     print("=======================")