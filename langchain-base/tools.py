import BaseModel
from langchain.tools import tool
from pydantic import BaseModel,Field

@tool
def add_number(num1, num2):
    """
    两个数加法运算
    """
    return num1 + num2
print(f"name = {add_number.name}")
print(f"args = {add_number.args}")
print(f"description = {add_number.description}")
print(f"return_direct = {add_number.return_direct}")


#大模型根据描述来判断是否需要调用该函数  会以刑参数描述的为准
@tool(name_or_callable="add_number",description="整数加法运算")
def add_number_v2(num1, num2):
    """
        两个数加法运算
     """
    return num1 + num2

print("======================================================")
print(f"name = {add_number_v2.name}")
print(f"args = {add_number_v2.args}")
print(f"description = {add_number_v2.description}")
print(f"return_direct = {add_number_v2.return_direct}")

add_number_v2.invoke({"num1":1,"num2":3})


class FiledInfo(BaseModel):
    num1: int = Field(description="第一个参数")
    num2: int = Field(description="第二个参数")

#大模型根据描述来判断是否需要调用该函数  会以刑参数描述的为准
@tool(name_or_callable="add_number",description="整数加法运算",
      args_schema=FiledInfo,return_direct=True)
def add_number_v3(num1, num2):
    """
        两个数加法运算
     """
    return num1 + num2

print("======================================================")
print(f"name = {add_number_v3.name}")
print(f"args = {add_number_v3.args}")
print(f"description = {add_number_v3.description}")
print(f"return_direct = {add_number_v3.return_direct}")

print(add_number_v3.invoke({"num1":3,"num2":5}))


