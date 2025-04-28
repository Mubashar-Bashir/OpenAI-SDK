import chainlit as cl
from agents import Agent, ItemHelpers, MessageOutputItem, Runner, set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel
from dotenv import load_dotenv
import os
import asyncio

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("MODEL") or 'gemini/gemini-2.0-flash-exp'

# Disable tracing for simplicity
set_tracing_disabled(disabled=True)

# Define translation agents
spanish_agent = Agent(
    name="spanish_agent",
    instructions="You translate the user's message to Spanish",
    model=LitellmModel(model=MODEL, api_key=GEMINI_API_KEY),
    handoff_description="An English to Spanish translator",
)

french_agent = Agent(
    name="french_agent",
    instructions="You translate the user's message to French",
    model=LitellmModel(model=MODEL, api_key=GEMINI_API_KEY),
    handoff_description="An English to French translator",
)

urdu_agent = Agent(
    name="urdu_agent",
    instructions="You translate the user's message to Modern Pakistani Urdu",
    model=LitellmModel(model=MODEL, api_key=GEMINI_API_KEY),
    handoff_description="An English to Urdu translator",
)

italian_agent = Agent(
    name="italian_agent",
    instructions="You translate the user's message to Italian",
    model=LitellmModel(model=MODEL, api_key=GEMINI_API_KEY),
    handoff_description="An English to Italian translator",
)

# Define orchestrator agent with translation tools
orchestrator_agent = Agent(
    name="orchestrator_agent",
    instructions=(
        "You are a translation agent. You use the tools given to you to translate. "
        "If asked for multiple translations, you call the relevant tools in order. "
        "You never translate on your own, you always use the provided tools."
    ),
    tools=[
        spanish_agent.as_tool(
            tool_name="translate_to_spanish",
            tool_description="Translate the user's message to Spanish",
        ),
        french_agent.as_tool(
            tool_name="translate_to_french",
            tool_description="Translate the user's message to French",
        ),
        italian_agent.as_tool(
            tool_name="translate_to_italian",
            tool_description="Translate the user's message to Italian",
        ),
        urdu_agent.as_tool(
            tool_name="translate_to_urdu",
            tool_description="Translate the user's message to Urdu",
        ),
    ],
    model=LitellmModel(model=MODEL, api_key=GEMINI_API_KEY),
)

# Define synthesizer agent
synthesizer_agent = Agent(
    name="synthesizer_agent",
    instructions="You inspect translations, correct them if needed, and produce a final concatenated response.",
    model=LitellmModel(model=MODEL, api_key=GEMINI_API_KEY),
)

# Chainlit event handler for app startup
@cl.on_chat_start
async def on_chat_start():
    # Create buttons for each language
    actions = [
        cl.Action(name="translate_to_spanish", payload={"language": "Spanish"}, label="Translate to Spanish"),
        cl.Action(name="translate_to_french", payload={"language": "French"}, label="Translate to French"),
        cl.Action(name="translate_to_italian", payload={"language": "Italian"}, label="Translate to Italian"),
        cl.Action(name="translate_to_urdu", payload={"language": "Urdu"}, label="Translate to Urdu"),
    ]
    # Send welcome message with buttons
    await cl.Message(
        content="Hi! Enter the text you want to translate, then click a language button to translate.",
        actions=actions
    ).send()

# Chainlit event handler for actions (button clicks)
@cl.action_callback("translate_to_spanish")
async def on_spanish_action(action: cl.Action):
    await process_translation(action.payload["language"])

@cl.action_callback("translate_to_french")
async def on_french_action(action: cl.Action):
    await process_translation(action.payload["language"])

@cl.action_callback("translate_to_italian")
async def on_italian_action(action: cl.Action):
    await process_translation(action.payload["language"])

@cl.action_callback("translate_to_urdu")
async def on_urdu_action(action: cl.Action):
    await process_translation(action.payload["language"])

# Helper function to process translations
async def process_translation(language: str):
    # Get the latest user message from session
    user_message = cl.user_session.get("last_message")
    if not user_message:
        await cl.Message(content="Please enter a message to translate first.").send()
        return

    # Map language to tool
    language_to_tool = {
        "Spanish": "translate_to_spanish",
        "French": "translate_to_french",
        "Italian": "translate_to_italian",
        "Urdu": "translate_to_urdu"
    }
    tool_name = language_to_tool.get(language)

    # Run orchestrator with specific tool instruction
    msg = f"Translate '{user_message}' to {language} using {tool_name}"
    orchestrator_result = await Runner.run(orchestrator_agent, msg)

    # Extract intermediate translations
    intermediate_results = []
    for item in orchestrator_result.new_items:
        if isinstance(item, MessageOutputItem):
            text = ItemHelpers.text_message_output(item)
            if text:
                intermediate_results.append(f"{language} translation: {text}")

    # Run synthesizer to finalize output
    synthesizer_result = await Runner.run(
        synthesizer_agent, orchestrator_result.to_input_list()
    )

    # Send final result to UI
    final_message = f"**Final {language} Translation**:\n{synthesizer_result.final_output}"
    if intermediate_results:
        final_message = "\n".join(intermediate_results) + "\n\n" + final_message

    await cl.Message(content=final_message).send()

# Chainlit event handler for incoming messages
@cl.on_message
async def on_message(message: cl.Message):
    # Store the latest message in session
    cl.user_session.set("last_message", message.content)
    # Prompt user to select a language
    actions = [
        cl.Action(name="translate_to_spanish", payload={"language": "Spanish"}, label="Translate to Spanish"),
        cl.Action(name="translate_to_french", payload={"language": "French"}, label="Translate to French"),
        cl.Action(name="translate_to_italian", payload={"language": "Italian"}, label="Translate to Italian"),
        cl.Action(name="translate_to_urdu", payload={"language": "Urdu"}, label="Translate to Urdu"),
    ]
    await cl.Message(
        content=f"Got your message: '{message.content}'. Click a button to translate.",
        actions=actions
    ).send()