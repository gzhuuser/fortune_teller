from typing import Dict, Any
from modelscope import snapshot_download
from RAG.Knowledge import KnowledgeBase


def rag_matching(
    input_data: Dict[str, str], knowledge_base: Any, feature, topk: int = 1
) -> str:
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
