import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.environ['GROQ_API_KEY']
GROQ_MODEL = os.getenv('GROQ_MODEL', 'openai/gpt-oss-120b')
MCP_PUBLIC_URL = os.getenv('MCP_PUBLIC_URL', '')
