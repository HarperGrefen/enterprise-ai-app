import os
from dotenv import load_dotenv
import yaml

class Config:
    def __init__(self):
        # 加载.env文件
        load_dotenv()
        # 加载dev.yaml配置
        with open("configs/dev.yaml", "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)
    
    def get(self, key: str, default=None):
        """获取配置，支持点分隔符，如llm.ak"""
        # 先从环境变量(.env)找
        env_key = key.replace(".", "_").upper()
        if os.getenv(env_key):
            return os.getenv(env_key)
        # 再从yaml配置找
        parts = key.split(".")
        value = self.config
        for part in parts:
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                return default
        return value

# 全局单例
config = Config()