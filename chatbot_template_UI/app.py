import os
from dotenv import load_dotenv, find_dotenv
import chainlit as cl
from agents import Agent, Runner, set_tracing_disabled, ItemHelpers
from openai import AsyncOpenAI
# from agents.extensions.models.litellm_model import LitellmModel
import asyncio
from typing import cast
from openai.types.responses import ResponseTextDeltaEvent
from comp_agents.ai_hub_agent_file import triage_agent

#Load environment variables from .env file
load_dotenv(find_dotenv())
set_tracing_disabled(disabled=True)
#SET GEMINI_API_KEY
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 

# Check if the API key is present; if not, raise an error
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")


#Set Model from .ENV file
MODEL = os.getenv("MODEL") or "gemini/gemini-2.0-flash" #Default to gemini-1.5-turbo if not set in .env
if not MODEL:
    raise ValueError("MODEL is not set. Please ensure it is defined in your .env file.")
print(f"Using model >>>> : {MODEL}")

#chainlit UI startup message Greetings introduction
@cl.on_chat_start
async def start_conversation():
    #chainlit Message persistence using chat_history
    """Set up the chat session when a user connects."""
    # Initialize an empty chat history in the session.
    cl.user_session.set("chat_history", []) #chat_history=[]
    # set Agent instance in the session with the correct key
    cl.user_session.set("triage_agent", triage_agent)
    # Send a welcome message to the user.
    await cl.Message(
        content="Hello! I am your AI HUB assistant. How can I help you today?",
    ).send()
    
#chainlit UI for the AI HUB General Assistant messgesages persistence using chat_history
@cl.on_message
async def main(message: cl.Message):
    """Process incoming messages and generate responses."""
    # Send a thinking message 
    triage_agent: Agent = cast(Agent, cl.user_session.get("triage_agent"))
    # config: RunConfig = cast(RunConfig, cl.user_session.get("config"))

    # Retrieve the chat history from the session.
    history = cl.user_session.get("chat_history") or []
    # print("Message_Content : >>>> ",message.content)
    # Append the user's message to the history.
    history.append({"role": "user", "content": message.content})
    # print("History : >>>> ",history)
    # Create a new message object for streaming
    msg = cl.Message(content="AI-HuB Assistant : ")
    # print("Message : >>>> ",msg.content)
    await msg.send()
    
    
    try:
        # print("\n[CALLING_AGENT_WITH_CONTEXT]\n", history, "\n")
        result = Runner.run_streamed(starting_agent = triage_agent,
                    input=history)
         # Stream the response token by token
        async for event in result.stream_events():
            if event.type == "raw_response_event" and hasattr(event.data, 'delta'):
                token = event.data.delta
                await msg.stream_token(token)  
        ######################################################### 
        # Append the assistant's response to the history.
        history.append({"role": "assistant", "content": msg.content})
        print("History with assistant : >>>> ",history)
        # print("Final Message msg.content: >>>> ",msg.content)
        await msg.update()
        # Update the session with the new history. overwrite the old history
        cl.user_session.set("chat_history", history)

        # Optional: Log the interaction
        # print(f"User: {message.content}")
        # print(f"Assistant: {msg.content}")

    except Exception as e:
        # Log the error with more details for debugging
        msg.content = f"Error: {str(e)}"
        await msg.update()
        print(f"Error occurred: {str(e)}")
        print("[DEBUG] History:", history)
        print("[DEBUG] Triage Agent:", triage_agent)
        print("[DEBUG] Message Content:", message.content)
