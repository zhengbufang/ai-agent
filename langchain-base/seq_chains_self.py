from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains import LLMChain
from langchain_openai import ChatOpenAI
from model import get_model

from langchain_classic.chains import SimpleSequentialChain



model = get_model()

prompt_first = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个股票基金分析师"),
        ("human", "请你尽可能详细的解释一下：{knowledge}"),
    ]
)

chainA_chains = LLMChain(llm=model,
prompt=prompt_first,
verbose=True
)



from langchain_core.prompts import ChatPromptTemplate

chainB_template = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个总结师"),
        ("human", "{question}请根据上述的回答，用一句话总结"),
    ]
)

chainB_chains = LLMChain(llm=model,prompt=chainB_template,verbose=True)

# 在chains参数中，按顺序传入LLMChain A 和LLMChain B
full_chain = SimpleSequentialChain(chains=[chainA_chains, chainB_chains], verbose=True)

# 在这个过程中，因为 SimpleSequentialChain 定义的是顺序链，所以在 chains 参数中传递的列表要按照
# 顺序来进行传入，即LLMChain A 要在LLMChain B之前。同时，在调用时，不再使用LLMChain A中定
# 义的 {knowledge} 参数，也不是LLMChainB中定义的 {description} 参数，而是要使用 input 进行变
# 量的传递。

invoke = full_chain.invoke({"input": "你觉得2026年那些基金板块适合入手？"})
print(invoke)

