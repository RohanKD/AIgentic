from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()
import asyncio
from videorag._llm import gemini_complete_if_cache


async def test_gemini():
    response = await gemini_complete_if_cache("gemini-2.0-flash", "Say hello!", )
    print(response)

asyncio.run(test_gemini())
