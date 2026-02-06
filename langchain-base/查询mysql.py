# ChatPromptTemplate示例
from langchain_classic.chains.sql_database.query import create_sql_query_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_classic.chains import LLMChain

from model import get_model

model = get_model()

# 连接 MySQL 数据库
db_user = "root"
db_password = "123456" #根据自己的密码填写
db_host = "127.0.0.1"
db_port = "3306"
db_name = "ssm_sms"


# mysql+pymysql://用户名:密码@ip地址:端口号/数据库名
db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")
print("哪种数据库：", db.dialect)
print("获取数据表：", db.get_usable_table_names())
# 执行查询
# res = db.run("SELECT count(*) FROM tb_admin;")
# print("查询结果：", res)

# create_sql_query_chain，SQL查询链，是创建生成SQL查询的链，用于将 自然语言 转换成 数据库的SQL查询

chain = create_sql_query_chain(llm=model, db=db)
response = chain.invoke({"question": "姓名为admin的密码是多少？", "table_names_to_use":
["tb_admin"]})
print(response)
