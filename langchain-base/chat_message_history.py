import asyncio

from langchain_classic.chains.conversation.base import ConversationChain
from langchain_classic.chains.llm import LLMChain
from langchain_classic.memory import ConversationBufferMemory, ConversationBufferWindowMemory, ConversationSummaryMemory
from langchain_core.messages import ChatMessage, BaseMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate

from model import get_model

model = get_model()


# 历史消息
async def test_chat_message_model():
    message = ChatMessageHistory()
    message.add_user_message("who are you")
    message.add_ai_message("what up?")
    print(message.messages)


# 历史消息 + llm
async def test_chat_message_model_v2() -> list[BaseMessage]:
    message = ChatMessageHistory()
    message.add_user_message("who are you")
    message.add_ai_message("what up?")
    invoke = model.invoke(message.messages)
    print(invoke.content)
    return message.messages

def chat_message_history():
    memory = ConversationBufferMemory(return_messages=True)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个通用助手"),
        MessagesPlaceholder(variable_name='history'),
        ("user", "{question}"), ])

    #初始化链
    chian = LLMChain(llm=model, prompt=prompt, memory=memory)
    res1 = chian.invoke({"question": "我的名字叫Tom"})
    print(res1,end="\n\n")

    res2 = chian.invoke({"question": "我刚刚问了什么"})
    print(res2, end="\n\n")

#对 ConversationBufferMemory 和 LLMChain 进行了封装
def conversation_chain():
    template = """
    以下是人类与AI之间的友好对话描述。AI表现得很健谈，并提供了大量来自其上下文的
    具体细节。如果AI不知道问题的答案，它会真诚地表示不知道。
    当前对话：
    {history}
    Human: {input}
    AI:
    """
    prompt = PromptTemplate.from_template(template)
    chain = ConversationChain(llm=model, prompt=prompt, verbose=True)
    chain.invoke({"input": "你好，你的名字叫小智"})
    chain.invoke({"input": "你好，你叫什么名字？"})

#{history} 保存上下文记忆变量
def conversation_window_memory():
    template = """
        以下是人类与AI之间的友好对话描述。AI表现得很健谈，并提供了大量来自其上下文的
        具体细节。如果AI不知道问题的答案，它会真诚地表示不知道。
        当前对话：
        {history}
        Human: {input}
        AI:
        """
    prompt = PromptTemplate.from_template(template)

    # k 表示记住几条
    memory = ConversationBufferWindowMemory(k=3)

    chain = LLMChain(llm=model, prompt=prompt, memory=memory,verbose=True)


    resut1 = chain.invoke(input="你是赵宇")

    # print(resut1)
    resut2 = chain.invoke(input="我好心累，找工作")
    # print(resut2)
    resut3 = chain.invoke(input="越长大越焦虑")

    resu4 = chain.invoke(input="我叫什么")
    print(resu4)


def conversation_chain_v2():
    conv_chain = ConversationChain(llm=model)
    resut1 = conv_chain.invoke(input="小明有1只猫")
    # print(resut1)
    resut2 = conv_chain.invoke(input="小刚有2只狗")
    # print(resut2)
    resut3 = conv_chain.invoke(input="小明和小刚一共有几只宠物?")
    print(resut3)

#对上文的是 LangChain 中一种 智能压缩对话历史 的记忆机制，它通过大语言模型(LLM)
#自动生成对话内容的 精简摘要 ，而不是存储原始对话文本。
def conversation_summary_memory():
    memory = ConversationSummaryMemory(llm=model)
    memory.save_context({"input": "你好"}, {"output": "怎么了"})
    memory.save_context({"input": "你是谁"}, {"output": "我是AI助手小智"})
    memory.save_context({"input": "初次对话，你能介绍一下你自己吗？"}, {"output": "当然可以了。我是一个无所不能的小智。"})

    # 5.读取消息（总结后的）
    print(memory.load_memory_variables({}))

    memory.save_context({"input":"短暂的休息正煎熬"},{"output": "为什么要这么说了"})
    print(memory.load_memory_variables({}))

if __name__ == '__main__':
    #chat_message_history()
    #conversation_chain()
    # conversation_chain_v2()
    #asyncio.run(test_chat_message_model_v2())
    #conversation_window_memory()
    conversation_summary_memory()

