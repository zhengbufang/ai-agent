from langchain_text_splitters import CharacterTextSplitter

# text = """
# LangChain 是一个用于开发由语言模型驱动的应用程序的框架的。它提供了一套工具和抽象，使开发者
# 能够更容易地构建复杂的应用程序。
# """

# 3.定义字符分割器
# splitter = CharacterTextSplitter(
#     chunk_size=50, # 每块大小
#     chunk_overlap=0,# 块与块之间的重复字符数
#     #length_function=len,
#     separator="" # 设置为空字符串时，表示禁用分隔符优先
# )



# separator优先原则：当设置了 separator （如"。"），分割器会首先尝试在分隔符处分割，然后再考
    # 虑 chunk_size。这是为了避免在句子中间硬性切断。这种设计是为了：
    # 1. 优先保持语义完整性（不切断句子）
    # 2. 避免产生无意义的碎片（如半个单词/不完整句子）
    # 3. 如果 chunk_size 比片段小，无法拆分片段，导致 overlap失效。
text = "这是一个示例文本啊。我们将使用CharacterTextSplitter将其分割成小块。分割基于字符数。"
#指定分隔符分割
splitter = CharacterTextSplitter(
    chunk_size=20, # 每块大小
    chunk_overlap=0,# 块与块之间的重复字符数
    #length_function=len,
    separator="。" # 设置为空字符串时，表示禁用分隔符优先
)

texts = splitter.split_text(text)

# 5.打印结果
for i, chunk in enumerate(texts):
    print(f" 长度：{len(chunk)}")
    print(chunk)
    print("-" * 50)

