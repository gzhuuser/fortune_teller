import openai
from openai import OpenAI
import os
from typing import Dict, List, Optional, Tuple, Union

"""
定制Prompt模板
"""
PROMPT_TEMPLATE = dict(
    RAG_PROMPT_TEMPALTE="""
        帮我完成一个数据扩展任务,接下来你会收到一个格式如下的数据:
        topic,feature,describe
        
        你要完成的任务是:
        1. 根据topic,feature 以及现有的describe来扩充数据集,主要是扩充describe部分
        2. 扩充的结果以json的形式返回
        3. 返回的中文要改为简体
        4. 控制describe的字数,不要超过200字
        
        数据: {topic},{feature},{describe}

        返回的格式:
        {{
            "topic": 有五个选项,分别是感情线,生命线,智慧线,婚姻线,事业线。你需要根据topic的值来完成这一部分的填充
            "feature": 基于已有的feature适当扩充,
            "describe": 将扩充的describe填写在这里
        }}
        """
)


class BaseModel(object):
    def __init__(self, path: str = ""):
        self.path = path

    def chat(self, prompt: str, history: Optional[List[dict]] = None, **args) -> str:
        pass

    def load_model(self):
        pass


class OpenAIChatModel(BaseModel):
    def __init__(self, path: str = "", model: str = "gpt-3.5-turbo-0125"):
        """
        :param path:
        :param model: 传入gpt模型
        """
        super().__init__(path)
        self.model = model
        self.client = OpenAI()  # 初始化OpenAI客户端
        self.client.api_key = os.getenv("OPENAI_API_KEY")
        self.client.base_url = os.getenv("OPENAI_BASE_URL")

    def chat(self, prompt: str, history: Optional[List[dict]] = None, **args) -> str:
        if history is None:
            history = []
        # 格式化 Prompt 模板
        formatted_prompt = PROMPT_TEMPLATE["RAG_PROMPT_TEMPALTE"].format(**args)
        history.append({"role": "user", "content": formatted_prompt})
        response = self.client.chat.completions.create(
            model=self.model, messages=history, max_tokens=500, temperature=0.1
        )
        return response.choices[0].message.content

    def load_model(self):
        pass  # 因为OpenAI使用的是API，因此这里无需加载模型
