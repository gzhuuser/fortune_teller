import numpy as np
import os
from FlagEmbedding import FlagModel
import pickle


class KnowledgeBase:
    def __init__(self, model_dir, instruction, use_fp16=True):
        # 初始化模型
        self.model = FlagModel(
            model_dir, query_instruction_for_retrieval=instruction, use_fp16=use_fp16
        )
        self.knowledge_embeddings = None
        self.knowledge_texts = None
        self.index_mapping = None

    def preprocess_knowledge(self, texts, save_path):
        # 对前置知识进行编码并保存
        self.knowledge_texts = texts
        self.knowledge_embeddings = self.model.encode(texts)

        # 保存时将索引映射一并保存
        self.index_mapping = list(range(len(texts)))

        with open(save_path, "wb") as f:
            pickle.dump(
                (self.knowledge_texts, self.knowledge_embeddings, self.index_mapping), f
            )

        print(f"Knowledge embeddings and indices saved to {save_path}")

    def load_knowledge(self, load_path):
        # 加载预处理的知识向量及其对应的索引
        if os.path.exists(load_path):
            with open(load_path, "rb") as f:
                (
                    self.knowledge_texts,
                    self.knowledge_embeddings,
                    self.index_mapping,
                ) = pickle.load(f)
            print(f"Knowledge embeddings and indices loaded from {load_path}")
        else:
            raise FileNotFoundError(f"{load_path} not found")

    def match_query(self, queries, top_k=3):
        # 对查询进行编码并与知识向量进行匹配
        q_embeddings = self.model.encode_queries(queries)
        scores = q_embeddings @ self.knowledge_embeddings.T
        top_indices = np.argsort(-scores, axis=1)[:, :top_k]

        results = []
        for i, indices in enumerate(top_indices):
            matched_texts = [
                (self.knowledge_texts[idx], scores[i, idx], self.index_mapping[idx])
                for idx in indices
            ]
            results.append(matched_texts)
        return results
