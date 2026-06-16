import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.rag.document_loader import document_processor

if __name__ == "__main__":
    print("=== 文档加载与分割测试 ===")
    
    # 创建测试文档
    test_content = """
    什么是RAG？
    RAG的全称是检索增强生成（Retrieval-Augmented Generation）。
    它是一种结合了检索系统和生成式大模型的技术。
    
    RAG的工作流程是什么？
    1. 文档加载：读取各种格式的文档
    2. 文本分割：把长文档切成小块
    3. 向量存储：把文本块转换成向量
    4. 向量检索：找到最相关的文本块
    5. 生成回答：根据检索到的内容生成回答
    
    RAG有什么优点？
    1. 不需要微调大模型，成本低
    2. 可以随时更新知识库
    3. 回答有据可依，减少幻觉
    4. 可以处理私有数据
    """
    
    with open("test_rag.txt", "w", encoding="utf-8") as f:
        f.write(test_content)
    
    # 加载文档
    documents = document_processor.load_single_file("test_rag.txt")
    print(f"✅ 加载了 {len(documents)} 个文档")
    
    # 分割文档
    chunks = document_processor.split_documents(documents)
    print(f"✅ 分割成了 {len(chunks)} 个文本块")
    
    # 动态打印所有文本块（修复：不再硬编码索引）
    for i, chunk in enumerate(chunks):
        print(f"\n--- 第 {i+1} 个文本块 ---")
        print(chunk.page_content)
    
    # 清理测试文件
    os.remove("test_rag.txt")
    
    print("\n✅ 文档加载与分割测试通过！")