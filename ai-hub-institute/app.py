import os
from dotenv import load_dotenv, find_dotenv
import chainlit as cl
from agents import Agent, Runner, set_tracing_disabled
from openai import AsyncOpenAI
from agents.extensions.models.litellm_model import LitellmModel
import asyncio

#Load environment variables from .env file
load_dotenv(find_dotenv())
set_tracing_disabled(disabled=True)
#SET GEMINI_API_KEY
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 
#Set Model from .ENV file
MODEL = os.getenv("MODEL") or "gemini/gemini-2.0-flash" #Default to gemini-1.5-turbo if not set in .env
print(f"Using model >>>> : {MODEL}")
#Set Litellm model instance for using Gemini API, and Model name
litellm_model = LitellmModel(
    model=MODEL,
    api_key=GEMINI_API_KEY
)
#Agent for AI HUB General Assistant
ai_hub_agent:Agent = Agent(
    name="AI_HUB_General_Assistant",
    instructions="An AI HUB assistant that can answer questions and provide information on a specific topics.",
    model=litellm_model,
)
# # set in main function in sync to run the agent until user press exit or Ctrl+C
# def main():
#     #Run the agent in a loop until user press exit or Ctrl+C
#     while True:
#         try:
#             #Get user input from command line
#             user_input = input("Enter your question (or 'exit' to quit): ")
#             if user_input.lower() == 'exit':
#                 break
#             #Run the agent with the user input
#             response = Runner.run_sync(starting_agent=ai_hub_agent, input=user_input)
#             #Display the response in print
#             print(response.final_output)
#         except KeyboardInterrupt:
#             break
#         except Exception as e:
#             print(f"An error occurred: {e}")
# set in main function in async await to run the agent until user press exit or Ctrl+C
async def main():
    #Run the agent in a loop until user press exit or Ctrl+C
    while True:
        try:
            #Get user input from command line
            user_input = input("Enter your question (or 'exit' to quit): ")
            if user_input.lower() == 'exit':
                break
            #Run the agent with the user input
            response =await Runner.run(starting_agent=ai_hub_agent, input=user_input)
            #Display the response in print
            print(response.final_output)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    #Run the main function
    print("Starting AI HUB General Assistant...")
    print("Press Ctrl+C to exit.")
    asyncio.run(main())
    