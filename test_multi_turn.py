import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.llm.doubao_client import doubao_client

if __name__ == "__main__":
    print("=" * 50)
    print("🤖 豆包多轮对话助手")
    print("✅ 输入任意内容开始对话，大模型会记住上下文")
    print("🔄 输入 clear 清空对话历史")
    print("🚪 输入 exit 退出程序")
    print("=" * 50)

    while True:
        # 获取用户输入
        user_input = input("\n👤 你: ").strip()
        
        # 处理退出指令
        if user_input.lower() in ["exit", "quit", "q"]:
            print("\n👋 再见！")
            break
        
        # 处理清空历史指令
        if user_input.lower() == "clear":
            doubao_client.clear_history()
            print("✅ 对话历史已清空")
            continue
        
        # 跳过空输入
        if not user_input:
            continue
        
        # 调用大模型多轮对话
        try:
            print("🤖 豆包: ", end="", flush=True)
            response = doubao_client.chat_with_history(user_input)
            print(response)
        except Exception as e:
            print(f"\n❌ 错误: {e}")