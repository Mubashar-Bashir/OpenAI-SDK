# import os
# from dotenv import load_dotenv
# from typing import cast
# import chainlit as cl
# from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
# from agents.run import RunConfig
# from agents.extensions.models.litellm_model import LitellmModel
# from model import FeedbackFormSchema

# # Load the environment variables from the .env file
# load_dotenv()

# OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# MODEL = os.getenv("MODEL", "gemini-2.0-flash")

# # Check if the API key is present; if not, raise an error
# if not GEMINI_API_KEY:
#     raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")
# if not OPENROUTER_API_KEY:
#     raise ValueError("OPENROUTER_API_KEY is not set. Please ensure it is defined in your .env file.")
# if not MODEL:
#     raise ValueError("MODEL is not set. Please ensure it is defined in your .env file.")

# # Check if the model is supported
# print(f"Using model >>> : {MODEL}")

# @cl.on_chat_start
# async def start():
   

#     config = RunConfig(
#         # model=MODEL,
#         model=LitellmModel(model=MODEL, api_key=gemini_api_key),
#         # model=OpenAIChatCompletionsModel(model=MODEL, openai_client=external_client),        
#         # model_provider=external_client,
#         tracing_disabled=True
#     )
#     """Set up the chat session when a user connects."""
#     # Initialize an empty chat history in the session.
#     cl.user_session.set("chat_history", [])

#     cl.user_session.set("config", config)
#     ai_hub_agent: Agent = Agent(
#         name="AI-Hub-Assistant", 
#         instructions="You are a helpful AI-Hub-Assistant assistant that helps users with their queries from the AI-Hub knowledge base.", 
#         model=LitellmModel(model=MODEL, api_key=GEMINI_API_KEY),
        
#     )
#     image_to_text_agent:Agent = Agent(
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
        
#         model=LitellmModel(model=MODEL, api_key=GEMINI_API_KEY),
        
#     )
#     # Define orchestrator agent with translation tools
#     orchestrator_agent:Agent = Agent(
#         name="orchestrator_agent",
#         instructions=(
#             "You are a AI-HUB General Assistant agent. You use the tools given to you to Assist. "
#             "If asked for General Question Answer Give Reply specifically, you call the relevant tools in order. "
#             "if you have to work for image to text for feedback form, you call the image_to_text_agent. "
#             "You should never try on your own, you always use the provided tools."
#         ),
#         tools=[
#             image_to_text_agent.as_tool(
#                 tool_name="image_to_text_tool",
#                 tool_description="Extract key:value from the user's provide image to json object",
#             ),
#             ai_hub_agent.as_tool(
#                 tool_name="ai_hub_agent_tool",
#                 tool_description="Answer the user's question using AI-Hub knowledge base.",
                
#             ),
        
#         ],
#         model=LitellmModel(model=MODEL, api_key=GEMINI_API_KEY),
#     )

        
    
    
    
#     cl.user_session.set("agent", orchestrator_agent)

#     await cl.Message(content="Welcome to the AI Assistant! How can I help you today?").send()

# @cl.on_message
# async def main(message: cl.Message):
#     """Process incoming messages and generate responses."""
#     # Send a thinking message
#     msg = cl.Message(content="Thinking...")
#     await msg.send()

#     agent: Agent = cast(Agent, cl.user_session.get("agent"))
#     config: RunConfig = cast(RunConfig, cl.user_session.get("config"))

#     # Retrieve the chat history from the session.
#     history = cl.user_session.get("chat_history") or []
    
#     # Append the user's message to the history.
#     history.append({"role": "user", "content": message.content})
    

#     try:
#         print("\n[CALLING_AGENT_WITH_CONTEXT]\n", history, "\n")
#         result = Runner.run_sync(starting_agent = orchestrator_agent,
#                     input=history,
#                     run_config=config)
        
#         response_content = result.final_output
        
#         # Update the thinking message with the actual response
#         msg.content = response_content
#         await msg.update()
    
#         # Update the session with the new history.
#         cl.user_session.set("chat_history", result.to_input_list())
        
#         # Optional: Log the interaction
#         print(f"User: {message.content}")
#         print(f"Assistant: {response_content}")
        
#     except Exception as e:
#         msg.content = f"Error: {str(e)}"
#         await msg.update()
#         print(f"Error: {str(e)}")
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

