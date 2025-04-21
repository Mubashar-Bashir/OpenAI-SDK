# Start of Selection
import os # os level env variable accessible
from dotenv import load_dotenv # .env file loader
from agents import Agent, Runner, AsyncOpenAI , OpenAIChatCompletionsModel, set_tracing_disabled
# from openai import AsyncOpenAI 
from agents.run import RunConfig
import asyncio

# Load the environment variables from the .env file
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = os.getenv('BASE_URL')
MODEL = os.getenv("MODEL")

# Check if the API key is present; if not, raise an error
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY is not set. Please ensure it is defined in your .env file.")

#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url=BASE_URL,
)
set_tracing_disabled(disabled=True)
async def main():
    # This agent will use the custom LLM provider
    agent = Agent(
        name="Assistant",
        instructions="You only respond in haikus.",
        model=OpenAIChatCompletionsModel(model=MODEL, openai_client=external_client),
    )

    result = await Runner.run(
        agent,
        "Tell me about recursion in programming.",
    )
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
