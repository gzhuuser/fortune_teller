from typing import Dict, Any
from modelscope import snapshot_download
from RAG.Knowledge import KnowledgeBase


def rag_matching(
    input_data: Union[Dict[str, str], str], knowledge_base: Any, feature: str = None, topk: int = 1
) -> str:
    """
    根据输入的掌纹特征，通过知识库匹配相关的知识。

    参数:
    input_data (Union[Dict[str, str], str]): 如果是字典，包含掌纹线特征，每个键代表一种掌纹线（如感情线、生命线等），值为对应的描述。如果是字符串，则直接作为查询内容。
    knowledge_base (Any): 预加载的知识库对象，用于匹配查询。
    feature (str): 当输入为字符串时，指定其对应的特征名。
    topk (int): 指定每个掌纹线特征返回的最相关知识片段的数量。

    返回:
    str: 包含每种掌纹线的相关知识的字符串。
    """

    if isinstance(input_data, str):
        # 输入是字符串，直接作为查询
        queries_dict = {feature: input_data}
    elif isinstance(input_data, dict):
        # 输入是字典，使用输入的键值对
        queries_dict = {key: input_data.get(key, "") for key in input_data}
    else:
        raise ValueError("input_data 必须是字符串或字典类型")

    # 最终结果字符串
    result_str = ""

    # 依次进行匹配并拼接结果
    for key, query in queries_dict.items():
        if query:
            matches = knowledge_base.match_query([query], top_k=topk)
            result_str += f"用户的{key}特征:\n"
            for match in matches[0]:  # matches[0] 因为只有一个query
                text = match[0]
                result_str += f"{text.strip()}\n"
            result_str += "\n"

    return result_str.strip()