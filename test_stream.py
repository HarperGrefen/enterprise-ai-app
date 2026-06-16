import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.llm.doubao_client import doubao_client

if __name__ == "__main__":
    print("=== 流式输出测试 ===")
    print("\n🤖 豆包: ", end="", flush=True)
    
    # 调用流式接口
    for chunk in doubao_client.chat_stream("请用3句话介绍一下什么是人工智能"):
        print(chunk, end="", flush=True)
    
    print("\n")
    
    print("=== 多轮流式输出测试 ===")
    print("\n👤 你: 我叫小明")
    print("🤖 豆包: ", end="", flush=True)
    for chunk in doubao_client.chat_with_history_stream("我叫小明"):
        print(chunk, end="", flush=True)
    
    print("\n\n👤 你: 我叫什么名字？")
    print("🤖 豆包: ", end="", flush=True)
    for chunk in doubao_client.chat_with_history_stream("我叫什么名字？"):
        print(chunk, end="", flush=True)
    
    print("\n")