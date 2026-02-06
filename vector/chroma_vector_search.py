# 将文本向量化之后，下一步就是进行向量的存储。这部分包含两块：
# 向量的存储 ：将非结构化数据向量化后，完成存储
# 向量的查询 ：查询时，嵌入非结构化查询并检索与嵌入查询“最相似”的嵌入向量。即具有相似性检索能力
import os

import dotenv
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

dotenv.load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY1")
os.environ['OPENAI_BASE_URL'] = os.getenv("OPENAI_BASE_URL")

#用Chroma数据库示例  内存模式
# 2.定义文档
raw_documents = [
    Document(
        page_content="葡萄是一种常见的水果，属于葡萄科葡萄属植物。它的果实呈圆形或椭圆形，颜色有绿色、紫色、红色等多种。葡萄富含维生素C和抗氧化物质，可以直接食用或酿造成葡萄酒。",
        metadata={"source": "水果", "type": "植物"}
    ),
    Document(
        page_content="白菜是十字花科蔬菜，原产于中国北方。它的叶片层层包裹形成紧密的球状，口感清脆微甜。白菜富含膳食纤维和维生素K，常用于制作泡菜、炒菜或煮汤。",
        metadata={"source": "蔬菜", "type": "植物"}
    ),
    Document(
        page_content="狗是人类最早驯化的动物之一，属于犬科。它们具有高度社会性，能理解人类情绪，常被用作宠物、导盲犬或警犬。不同品种的狗在体型、毛色和性格上有很大差异。",
        metadata={"source": "动物", "type": "哺乳动物"}
    ),
    Document(
        page_content="猫是小型肉食性哺乳动物，性格独立但也能与人类建立亲密关系。它们夜视能力极强，擅长捕猎老鼠。家猫的品种包括波斯猫、暹罗猫等，毛色和花纹多样。",
        metadata={"source": "动物", "type": "哺乳动物"}
    ),
    Document(
        page_content="人类是地球上最具智慧的生物，属于灵长目人科。现代人类（智人）拥有高度发达的大脑，创造了语言、工具和文明。人类的平均寿命约70-80年，分布在全球各地。",
        metadata={"source": "生物", "type": "灵长类"}
    ),
    Document(
        page_content="太阳是太阳系的中心恒星，直径约139万公里，主要由氢和氦组成。它通过核聚变反应产生能量，为地球提供光和热。太阳活动周期约为11年，会影响地球气候。",
        metadata={"source": "天文", "type": "恒星"}
    ),
    Document(
        page_content="长城是中国古代的军事防御工程，总长度超过2万公里。它始建于春秋战国时期，秦朝连接各段，明朝大规模重修。长城是世界文化遗产和人类建筑奇迹。",
    metadata={"source": "历史", "type": "建筑"}
    ),
    Document(
        page_content="量子力学是研究微观粒子运动规律的物理学分支。它提出了波粒二象性、测不准原理等概念，彻底改变了人类对物质世界的认知。量子计算机正是基于这一理论发展而来。",
        metadata={"source": "物理", "type": "科学"}
    ),
    Document(
        page_content="《红楼梦》是中国古典文学四大名著之一，作者曹雪芹。小说以贾、史、王、薛四大家族的兴衰为背景，描绘了贾宝玉与林黛玉的爱情悲剧，反映了封建社会的种种矛盾。",
        metadata={"source": "文学", "type": "小说"}
    ),
    Document(
        page_content="新冠病毒（SARS-CoV-2）是一种可引起呼吸道疾病的冠状病毒。它通过飞沫传播，主要症状包括发热、咳嗽、乏力。疫苗和戴口罩是有效的预防措施。",
        metadata={"source": "医学", "type": "病毒"}
    )
]

ai_embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

db = Chroma.from_documents(raw_documents, ai_embeddings, persist_directory="./chroma_db_search")
# 相似性查询
# search = db.similarity_search("介绍下新冠病毒？",k=3)


# 直接对问题向量查询
# embedding_vector = ai_embeddings.embed_query("哺乳动物")
# search = db.similarity_search_by_vector(embedding_vector)


# 相似性检索，支持过滤元数据（filter）
search = db.similarity_search("哺乳动物",k=3,filter={"source":"动物"})

# 通过L2距离分数进行搜索 分数值越小，检索到的文档越和问题相似。分值取值范围：[0，正无穷]
# search = db.similarity_search_with_score(
#     "量子力学是什么?"
# )

# 通过余弦相似度分数进行搜索
# search = db._similarity_search_with_relevance_scores(
#     "量子力学是什么?"
# )

for search in search:
    print(search.page_content)
    print("-"* 30)

