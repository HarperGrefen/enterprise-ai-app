# 自定义异常：专门标记大模型调用出错
class LLMException(Exception):
    pass