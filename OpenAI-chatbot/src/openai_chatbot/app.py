import os
import asyncio
import logging  # Import the logging module

from agents import Agent, Runner, function_tool, set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# BASE_URL= os.getenv('BASE_URL')
MODEL = os.getenv("MODEL") or 'gemini/gemini-2.0-flash-exp'
print('Selected LLM Model for this project >>> ', MODEL)
set_tracing_disabled(disabled=True)

# Check if the API key is present; if not, raise an error
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")
if not MODEL:
    raise ValueError("Model is not Selected")
# if not BASE_URL :
#    raise ValueError("BASE_URL is not selected")

@function_tool
def get_weather(city: str) -> str:
    print(f"[debug] getting weather for {city}")
    return f"The weather in {city} is sunny."

def main():
    # Initialize the agent
    agent = Agent(
        name="Assistant",
        instructions="You only respond in haikus.",
        tools=[get_weather],
        model=LitellmModel(model=MODEL, api_key=GEMINI_API_KEY),
    )

    # Run the agent with the input "What's the weather in Tokyo?"
    try:
        result = Runner.run_sync(
            starting_agent=agent, 
            input="What's the weather in Tokyo?")  # Corrected
        # Print the final output
        print(result.final_output)
    except Exception as e:
        logging.error(f"An error occurred: {e}")  # Log the error
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Start Generation Here
    # INSERT_YOUR_CODE
    main()
