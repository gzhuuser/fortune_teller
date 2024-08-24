import os
import io
import base64
from PIL import Image
from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
from MLLM.pic2url import pic2url  # 导入相关库
from MLLM.MMML import MMML
from MLLM.preprocess import preprocess_hand_image
from RAG.utils import rag_matching
from RAG.Knowledge import KnowledgeBase
from modelscope import snapshot_download
from LLM.model import get_model, generate_response, generate_stream_response

app = Flask(__name__)
CORS(app)  # 允许所有来源

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
    # 取消上下文
    history = []
    data = request.json

    text = data.get("text")
    image_data = data.get("image")  # 应该是一个base64编码的图像
    feature = data.get("feature")

    if image_data:
        try:
            # 将base64编码的图像转换为PIL图像
            image = Image.open(io.BytesIO(base64.b64decode(image_data)))
            image_path = "./uploaded_image.jpg"
            image.save(image_path)
            preprocess_hand_image(image_path)
            # 使用初始化的模型处理图像
            cloud_url = pic2url(image_path)
            MMML_res = MMML(cloud_url)
            RAG_res = rag_matching(MMML_res, knowledge_base, feature, topk=1)

            content = PROMPT.format(
                MMML_res=MMML_res[feature], RAG_res=RAG_res, user_input=text
            )
            history.append({"role": "user", "content": content})
            system_response = generate_response(tokenizer, model, history)
            history.append({"role": "system", "content": system_response})

            return (
                jsonify({"status": 200, "statusText": "OK", "body": system_response}),
                200,
            )
        except Exception as e:
            print(str(e))
            return (
                jsonify(
                    {
                        "status": 500,
                        "statusText": f"Internal Server Error: {str(e)}",
                        "body": None,
                    }
                ),
                500,
            )
    else:
        return (
            jsonify(
                {
                    "status": 400,
                    "statusText": "Bad Request: No image uploaded",
                    "body": None,
                }
            ),
            400,
        )


@app.route("/v2", methods=["POST"])
def process_input_v2():
    global history  # 使用全局历史记录变量
    history = []
    data = request.json

    text = data.get("text")
    image_data = data.get("image")  # 获取Base64编码的图像数据
    feature = data.get("feature")

    if image_data:
        try:
            # 将Base64编码的图像转换为PIL图像
            image = Image.open(io.BytesIO(base64.b64decode(image_data)))
            image_path = "./uploaded_image.jpg"
            image.save(image_path)
            print("Image saved to", image_path)
            preprocess_hand_image(image_path)

            # 使用初始化的模型处理图像
            cloud_url = pic2url(image_path)
            MMML_res = MMML(cloud_url)
            RAG_res = rag_matching(MMML_res, knowledge_base, feature, topk=1)

            content = PROMPT.format(
                MMML_res=MMML_res[feature], RAG_res=RAG_res, user_input=text
            )
            history.append({"role": "user", "content": content})

            def generate():
                try:
                    for response in generate_stream_response(tokenizer, model, history):
                        yield response
                except Exception as e:
                    print(f"Error during stream response generation: {str(e)}")
                    raise e

            return Response(
                stream_with_context(generate()),
                content_type="text/plain",
                headers={
                    "status": 200,
                    "statusText": "OK",
                },
            )
        except Exception as e:
            print("Error occurred:", str(e))
            return (
                jsonify(
                    {
                        "status": 500,
                        "statusText": f"Internal Server Error: {str(e)}",
                        "body": None,
                    }
                ),
                500,
            )
    else:
        return (
            jsonify(
                {
                    "status": 400,
                    "statusText": "Bad Request: No image uploaded",
                    "body": None,
                }
            ),
            400,
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6006, debug=False)
