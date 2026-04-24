from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI


def get_model() -> BaseChatModel:
    return ChatOpenAI(
        temperature=0,
        model_name="glm-4-plus",
        # 填写密钥
        openai_api_key="86c1c5671f15f3676cb11e4a75197ebc.oJB2pL19OHIN7xOf",
        openai_api_base="https://open.bigmodel.cn/api/paas/v4/",
        max_tokens=100
    )