"""
Configuration file for deployment
"""
import os

# API Base URL - 根据部署环境自动设置
# 本地开发：http://localhost:5001
# 生产环境：从环境变量读取，或使用相对路径
API_BASE_URL = os.environ.get('API_BASE_URL', 'http://localhost:5001')

# 如果是生产环境且没有设置 API_BASE_URL，使用相对路径
if os.environ.get('FLASK_ENV') == 'production' and API_BASE_URL == 'http://localhost:5001':
    API_BASE_URL = ''  # 使用相对路径，同域名

