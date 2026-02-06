from langchain_community.document_loaders.json_loader import JSONLoader

# jq_schema="." 直接提取完整的JSON对象（包括所有字段）
#保持原始 JSON 结构，将提取的数据转换为JSON字符串存入page_content字段中

# json_loader = JSONLoader(file_path="D:\\pythoncode\\ai-agent\\document_loader\\data.json"
#                          ,jq_schema=".",text_content=False)

#加载指定的json对象  https://docs.langchain.com/oss/python/integrations/document_loaders/json
# json_loader = JSONLoader(file_path="D:\\pythoncode\\ai-agent\\document_loader\\data.json"
#                          ,jq_schema=".items[].content_2",text_content=False)


#提取精确的对象
# 如果希望处理 JSON 中的 嵌套字段、数组元素提取，可以使用 content_key 配合
# is_content_key_jq_parsable=True ，通过 jq 语法精准定位目标数据。
# json_loader = JSONLoader(file_path="D:\\pythoncode\\ai-agent\\document_loader\\data_v2.json"
#                          ,jq_schema=".items[]", #先定位到数组条目
#                          content_key=".content", # 再从条目中提取 content 字段
#                          is_content_key_jq_parsable=True, # 用jq解析content_key
#                          text_content=False)

# items[].content[] 里的 title、content 和 其文本
# json_loader = JSONLoader(file_path="D:\\pythoncode\\ai-agent\\document_loader\\data_v2.json"
#                          ,jq_schema=".items[].content", #先定位到数组条目
#                          is_content_key_jq_parsable=True, # 用jq解析content_key
#                          text_content=False)

# items[].content[] 里的 title、content 和 其文本
json_loader = JSONLoader(file_path="D:\\pythoncode\\ai-agent\\document_loader\\data_v2.json"
                         ,jq_schema=".items[].content", #先定位到数组条目
                         content_key='.content_34',
                         is_content_key_jq_parsable=True, # 用jq解析content_key
                         )

doc = json_loader.load()
print(doc)

# for item in doc:
#     print(item.page_content)
#     print("=======================")