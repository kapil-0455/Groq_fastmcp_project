import json
from fastmcp import Client
from groq import AsyncGroq
from app import config
from app.mcp_server.server import mcp

groq = AsyncGroq(api_key=config.GROQ_API_KEY)


async def ask_local(question: str) -> str:
    # In-memory transport. Use Client('http://localhost:8000/mcp-server/mcp')
    # to go through the running HTTP endpoint instead.
    async with Client(mcp) as mcp_client:
        mcp_tools = await mcp_client.list_tools()
        tools = [
            {
                'type': 'function',
                'function': {
                    'name': t.name,
                    'description': t.description or '',
                    'parameters': t.inputSchema,
                },
            }
            for t in mcp_tools
        ]

        messages = [{'role': 'user', 'content': question}]

        while True:
            resp = await groq.chat.completions.create(
                model=config.GROQ_MODEL,
                messages=messages,
                tools=tools,
                tool_choice='auto',
            )
            msg = resp.choices[0].message
            messages.append(msg)

            if not msg.tool_calls:
                return msg.content or ''

            for call in msg.tool_calls:
                args = json.loads(call.function.arguments or '{}')
                result = await mcp_client.call_tool(call.function.name, args)
                messages.append({
                    'role': 'tool',
                    'tool_call_id': call.id,
                    'content': result.content[0].text,
                })
