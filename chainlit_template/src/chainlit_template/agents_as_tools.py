import asyncio
from agents import Agent, ItemHelpers, MessageOutputItem, Runner, set_tracing_disabled, OpenAIChatCompletionsModel, trace
from openai import AsyncOpenAI
from agents.extensions.models.litellm_model import LitellmModel
from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("MODEL") or 'gemini/gemini-2.0-flash-exp'
print("\n\n Model Selected >>> ",MODEL)

"""
This example shows the agents-as-tools pattern. The frontline agent receives a user message and
then picks which agents to call, as tools. In this case, it picks from a set of translation
agents.
"""
# set_tracing_disabled(disabled=True)

spanish_agent = Agent(
    name="spanish_agent",
    instructions="You translate the user's message to Spanish",
    model=LitellmModel(model=MODEL, api_key=GEMINI_API_KEY),
    handoff_description="An english to spanish translator",
)

french_agent = Agent(
    name="french_agent",
    instructions="You translate the user's message to French",
    model=LitellmModel(model=MODEL, api_key=GEMINI_API_KEY),
    handoff_description="An english to french translator",
)
urdu_agent = Agent(
    name="urdu_agent",
    instructions="You translate the user's message to Modern Pakistani Urdu",
    model=LitellmModel(model=MODEL, api_key=GEMINI_API_KEY),
    handoff_description="An english to urdu translator",
)

italian_agent = Agent(
    name="italian_agent",
    instructions="You translate the user's message to Italian",
    model=LitellmModel(model=MODEL, api_key=GEMINI_API_KEY),
    handoff_description="An english to italian translator",
)

orchestrator_agent = Agent(
    name="orchestrator_agent",
    instructions=(
        "You are a translation agent. You use the tools given to you to translate."
        "If asked for multiple translations, you call the relevant tools in order."
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
            tool_description="Translate the user's message to urdu",
        ),
    ],
    model=LitellmModel(model=MODEL, api_key=GEMINI_API_KEY),
)

synthesizer_agent = Agent(
    name="synthesizer_agent",
    instructions="You inspect translations, correct them if needed, and produce a final concatenated response.",
    model=LitellmModel(model=MODEL, api_key=GEMINI_API_KEY),
)


async def main():
    msg = input("Hi! What would you like translated, and to which languages? ")

    # Run the entire orchestration in a single trace
    with trace("Orchestrator evaluator"):
        orchestrator_result = await Runner.run(orchestrator_agent, msg)

        for item in orchestrator_result.new_items:
            if isinstance(item, MessageOutputItem):
                text = ItemHelpers.text_message_output(item)
                if text:
                    print(f"  - Translation step: {text}")

        synthesizer_result = await Runner.run(
            synthesizer_agent, orchestrator_result.to_input_list()
        )

    print(f"\n\nFinal response:\n{synthesizer_result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())