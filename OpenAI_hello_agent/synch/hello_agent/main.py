import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig

# Load the environment variables from the .env file
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL= os.getenv('BASE_URL')
MODEL ='mistralai/mistral-small-24b-instruct-2501:free'
print('I have selected LLM Model >>> ',MODEL)


# Check if the API key is present; if not, raise an error
if not OPENROUTER_API_KEY :
    raise ValueError("OPENROUTER_API_KEY, is not set. Please ensure it is defined in your .env file.")
if not  MODEL:
    raise ValueError("Model is not Selected")
if not BASE_URL :
    raise ValueError("BASE_URL is not selected") 

#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url=BASE_URL,
)

model = OpenAIChatCompletionsModel(
    model=MODEL,
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

agent: Agent = Agent(name="Assistant", instructions="You are a helpful assistant", model=model)

result = Runner.run_sync(agent, "Hello, how are you.", run_config=config)

print("\nCALLING AGENT\n")
print(result.final_output)