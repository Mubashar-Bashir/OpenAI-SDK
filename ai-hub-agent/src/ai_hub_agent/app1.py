import os
from dotenv import load_dotenv
from typing import cast, List, Dict, Any
import chainlit as cl
from agents import Agent, Runner
from agents.run import RunConfig
from agents.extensions.models.litellm_model import LitellmModel


# Load the environment variables from the .env file
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("MODEL", "gemini-2.0-flash") # Default model if not set

# Check if necessary environment variables are present
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")
if not MODEL:
    print("MODEL is not set. Using default: gemini-2.0-flash")

print(f"Using model >>> : {MODEL}")

# Initialize the model instance using LiteLLM
llm_model_instance = LitellmModel(model=MODEL, api_key=GEMINI_API_KEY)



cl.on_chat_start
async def start():
    """Set up the chat session when a user connects."""

    # Initialize the model instance using LiteLLM
    llm_model_instance = LitellmModel(model=MODEL, api_key=GEMINI_API_KEY)

    # Configure the runner. Note: Using the LitellmModel instance here.
    config = RunConfig(
        model=llm_model_instance, # Pass the instantiated model
        tracing_disabled=True # Set to False if you want tracing in Chainlit UI
    )

    # Initialize an empty chat history in the session.
    # History format: List of {"role": "user"|"assistant", "content": "string"|[{...multimodal_parts}]}
    cl.user_session.set("chat_history", [])

    cl.user_session.set("config", config)
    
    # Define Agents using the same model instance
ai_hub_agent: Agent = Agent(
    name="AI-Hub-Feedback-Assistant",
    instructions="You are a helpful AI-Hub-Assistant to extract json from provided image .",
    model=llm_model_instance,
    
)
@cl.on_message
async def main(message: cl.Message):
    # Your custom logic goes here...
    msg= cl.Message(content= "Thinking...")
    await msg.send()
    # add the message to the chat history
    chat_history = cl.user_session.get("chat_history", [])
    chat_history.append({"role": "user", "content": message.content})
    history= chat_history
    print("Message received >>>>>",message)
    # Send a response back to the user
    try:
        print("\n[CALLING_AGENT_WITH_CONTEXT]\n", chat_history, "\n")
        result = Runner.run_sync(starting_agent = ai_hub_agent,
                    input=history,
                    )
        
        response_content = result.final_output
        
        # Update the thinking message with the actual response
        msg.content = response_content
        await msg.update()

        # Update the session with the new history.
        cl.user_session.set("chat_history", result.to_input_list())
        
        # Optional: Log the interaction
        print(f"User: {message.content}")
        print(f"Assistant: {response_content}")
        
    except Exception as e:
        msg.content = f"Error: {str(e)}"
        await msg.update()
        print(f"Error: {str(e)}")
        
   
# @cl.on_chat_start
# async def start():
#     """Set up the chat session when a user connects."""

#     # Initialize the model instance using LiteLLM
#     llm_model_instance = LitellmModel(model=MODEL, api_key=GEMINI_API_KEY)

#     # Configure the runner. Note: Using the LitellmModel instance here.
#     config = RunConfig(
#         model=llm_model_instance, # Pass the instantiated model
#         tracing_disabled=True # Set to False if you want tracing in Chainlit UI
#     )

#     # Initialize an empty chat history in the session.
#     # History format: List of {"role": "user"|"assistant", "content": "string"|[{...multimodal_parts}]}
#     cl.user_session.set("chat_history", [])

#     cl.user_session.set("config", config)

#     # # Define Agents using the same model instance
#     # ai_hub_agent: Agent = Agent(
#     #     name="AI-Hub-Assistant",
#     #     instructions="You are a helpful AI-Hub-Assistant assistant that helps users with their queries from the AI-Hub knowledge base.",
#     #     model=llm_model_instance,
#     # )

#     image_to_text_agent: Agent = Agent(
#         name="ImageToTextAgent",
#         instructions="""You are an OCR image processor and handwritten feedback form extractor.
#         Your task is to return a structured JSON object with extracted values, strictly following this format:
#         {
#           "Name": "<Extracted Name>",
#           "Institution": "<Extracted Institution>",
#           "Contact": "<Extracted Contact Number>",
#           "Designation": "<Extracted Designation>",
#           "Content_relevance": "<Excellent | Good | Average | Poor>",
#           "Clarity_of_explanation": "<Very Clear | Clear | Somewhat Unclear | Very Unclear>",
#           "Presenter_engagement": "<Very Engaging | Moderately | Neutral | Not Engaging>",
#           "Communication_effectiveness": "<Excellent | Good | Average | Poor>",
#           "Overall_rating": "<Excellent | Good | Average | Poor>",
#           "Suggestions_for_improvement": "<Extracted Text>",
#           "Interest_in_more_sessions": "<Yes | No>",
#           "Preferred_topics": "<Extracted Text>"
#         }
#         Respond only with a valid JSON object. No extra text.
#         """,
#         model=llm_model_instance, # Use the same model instance
#     )
