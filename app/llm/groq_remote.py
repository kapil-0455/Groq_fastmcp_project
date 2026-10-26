from openai import OpenAI
from app import config

client = OpenAI(
    api_key=config.GROQ_API_KEY,
    base_url='https://api.groq.com/openai/v1',
)


def ask_remote(question: str) -> str:
    resp = client.responses.create(
        model=config.GROQ_MODEL,
        input=question,
        tools=[{
            'type': 'mcp',
            'server_label': 'my_tools',
            'server_url': config.MCP_PUBLIC_URL,
            'require_approval': 'never',
            # 'allowed_tools': ['add', 'get_weather'],
            # 'headers': {'Authorization': 'Bearer <token>'},
        }],
    )
    return resp.output_text
