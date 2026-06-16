import os
import tiktoken  # 修复：添加缺失的tiktoken导入
from dotenv import load_dotenv
from volcenginesdkarkruntime import Ark
from src.common.exceptions import LLMException
from typing import Iterator

# 加载环境变量
load_dotenv(override=True)

class DoubaoClient:
    def __init__(self):
        # 初始化火山方舟客户端
        self.client = Ark(
            ak=os.getenv("VOLC_AK"),
            sk=os.getenv("VOLC_SK"),
            region="cn-beijing"
        )
        self.model = os.getenv("VOLC_ENDPOINT_ID")
        
        # 会话&记忆配置
        self.max_context_tokens = 28000
        self.default_session_id = "default"
        self.sessions = {
            self.default_session_id: []
        }

        # token计算器
        self.encoder = tiktoken.get_encoding("cl100k_base")

    # ✅ 新增：token计算私有方法（滑动窗口必需）
    def _count_tokens(self, messages: list) -> int:
        """计算消息列表的总token数"""
        total_tokens = 0
        for message in messages:
            # 每条消息基础开销：4个token
            total_tokens += 4
            # 消息内容的token数
            total_tokens += len(self.encoder.encode(message["content"]))
            # 角色的token数
            total_tokens += len(self.encoder.encode(message["role"]))
        # 每条回复基础开销：3个token
        total_tokens += 3
        return total_tokens

    # ✅ 新增：滑动窗口裁剪私有方法（滑动窗口必需）
    def _trim_context(self, messages: list) -> list:
        """滑动窗口裁剪上下文，确保总token数不超过上限"""
        # 如果当前长度已经在安全范围内，直接返回
        if self._count_tokens(messages) <= self.max_context_tokens:
            return messages
        
        # 否则，不断删除最早的消息，直到长度符合要求
        while self._count_tokens(messages) > self.max_context_tokens and len(messages) > 0:
            messages.pop(0)
        
        return messages

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

    # ✅ 修复：升级非流式多轮对话，支持多会话和滑动窗口
    def chat_with_history(self, prompt: str, session_id: str = None) -> str:
        """多轮对话（保留历史上下文，支持多会话）"""
        try:
            # 不传会话id则使用默认会话
            if session_id is None:
                session_id = self.default_session_id
            
            # 不存在该会话则新建空历史
            if session_id not in self.sessions:
                self.sessions[session_id] = []
            
            # 添加用户消息到历史
            self.sessions[session_id].append({"role": "user", "content": prompt})
            
            # 裁剪上下文，防止token超限
            self.sessions[session_id] = self._trim_context(self.sessions[session_id])
            
            # 调用大模型
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.sessions[session_id],
                temperature=0.7,
                max_tokens=1024
            )
            
            # 添加助手回复到历史
            assistant_message = response.choices[0].message.content
            self.sessions[session_id].append({"role": "assistant", "content": assistant_message})
            
            return assistant_message
        except Exception as e:
            raise LLMException(f"多轮对话失败: {str(e)}")

    # ✅ 修复：升级清空历史方法，支持清空指定会话
    def clear_history(self, session_id: str = None):
        """清空指定会话的对话历史"""
        if session_id is None:
            session_id = self.default_session_id
        
        if session_id in self.sessions:
            self.sessions[session_id] = []

    # ✅ 新增：单轮流式对话
    def chat_stream(self, prompt: str) -> Iterator[str]:
        """单轮流式对话（不保留历史）"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1024,
                stream=True  # 关键：开启流式输出
            )
            
            for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            raise LLMException(f"流式调用失败: {str(e)}")

    # ✅ 新增：多轮流式对话
    def chat_with_history_stream(self, prompt: str, session_id: str = None) -> Iterator[str]:
        """多轮流式对话（保留历史，支持多会话）"""
        try:
            if session_id is None:
                session_id = self.default_session_id
            
            if session_id not in self.sessions:
                self.sessions[session_id] = []
            
            # 添加用户消息到历史
            self.sessions[session_id].append({"role": "user", "content": prompt})
            
            # 裁剪上下文，防止token超限
            self.sessions[session_id] = self._trim_context(self.sessions[session_id])
            
            # 调用大模型流式接口
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.sessions[session_id],
                temperature=0.7,
                max_tokens=1024,
                stream=True  # 关键：开启流式输出
            )
            
            # 收集助手回复，用于保存到历史
            assistant_message = ""
            
            for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    assistant_message += content
                    yield content
            
            # 添加助手回复到历史
            self.sessions[session_id].append({"role": "assistant", "content": assistant_message})
                    
        except Exception as e:
            raise LLMException(f"多轮流式对话失败: {str(e)}")

    # ✅ 新增：获取所有会话ID
    def get_all_sessions(self) -> list:
        """获取所有会话ID"""
        return list(self.sessions.keys())

# 全局单例
doubao_client = DoubaoClient()