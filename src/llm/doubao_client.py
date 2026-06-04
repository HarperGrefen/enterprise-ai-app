import os
from dotenv import load_dotenv
from volcenginesdkarkruntime import Ark
from src.common.exceptions import LLMException

load_dotenv(override=True)

class DoubaoClient:
    def __init__(self):
        self.client = Ark(
            ak=os.getenv("VOLC_AK"),
            sk=os.getenv("VOLC_SK"),
            region="cn-beijing"
        )
        self.model = os.getenv("VOLC_ENDPOINT_ID")
        # 新增：对话历史上下文
        self.messages = []

    def chat(self, prompt: str) -> str:
        """单轮对话（不保留历史）"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1024
            )
            return response.choices[0].message.content
        except Exception as e:
            raise LLMException(f"调用失败: {str(e)}")

    def chat_with_history(self, prompt: str) -> str:
        """多轮对话（保留历史上下文）"""
        try:
            # 添加用户消息到历史
            self.messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                temperature=0.7,
                max_tokens=1024
            )
            
            # 添加助手回复到历史
            assistant_message = response.choices[0].message.content
            self.messages.append({"role": "assistant", "content": assistant_message})
            
            return assistant_message
        except Exception as e:
            raise LLMException(f"多轮对话失败: {str(e)}")

    def clear_history(self):
        """清空对话历史"""
        self.messages = []

# 全局单例
doubao_client = DoubaoClient()