from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains import LLMChain
from langchain_openai import ChatOpenAI
from model import get_model

from langchain_classic.chains import SimpleSequentialChain



model = get_model()

chainA_template = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一位精通各领域知识的心理学家"),
        ("human", "请你尽可能详细的解释一下：{knowledge}"),
    ]
)

chainA_chains = LLMChain(llm=model,
prompt=chainA_template,
verbose=True
)

# invoke = chainA_chains.invoke({"knowledge": "30岁失业了为什么会焦虑？"})
# print(invoke)


from langchain_core.prompts import ChatPromptTemplate

chainB_template = ChatPromptTemplate.from_messages(
    [
        ("system", "你非常善于提取文本中的重要信息，并做出简短的总结"),
        ("human", "这是针对一个提问的完整的解释说明内容：{description}"),
        ("human", "请你根据上述说明，尽可能简短的输出重要的结论，请控制在20个字以内"),
    ]
)

chainB_chains = LLMChain(llm=model,prompt=chainB_template,verbose=True)

# 在chains参数中，按顺序传入LLMChain A 和LLMChain B
full_chain = SimpleSequentialChain(chains=[chainA_chains, chainB_chains], verbose=True)

# 在这个过程中，因为 SimpleSequentialChain 定义的是顺序链，所以在 chains 参数中传递的列表要按照
# 顺序来进行传入，即LLMChain A 要在LLMChain B之前。同时，在调用时，不再使用LLMChain A中定
# 义的 {knowledge} 参数，也不是LLMChainB中定义的 {description} 参数，而是要使用 input 进行变
# 量的传递。

invoke = full_chain.invoke({"input": "什么是langChain？"})
print(invoke)

