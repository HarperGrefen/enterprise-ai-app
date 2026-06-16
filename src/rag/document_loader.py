from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.common.exceptions import LLMException

class DocumentProcessor:
    def __init__(self):
        # 初始化文本分割器
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,  # 每个块的大小（字符数）
            chunk_overlap=50,  # 块之间的重叠部分，防止上下文断裂
            separators=["\n\n", "\n", "。", "！", "？", " ", ""],  # 分割优先级
            length_function=len
        )
    
    def load_single_file(self, file_path: str) -> list:
        """加载单个文档"""
        try:
            loader = TextLoader(file_path, encoding="utf-8")
            return loader.load()
        except Exception as e:
            raise LLMException(f"加载文档失败: {str(e)}")
    
    def load_directory(self, dir_path: str) -> list:
        """加载整个目录下的所有txt和md文档"""
        try:
            loader = DirectoryLoader(
                dir_path,
                glob="**/*.{txt,md}",  # 只加载txt和md文件
                loader_cls=TextLoader,
                loader_kwargs={"encoding": "utf-8"}
            )
            return loader.load()
        except Exception as e:
            raise LLMException(f"加载目录失败: {str(e)}")
    
    def split_documents(self, documents: list) -> list:
        """把文档分割成小块"""
        return self.text_splitter.split_documents(documents)

# 全局单例
document_processor = DocumentProcessor()