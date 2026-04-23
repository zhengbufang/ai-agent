import uuid

from langchain_core.stores import InMemoryBaseStore
from langgraph.store.memory import InMemoryStore

#内存的短期记忆
memory_story = InMemoryStore()


#put 三个参数
#命名空间（元组） 作为记忆的逻辑分组机制，建议以用户标识符和记忆类别（“user_123","chat_history"）

# 键（字符串） 标记命名空间内记忆条目的唯一标识符。

# 值（dict） 用户数据  例如用户姓名等

namespace = ("user_info","user_id")

key = uuid.uuid4()

value = {"name":"郑不凡","age":20,"gender":1}

#保存记忆
memory_story.put(namespace, key, value)

print(memory_story.get(namespace,key).value)