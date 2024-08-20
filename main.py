from MLLM.pic2url import pic2url
from MLLM.MMML import MMML
from RAG.utils import rag_matching
from RAG.Knowledge import KnowledgeBase
from modelscope import snapshot_download
from LLM.model import get_model, generate_response, generate_stream_response
import os
import numpy as np
from PIL import Image

os.environ["key"] = ""
os.environ["base_url"] = ""
os.environ["accessKeyId"] = ""
os.environ["accessKeySecret"] = ""

# 初始化历史记录
history = []

PROMPT = """
你是一个算命大师,你需要结合用户的手相特征和已知信息回答用户的问题

现在用户的手相特征如下:
---
{MMML_res}
---

目前已知的信息是:
---
{RAG_res}
---

用户的问题是:
---
{user_input}
---
"""


def init():
    # 下载模型并得到模型在本地存储的路径
    model_dir = snapshot_download(
        "AI-ModelScope/bge-large-zh-v1.5", cache_dir="./", revision="master"
    )
    instruction = "为这个句子生成表示以用于检索相关文章"
    # 初始化并加载知识库
    knowledge_base = KnowledgeBase(model_dir, instruction)
    knowledge_base.load_knowledge("./RAG/data/knowledge_embeddings_with_indices.pkl")
    # knowledge_base = None
    tokenizer, model = get_model()
    return knowledge_base, model, tokenizer


def process_input(text, image, knowledge_base, model, tokenizer):
    global history  # 使用全局历史记录变量

    if image is not None:
        # 将图像保存到本地
        image_path = "./uploaded_image.jpg"
        image_pil = Image.fromarray(image.astype(np.uint8))  # 将 numpy 数组转换为 PIL 图像
        image_pil.save(image_path)

        # 使用初始化的模型处理图像
        cloud_url = pic2url(image_path)
        MMML_res = MMML(cloud_url)
        RAG_res = rag_matching(MMML_res, knowledge_base, topk=1)
        print(RAG_res)
        # # 记录用户的输入

        content = PROMPT.format(MMML_res=MMML_res, RAG_res=RAG_res, user_input=text)
        history.append({"role": "user", "content": content})
        system_response = generate_response(tokenizer, model, history)
        # 记录系统的响应
        history.append({"role": "system", "content": system_response})

        return system_response
    else:
        # 记录用户的输入
        history.append({"role": "user", "content": text})
        # 记录系统的响应
        history.append({"role": "assistant", "content": "No image uploaded"})

        # 将历史记录合成为一个prompt
        prompt = "\n".join([f"{h['role']}: {h['content']}" for h in history])

        return f"Text: {text}\nNo image uploaded"


# 初始化模型和知识库
knowledge_base, model, tokenizer = init()


# 启动应用程序
if __name__ == "__main__":
    res = process_input("帮我分析一下手相", " ", knowledge_base, model, tokenizer)
    print(res)
