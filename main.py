from utils.Knowledge import KnowledgeBase


model_dir = "AI-ModelScope/bge-large-zh-v1.5"
instruction = "为这个句子生成表示以用于检索相关文章"

knowledge_base = KnowledgeBase(model_dir, instruction)

# 示例知识文本
text = [
    """
    五大掌紋分析：
    
    婚姻線：反映婚姻狀況，但不等同於婚姻次數。
    感情線：揭示一個人的情感狀態和愛情運勢。
    智慧線：反映思維能力和學習心態。
    生命線：象徵健康狀況和生活熱情，而非壽命長短。
    事業線/命運線：象徵事業運勢和人生方向，並不完全等同於財富。
    """,
    """
    手相分析的五大原則：
    
    慣用手：反映一個人的意識層面和當前的生活狀況。
    非慣用手：代表潛意識層面和先天性格。
    左右手的比較：可以解讀不同的意義，顯示一個人是否在改變現狀。
    掌紋方向：平行掌紋如婚姻線、感情線、智慧線和生命線，以及垂直掌紋如事業線，各自代表不同的運勢和影響力。
    """,
    """
    四種手形與人格特質：
    
    大地型手掌：踏實負責，但有時固執。
    火型手掌：外向熱情，喜歡冒險，但易衝動。
    空氣型手掌：聰明且善於社交，但易走極端。
    水型手掌：敏感、創意豐富，但容易情緒化。
    """,
    """
    手相常見問題：
    
    斷掌代表個性鮮明，與過去的迷思不同。
    雙手靈活的人可通過手相分析潛在意識。
    婚姻線不能直接反映婚姻次數或子女數量。
    事業線紋路深長不一定代表高收入，而是對人生方向的滿意度。
    生命線並不代表壽命，而是要了解情緒和生活態度。
    """,
    """
    手相的基本概念：手相學已有四千多年的歷史，透過觀察手掌和掌紋的形狀來判斷一個人的性格、生活狀態和未來運勢。
    """,
]

# 预处理并保存知识库
# knowledge_base.preprocess_knowledge(text, "knowledge_embeddings_with_indices.pkl")

# 加载知识库
knowledge_base.load_knowledge("knowledge_embeddings_with_indices.pkl")

# 进行查询并匹配
queries = ["命运线：浅显。"]
matches = knowledge_base.match_query(queries, top_k=2)

print("匹配结果：")
for query, match in zip(queries, matches):
    print(f"Query: {query}")
    for text, score, idx in match:
        print(f"  Matched Text: {text}, Score: {score}, Original Index: {idx}")
