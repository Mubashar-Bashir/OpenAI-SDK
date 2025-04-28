from agents import Agent, Runner, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from dotenv import load_dotenv, find_dotenv
import os

_:bool = load_dotenv(find_dotenv())

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
 #Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

# config = RunConfig(
#     model=model,
#     model_provider=external_client,
#     tracing_disabled=True
# )
greeting_agent:Agent = Agent(
    name= "Greeting_Agent",
    instructions = "Give Greetings to Agent",
    model= model
    
)


def main():
    print("Hello from console-agent!")
    user_input = input("ENter Text here ...!!")
    response=Runner.run_sync(
        starting_agent= greeting_agent,
        input=user_input
         
    )

if __name__ == "__main__":
    main()
