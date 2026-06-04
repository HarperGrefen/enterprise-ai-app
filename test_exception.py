# 让Python能找到src
import sys
import os
sys.path.append(os.path.dirname(__file__))

# 导入我们写的异常
from src.common.exceptions import LLMException

# 测试抛出异常
raise LLMException("测试大模型异常")