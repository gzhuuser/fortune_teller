import http.client
import json
import re
import os


def MMML(url):
    key = os.getenv("key")
    base_url = os.getenv("base_url")
    conn = http.client.HTTPSConnection(base_url)
    payload = json.dumps(
        {
            "model": "gpt-4o",
            "stream": False,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "描述一下这个掌纹感情线，生命线，智慧线，婚姻线，事业线,格式按照 **感情线**：内容\n给出,最后一行给出掌纹不科学",
                        },
                        {"type": "image_url", "image_url": {"url": url}},
                    ],
                }
            ],
            "temperature": 0.9,
            "max_tokens": 400,
        }
    )
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {key}",
        "User-Agent": "Apifox/1.0.0 (https://apifox.com)",
        "Content-Type": "application/json",
    }
    conn.request("POST", "/v1/chat/completions", payload, headers)
    res = conn.getresponse()
    data = res.read()
    # 得到返回的数据
    data = json.loads(data.decode("utf-8"))
    # 提取内容
    content = data["choices"][0]["message"]["content"]
    # 使用正则表达式提取每条掌纹后的文本
    patterns = {
        "生命线": r"\*\*生命线\*\*：(.*?)\n",
        "智慧线": r"\*\*智慧线\*\*：(.*?)\n",
        "感情线": r"\*\*感情线\*\*：(.*?)\n",
        "婚姻线": r"\*\*婚姻线\*\*：(.*?)\n",
        "事业线": r"\*\*事业线\*\*：(.*?)\n",
    }

    # 初始化一个字典来存储提取的内容
    palm_lines = {}

    # 遍历每条掌纹的模式并提取内容
    for line_name, pattern in patterns.items():
        match = re.search(pattern, content, re.S)
        if match:
            palm_lines[line_name] = match.group(1).strip()
        else:
            palm_lines[line_name] = "未提及"

    # 打印提取结果
    print(json.dumps(palm_lines, ensure_ascii=False, indent=2))

    # 返回字典格式的提取结果
    return palm_lines


if __name__ == "__main__":
    result = MMML(
        "https://image-bed-datawhale.oss-cn-beijing.aliyuncs.com/test/myhand.png"
    )
    print(result)  # 打印字典格式的结果
