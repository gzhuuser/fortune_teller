from transformers import AutoTokenizer, AutoModelForCausalLM, TextIteratorStreamer
import torch
from threading import Thread
from modelscope import snapshot_download

# 定义一个函数，用于下载和加载模型
def download_and_load_model(
    model_name="IEITYuan/Yuan2-2B-Mars-hf", cache_dir="./", torch_dtype=torch.bfloat16
):
    # 下载模型到本地缓存目录
    model_dir = snapshot_download(model_name, cache_dir=cache_dir)
    path = f"{cache_dir}/{model_name}"  # 定义模型路径

    # 创建tokenizer
    print("Creating tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(
        path, add_eos_token=False, add_bos_token=False, eos_token="<eod>"
    )

    # 添加自定义的特殊token
    tokenizer.add_tokens(
        [
            "<sep>",
            "<pad>",
            "<mask>",
            "<predict>",
            "<FIM_SUFFIX>",
            "<FIM_PREFIX>",
            "<FIM_MIDDLE>",
            "<commit_before>",
            "<commit_msg>",
            "<commit_after>",
            "<jupyter_start>",
            "<jupyter_text>",
            "<jupyter_code>",
            "<jupyter_output>",
            "<empty_output>",
        ],
        special_tokens=True,
    )

    # 创建并加载预训练模型
    print("Creating model...")
    model = AutoModelForCausalLM.from_pretrained(
        path, torch_dtype=torch_dtype, trust_remote_code=True
    ).cuda()

    return tokenizer, model.eval()  # 返回加载好的tokenizer和model，并设置模型为评估模式


# 获取并加载模型和tokenizer的函数
def get_model():
    return download_and_load_model()


# 定义一个函数，用于生成回复（非流式）
def generate_response(tokenizer, model, messages, max_length=1024):
    # 将所有对话消息拼接成一个字符串，作为模型输入的提示语
    prompt = "<n>".join(msg["content"] for msg in messages) + "<sep>"
    inputs = tokenizer(prompt, return_tensors="pt")[
        "input_ids"
    ].cuda()  # 将输入文本编码为张量并加载到GPU上
    outputs = model.generate(inputs, do_sample=False, max_length=max_length)  # 生成回复
    output = tokenizer.decode(outputs[0])  # 将生成的输出张量解码为文本
    response = output.split("<sep>")[-1].replace("<eod>", "")  # 提取回复内容，并去除结束标志

    return response


# 定义一个函数，用于生成流式回复
def generate_stream_response(tokenizer, model, messages, max_length=1024):
    streamer = TextIteratorStreamer(tokenizer)  # 创建一个流式输出的迭代器
    prompt = "<n>".join(msg["content"] for msg in messages) + "<sep>"  # 将所有对话消息拼接成一个字符串
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")  # 将输入文本编码为张量并加载到GPU上
    generation_kwargs = dict(
        inputs, streamer=streamer, max_new_tokens=max_length
    )  # 设置生成参数
    thread = Thread(target=model.generate, kwargs=generation_kwargs)  # 在一个独立线程中异步生成回复
    thread.start()  # 启动生成线程
    generated_text = ""
    count = 0

    # 流式输出生成的内容
    for new_text in streamer:
        generated_text += new_text  # 累积生成的文本
        if "<sep>" in generated_text:
            generated_text = generated_text.split("<sep>")[-1]  # 分离最后一段生成的有效文本
        if "<eod>" in generated_text:
            generated_text = generated_text.replace("<eod>", "")  # 去除结束标志
        count += 1
        if count % 8 == 0:
            yield generated_text  # 每8个新文本单元输出一次
            generated_text = ""  # 清空已输出的内容，避免重复输出
    yield generated_text  # 输出剩余的内容


if __name__ == "__main__":
    # 加载model和tokenizer
    tokenizer, model = get_model()

    # 获取用户输入
    text = input("请输入内容：")

    # 定义对话消息列表
    messages = [
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "你好，有什么我可以帮你的吗？"},
        {"role": "user", "content": text},
    ]

    # 提示开始生成流式回复
    print("-" * 30 + "生成流式回复" + "-" * 30)

    # 调用流式回复生成函数
    response = generate_stream_response(tokenizer, model, messages)

    # 实时输出流式生成的回复内容
    for stream in response:
        print(stream, end="", flush=True)

    print("\n" + "-" * 30 + "流式回复结束" + "-" * 30)  # 提示流式回复生成结束
