import TextLoader
import dotenv
import os
from langchain.agents import create_agent
from langchain_chroma.vectorstores import Chroma
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.retrievers import BaseRetriever
from langchain_core.tools import create_retriever_tool
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from model import get_model

dotenv.load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY1")
os.environ['OPENAI_BASE_URL'] = os.getenv("OPENAI_BASE_URL")



from langchain_tavily import TavilySearch

def get_tavily_search():
    # 定义 AVILY_KEY 密钥
    os.environ["TAVILY_API_KEY"] = "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"
    # 查询 Tavily 搜索 API
    return TavilySearch(max_results=1)

def get_retriever() -> BaseRetriever:
    # 文件加载成文档
    loader = TextLoader(file_path="D:\\pythoncode\\ai-agent\\vector\\llm\\rag.txt", encoding="utf-8")
    doc = loader.load()
    # 文档切成块
    spliter = RecursiveCharacterTextSplitter(chunk_size=100,chunk_overlap=0)
    spit_doc = spliter.split_documents(doc)

    # 嵌入模型
    ai_embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    #向量数据库 向量化
    db = Chroma.from_documents(spit_doc, ai_embeddings, persist_directory="./chroma_db_agent")
    return db.as_retriever()


# 封装通用逻辑
def get_model_with_tools():
    # 创建一个工具来检索文档
    retriever =  get_retriever()
    retriever_tool = create_retriever_tool(
        retriever=retriever,
        name="wiki_search",
        description="搜索维基百科",
    )

    # 定义工具
    tools = [get_tavily_search(), retriever_tool]

    # 获取大模型
    model = get_model()

    # 提示词模板
    prompt = ChatPromptTemplate.from_messages(
        [("system", "你是通用助手，善于总结回答，请以简短精确得总结对用于回答的内容"), ("human", "{question}")])

    # 绑定工具
    return prompt | model.bind_tools(tools)

# 没有用agent的情况 工具得手动调用 大模型只是给返回需要调用得
async def no_agent_invoke():
    # 绑定工具
    model_with_tools  = get_model_with_tools()
    response = model_with_tools.invoke({"question": "今天上海天气怎么样"})
    print(f"ContentString: {response.content}")
    print(f"ToolCalls: {response.tool_calls}")

    # 我们可以看到现在没有内容，但有一个工具调用！它要求我们调用Tavily
    # Search工具。
    # 这并不是在调用该工具，只是告诉我们要调用。为了实际调用它，我们将创建我们的Agent程序。

def agent_invoke():
    # model_with_tools = get_model_with_tools()
    # 创建一个工具来检索文档
    retriever = get_retriever()
    retriever_tool = create_retriever_tool(
        retriever=retriever,
        name="wiki_search",
        description="获取接种相关信息",
    )

    # 定义工具
    tools = [get_tavily_search(), retriever_tool]

    # 获取大模型
    model = get_model()

    # 提示词模板
    # 注意：agent_scratchpad必须声明，它用于存储和传递Agent的思考过程。比如，在调用链式工具时
    # （如先搜索天气再推荐行程）， agent_scratchpad
    # 保留所有历史步骤，避免上下文丢失。format方法
    # 会将intermediate_steps转换为特定格式的字符串，并赋值给agent_scratchpad变量。如果不传递
    # intermediate_steps参数，会导致KeyError: 'intermediate_steps'
    # 错误。
    prompt = ChatPromptTemplate.from_messages(
        [("system", "你是通用助手，善于总结回答，请以简短精确得总结对用于回答的内容"),
         ("human", "{question}"),
         ("placeholder", "{agent_scratchpad}")])
    # 现在，我们可以在几个查询上运行Agent！请注意，目前这些都是无状态查询（它不会记住先前的交
    # 互）。

    # agent = create_tool_calling_agent(model, tools, prompt)
    # agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    # invoke = agent_executor.invoke("湖南新冠接种系统是哪个公司开发得？")
    # print(invoke) 会报错

    prompt = SystemMessage(content="你是通用助手，善于总结回答，请以简短精确得总结对用于回答的内容")
    agent = create_agent(
        model=model,
        tools=tools,  # All tools pre-registered
        system_prompt= prompt
    )

    result = agent.invoke({"messages": [HumanMessage("湖南新冠接种系统是哪个公司开发得")]})
    print(result)


if __name__ == "__main__":
    # asyncio.run(no_agent_invoke())
    agent_invoke()





