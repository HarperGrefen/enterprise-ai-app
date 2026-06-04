import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.llm.doubao_client import doubao_client

if __name__ == "__main__":
    print("正在调用豆包大模型...")
    try:
        response = doubao_client.chat("用一句话介绍Python")
        print("\n✅ 大模型回复:")
        print(response)
    except Exception as e:
        print(f"\n❌ 错误: {e}")