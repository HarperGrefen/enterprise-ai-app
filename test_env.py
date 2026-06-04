import os
from dotenv import load_dotenv

# 强制加载当前目录的.env文件
load_dotenv(override=True)

# 打印所有环境变量
print("ARK_API_KEY:", os.getenv("ARK_API_KEY"))
print("ARK_BASE_URL:", os.getenv("ARK_BASE_URL"))
print("ARK_ENDPOINT_ID:", os.getenv("ARK_ENDPOINT_ID"))