@cl.on_chat_start
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
        name="AI-Hub-Assistant",
        instructions="You are a helpful AI-Hub-Assistant assistant that helps users with their queries from the AI-Hub knowledge base.",
        model=llm_model_instance,
    )

    image_to_text_agent: Agent = Agent(
        name="ImageToTextAgent",
        instructions="""You are an OCR image processor and handwritten feedback form extractor.
        Your task is to return a structured JSON object with extracted values, strictly following this format:
        {
          "Name": "<Extracted Name>",
          "Institution": "<Extracted Institution>",
          "Contact": "<Extracted Contact Number>",
          "Designation": "<Extracted Designation>",
          "Content_relevance": "<Excellent | Good | Average | Poor>",
          "Clarity_of_explanation": "<Very Clear | Clear | Somewhat Unclear | Very Unclear>",
          "Presenter_engagement": "<Very Engaging | Moderately | Neutral | Not Engaging>",
          "Communication_effectiveness": "<Excellent | Good | Average | Poor>",
          "Overall_rating": "<Excellent | Good | Average | Poor>",
          "Suggestions_for_improvement": "<Extracted Text>",
          "Interest_in_more_sessions": "<Yes | No>",
          "Preferred_topics": "<Extracted Text>"
        }
        Respond only with a valid JSON object. No extra text.
        """,
        model=llm_model_instance, # Use the same model instance
    )

    # Define orchestrator agent with tools
    orchestrator_agent: Agent = Agent(
        name="orchestrator_agent",
        instructions=(
            "You are a AI-HUB General Assistant agent. You use the tools given to you to Assist. "
            "If asked for General Question Answer, Give Reply specifically, you call the relevant tools in order. "
            "If you have to work for image to text for feedback form, you call the image_to_text_tool. "
            "You should never try on your own, you always use the provided tools."
        ),
        tools=[
            image_to_text_agent.as_tool(
                tool_name="image_to_text_tool",
                tool_description="Extract key:value from the user's provide image to json object",
            ),
            ai_hub_agent.as_tool(
                tool_name="ai_hub_agent_tool",
                tool_description="Answer the user's question using AI-Hub knowledge base.",
            ),
        ],
        model=llm_model_instance, # Use the same model instance
    )

    cl.user_session.set("agent", orchestrator_agent)

    await cl.Message(content="Welcome to the AI Assistant! How can I help you today?").send()

