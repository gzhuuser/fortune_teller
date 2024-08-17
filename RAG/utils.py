from typing import Dict, Any
from modelscope import snapshot_download
from Knowledge import KnowledgeBase

# 下载模型并得到模型在本地存储的路径
model_dir = snapshot_download("AI-ModelScope/bge-large-zh-v1.5", revision="master")
instruction = "为这个句子生成表示以用于检索相关文章"

# 初始化并加载知识库
knowledge_base = KnowledgeBase(model_dir, instruction)
knowledge_base.load_knowledge("./RAG/data/knowledge_embeddings_with_indices.pkl")

# ------------------上面这一部分必须要在使用下面的函数前预先加载好
# knowledge_embeddings_with_indices.pkl已经是处理好的向量数据了,到时候直接使用load_knowledge加载即可


def rag_matching(input_data: Dict[str, str], knowledge_base: Any, topk: int = 1) -> str:
    """
    根据输入的掌纹特征，通过知识库匹配相关的知识。

    参数:
    input_data (Dict[str, str]): 包含掌纹线特征的字典，每个键代表一种掌纹线（如感情线、生命线等），值为对应的描述。
    knowledge_base (Any): 预加载的知识库对象，用于匹配查询。
    topk (int): 指定每个掌纹线特征返回的最相关知识片段的数量。

    返回:
    str: 包含每种掌纹线的相关知识的字符串。
    """

    # 构建查询字典
    queries_dict = {
        "感情线": input_data.get("感情线", ""),
        "生命线": input_data.get("生命线", ""),
        "智慧线": input_data.get("智慧线", ""),
        "婚姻线": input_data.get("婚姻线", ""),
        "事业线": input_data.get("事业线", ""),
    }

    # 最终结果字符串
    result_str = ""

    # 依次进行匹配并拼接结果
    for key, query in queries_dict.items():
        if query:
            matches = knowledge_base.match_query([query], top_k=topk)
            result_str += f"{key}的相关的知识:\n"
            for match in matches[0]:  # matches[0] 因为只有一个query
                text = match[0]
                result_str += f"  相关知识: {text.strip()}\n"
            result_str += "\n"

    return result_str.strip()


# 使用示例:
if __name__ == "__main__":
    input_data = {
        "感情线": "较长,弯曲,较深,无分叉",
        "生命线": "中等长度,弧形,深",
        "智慧线": "较长,直线,浅,末端分叉",
        "婚姻线": "两条,一条较长,一条较短,弯曲",
        "事业线": "较长,直线,深",
    }

    result = rag_matching(input_data, knowledge_base)
    print(result)
