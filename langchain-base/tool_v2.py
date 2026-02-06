from langchain_core.tools import StructuredTool
from pydantic import BaseModel,Field


class FieldInfo(BaseModel):
    query: str = Field(description="要检索的关键词")

def search_function(query: str):
    return "LangChain"

#StructuredTool.from_function 类方法提供了比 @tool 装饰器更多的可配置性，而无需太多额外的代码。
# search1 = StructuredTool.from_function(
#         func=search_function,
#         name="Search",
#         description="useful for when you need to answer questions about current events"
#     )


search1 = StructuredTool.from_function(
    func=search_function,
    name="Search",
    description="useful for when you need to answer questions about current events",
    args_schema=FieldInfo,
    return_direct=True,
)

print(f"name = {search1.name}")
print(f"description = {search1.description}")
print(f"args = {search1.args}")
search1.invoke("hello")