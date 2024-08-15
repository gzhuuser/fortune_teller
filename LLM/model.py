from transformers import AutoTokenizer, AutoModelForCausalLM, TextIteratorStreamer
import torch
from threading import Thread
from modelscope import snapshot_download


# 定义一个函数，用于下载和加载模型
def download_and_load_model(model_name='IEITYuan/Yuan2-2B-Mars-hf', cache_dir='./', torch_dtype=torch.bfloat16):
    # 下载模型
    model_dir = snapshot_download(model_name, cache_dir=cache_dir)
    # 定义模型路径
    path = f'{cache_dir}/{model_name}'

    # 创建tokenizer
    print("Creating tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(path, add_eos_token=False, add_bos_token=False, eos_token='<eod>')
    tokenizer.add_tokens(['<sep>', '<pad>', '<mask>', '<predict>', '<FIM_SUFFIX>', '<FIM_PREFIX>', '<FIM_MIDDLE>',
                          '<commit_before>', '<commit_msg>', '<commit_after>', '<jupyter_start>', '<jupyter_text>',
                          '<jupyter_code>', '<jupyter_output>', '<empty_output>'], special_tokens=True)

    # 创建model
    print("Creating model...")
    model = AutoModelForCausalLM.from_pretrained(path, torch_dtype=torch_dtype, trust_remote_code=True).cuda()
    
    return tokenizer, model.eval()


def get_model():
    return download_and_load_model()


# 定义一个函数，用于生成回复
def generate_response(tokenizer, model, messages, max_length=1024):
    prompt = "<n>".join(msg["content"] for msg in messages) + "<sep>"  # 拼接对话历史
    inputs = tokenizer(prompt, return_tensors="pt")["input_ids"].cuda()
    outputs = model.generate(inputs, do_sample=False, max_length=max_length)  # 设置解码方式和最大生成长度
    output = tokenizer.decode(outputs[0])  # 定义对话消息列表
    response = output.split("<sep>")[-1].replace("<eod>", '')

    return response


# 定义一个函数，用于生成流式回复
def generate_stream_response(tokenizer, model, messages, max_length=1024):
    streamer = TextIteratorStreamer(tokenizer)
    prompt = "<n>".join(msg["content"] for msg in messages) + "<sep>"  # 拼接对话历史
    inputs = tokenizer(prompt, return_tensors="pt").to('cuda')
    generation_kwargs = dict(inputs, streamer=streamer, max_new_tokens=max_length)
    thread = Thread(target=model.generate, kwargs=generation_kwargs)
    thread.start()
    generated_text = ""
    count = 0

    # 流式输出
    for new_text in streamer:
        generated_text += new_text
        if "<sep>" in generated_text:
            generated_text = generated_text.split("<sep>")[-1]
        if "<eod>" in generated_text:
            generated_text = generated_text.replace("<eod>", '')
        count += 1
        if count % 8 == 0:
            yield generated_text
    yield generated_text


if __name__ == "__main__":
    # 加载model和tokenizer
    tokenizer, model = get_model()
    # 定义对话消息列表
    messages = [
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "你好，有什么我可以帮你的吗？"},
        {"role": "user", "content": "写一个python的Hello World程序"}
    ]
    # 生成回复
    response = generate_response(tokenizer, model, messages)
    print("Assistant:", response)
    # 生成流式回复
    print("-"*30 + "生成流式回复" + "-"*30)
    response = generate_stream_response(tokenizer, model, messages)
    for stream in response:
        import os
        os.system("clear")
        print(stream, flush=True)