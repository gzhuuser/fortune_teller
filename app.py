import os
import io
import base64
import numpy as np
from PIL import Image
from flask import Flask, request, jsonify, Response, stream_with_context
from threading import Thread
from MLLM.pic2url import pic2url  # 导入相关库
from MLLM.MMML import MMML
from RAG.utils import rag_matching
from RAG.Knowledge import KnowledgeBase
from modelscope import snapshot_download
from LLM.model import get_model, generate_response, generate_stream_response

app = Flask(__name__)

# 设置环境变量
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
    tokenizer, model = get_model()
    return knowledge_base, model, tokenizer


knowledge_base, model, tokenizer = init()


@app.route("/v1", methods=["POST"])
def process_input():
    global history  # 使用全局历史记录变量
    data = request.json

    text = data.get("text")
    image_data = data.get("image")  # 应该是一个base64编码的图像
    feature = data.get("feature")

    if image_data:
        # 将base64编码的图像转换为PIL图像
        image = Image.open(io.BytesIO(base64.b64decode(image_data)))
        image_path = "./uploaded_image.jpg"
        image.save(image_path)

        # 使用初始化的模型处理图像
        cloud_url = pic2url(image_path)
        MMML_res = MMML(cloud_url)
        RAG_res = rag_matching(MMML_res, knowledge_base, feature, topk=1)
        print(RAG_res)

        content = PROMPT.format(
            MMML_res=MMML_res[feature], RAG_res=RAG_res, user_input=text
        )
        history.append({"role": "user", "content": content})
        system_response = generate_response(tokenizer, model, history)
        history.append({"role": "system", "content": system_response})

        return jsonify({"response": system_response})
    else:
        history.append({"role": "user", "content": text})
        history.append({"role": "assistant", "content": "No image uploaded"})
        return jsonify({"response": "No image uploaded"})


@app.route("/v2", methods=["POST"])
def process_input_v2():
    global history  # 使用全局历史记录变量
    data = request.json

    text = data.get("text")
    image_data = data.get("image")  # 获取Base64编码的图像数据
    feature = data.get("feature")
    if image_data:
        # 将Base64编码的图像转换为PIL图像
        image = Image.open(io.BytesIO(base64.b64decode(image_data)))
        image_path = "./uploaded_image.jpg"
        image.save(image_path)

        # 使用初始化的模型处理图像
        cloud_url = pic2url(image_path)
        MMML_res = MMML(cloud_url)
        RAG_res = rag_matching(MMML_res, knowledge_base, feature, topk=1)

        content = PROMPT.format(
            MMML_res=MMML_res[feature], RAG_res=RAG_res, user_input=text
        )
        history.append({"role": "user", "content": content})

        # 使用流式响应生成回复
        def generate():
            for response in generate_stream_response(tokenizer, model, history):
                yield response

        return Response(stream_with_context(generate()), content_type="text/plain")

    else:
        history.append({"role": "user", "content": text})
        history.append({"role": "assistant", "content": "No image uploaded"})
        return jsonify({"response": "No image uploaded"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6006)