@cl.on_message
async def main(message: cl.Message):
    """Process incoming messages (text and images) and generate responses."""
    # --- File Upload Handling ---
    uploaded_files = [elem for elem in message.elements if isinstance(elem, (cl.Image, cl.File))]
    upload_dir = "uploads" # Define the directory

    if uploaded_files:
        print(f"Detected {len(uploaded_files)} uploaded file(s).")
        # Ensure the uploads directory exists
        os.makedirs(upload_dir, exist_ok=True)
        try:
            # Save all attached files to the directory
            # Chainlit saves them with their original filenames by default
            # saved_files_paths = await message
            print(f"Saved file(s) to: {saved_files_paths}")
            # Optional: Send a message confirming file upload/save
            # await cl.Message(content=f"Saved file(s): {', '.join([os.path.basename(p) for p in saved_files_paths])}").send()
        except Exception as e:
            print(f"Error saving files: {e}")
            # Optional: Inform the user about the saving error
            # await cl.Message(content=f"Error saving uploaded file(s): {e}").send()
    # --- End File Upload Handling ---

    
    # Send a thinking message
    msg = cl.Message(content="Thinking...")
    await msg.send()
    print("[Debuging] >>> ",msg)
    agent: Agent = cast(Agent, cl.user_session.get("agent"))
    config: RunConfig = cast(RunConfig, cl.user_session.get("config"))

    # Retrieve the chat history from the session.
    # History format: List of {"role": ..., "content": ...}
    history: List[Dict[str, Any]] = cl.user_session.get("chat_history", [])

    # --- Prepare current turn's input (text + images) ---
    current_message_content: Any # Will be str or List[Dict]
    #create uploadd directory if not exists
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    
    # # Save the image to a file in the uploads directory
    # # This is a placeholder; you should implement the actual saving logic based on your requirements.
    # # For example, you might want to save the image with a unique name or timestamp.
    # image_path = os.path.join("uploads", f"{message.id}.jpeg") # Example path
    # # uploads = await message.save_image(image_path) # This is a placeholder; implement your own saving logic
    # #save the image to a file in the uploads directory
    # # This is a placeholder; you should implement the actual saving logic based on your requirements.
    # # .uploads = await message.save_image(image_path) # This is a placeholder; implement your own saving logic
    # #plot the image using chainlit
    
    
    # cl.image(image_path, caption="Uploaded Image") # This is a placeholder; implement your own image display logic
    # #chainlit image saving path and location 
    # cl.image(image_path, caption="Uploaded Image", name="Uploaded Image") # This is a placeholder; implement your own image display logic
    # cl.Image(image_path, caption="Uploaded Image", name="Uploaded Image") # This is a placeholder; implement your own image display logic
    # # Append the user's message to the history.
    # # Ensure the message content is a string or multimodal list
    
    # Handle image elements first to ensure URLs are ready
    image_elements = [elem for elem in message.elements if isinstance(elem, cl.Image)]
    
    # Process images if they exist
    if image_elements:
        # Create a message to send just the images to get their URLs populated by Chainlit
        image_message = cl.Message(
            content="", # No text content needed for this intermediate message
            elements=image_elements
        )
        # Sending the message updates the elements' .url attribute with data URLs
        await image_message.send()

        # Now, build the content list for the user message
        content_parts: List[Dict[str, Any]] = []

        # Add text content if it exists
        if message.content:
             content_parts.append({"type": "text", "text": message.content})

        # Add image elements with populated URLs
        for sent_element in image_message.elements:
            if sent_element.url: # Check if URL was successfully populated
                 content_parts.append({
                     "type": "image_url",
                     "image_url": {
                         "url": sent_element.url # Use the populated data URL
                     }
                 })
            else:
                print(f"Warning: Image element '{sent_element.name}' did not get a URL. Skipping.")
                # You might want to inform the user if an image failed to load
                # await cl.Message(content=f"Warning: Could not process image '{sent_element.name}'.").send()

        # The final content is the list of parts
        current_message_content = content_parts

    elif message.content:
        # If only text, the content is just the string
        current_message_content = message.content
    else:
        # If no content (neither text nor images), handle or skip
        msg.content = "No processable input received (text or supported image)."
        await msg.update()
        return # Exit if no valid content to process

    # Append the current user message (string or multimodal list) to the history.
    # Ensure there is content before appending a user message
    if current_message_content:
        history.append({"role": "user", "content": current_message_content})
    else:
        # This case should ideally be caught by the `if not current_message_content_parts` check above,
        # but added as a safeguard.
        msg.content = "No valid input to process."
        await msg.update()
        return


    try:
        print("\n[CALLING_AGENT_WITH_CONTEXT]\n", history, "\n")

        # Run the orchestrator agent with the full history as input
        # ASSUMPTION: Your Runner/Agent SDK processes the history list as the conversation context
        # and uses the LAST item in the list as the current user input for the first step.
        result = Runner.run_sync(
            starting_agent=agent, # Use the agent retrieved from session (orchestrator)
            input=history,        # Pass the full history list
            run_config=config     # Use the defined config
        )

        response_content = result.final_output

        # Ensure response content is appropriate for display
        if isinstance(response_content, dict):
             # If the output is the feedback JSON, display it nicely
             msg.content = "Successfully extracted feedback data:\n```json\n" + str(response_content) + "\n```"
        elif response_content is None:
             # Agent finished without producing a final output string/dict
             msg.content = "Agent finished without producing a final output."
        else:
            # Assuming standard text response
            msg.content = str(response_content)

        # Update the thinking message with the actual response
        await msg.update()

        # Append the assistant's final response to the chat history
        # Only append the final response, not internal tool calls/steps
        # Ensure the assistant message content is always a string for history
        history.append({"role": "assistant", "content": msg.content})

        # Update the session with the new history.
        cl.user_session.set("chat_history", history)

        # Optional: Log the interaction
        print(f"User input (formatted for agent): {current_message_content}")
        print(f"Assistant: {msg.content}")

    except Exception as e:
        # Provide more detailed error logging on the server side
        import traceback
        traceback.print_exc()
        msg.content = f"Error during agent run: {str(e)}\n\nCheck server logs for details."
        await msg.update()
        print(f"Error during agent run: {str(e)}")