# OpenAI Chatbot Project

## Overview

This project sets up a chatbot using the OpenAI Agents framework, utilizing LiteLLM for model management and Gemini as the language model.  It includes a basic example of a function tool.

## Features

* **Chatbot Agent:** An agent is configured to respond to user input.
* **LiteLLM Integration:** LiteLLM is used to provide a unified interface to different language models.
* **Gemini Model:** The agent is set up to use the Gemini language model.
* **Function Tool:** The project includes an example of a function tool (`get_weather`) that the agent can use.
* **Environment Setup:** Uses `.env` file for managing API keys and model settings.

## Requirements

* Python 3.12.8
* The following Python packages:
    * `openai-agents[litellm]`
    * `python-dotenv`
    * `chainlit`

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <your_repository_url>
    cd openai-chatbot
    ```

2.  **Create a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  **Install the dependencies:**
    ```bash
    uv pip install -r requirements.txt
    ```

4.  **Set up the `.env` file:**
    * Create a `.env` file in the project's root directory.
    * Add your Gemini API key:
        ```.env
        GEMINI_API_KEY=YOUR_GEMINI_API_KEY
        MODEL=gemini/gemini-2.0-flash # Or your preferred Gemini model
        ```
    * Ensure that the `.env` file is in the same directory as `app.py`.

## Usage

1.  **Run the Chainlit application:**
    ```bash
    chainlit run app.py
    ```

2.  Interact with the chatbot through the Chainlit interface.

## Code Description

### `app.py`

* Imports necessary libraries: `os`, `asyncio`, `logging`, `agents`, `LitellmModel`, `dotenv`.
* Loads environment variables from a `.env` file.
* Defines a function tool:
    * `get_weather(city: str) -> str`:  A simple example that returns a weather string for a given city.
* Configures an agent:
    * Uses `LitellmModel` to interface with the Gemini model.
    * Sets the agent's instructions.
    * Assigns the `get_weather` tool to the agent.
* Runs the agent using `Runner.run_sync()`.

### Function Tool Example

The `@function_tool` decorator is used to define functions that the agent can use.  In this example, the `get_weather` function is decorated:

```python
@function_tool
def get_weather(city: str) -> str:
    print(f"[debug] getting weather for {city}")
    return f"The weather in {city} is sunny."
The agent can call this function when it determines that it needs to know the weather in a city.  The function's docstring is important, as it tells the agent what the function does.Agent using LiteLLM with Gemini settingsThe agent is initialized with the LitellmModel, which is configured to use the Gemini model:agent = Agent(
    name="Assistant",
    instructions="You only respond in haikus.",
    tools=[get_weather],
    model=LitellmModel(model=MODEL, api_key=GEMINI_API_KEY),
)
model=MODEL:  Specifies the Gemini model to use (e.g., "gemini/gemini-2.0-flash").  The value of MODEL is read from the .env file.api_key=GEMINI_API_KEY:  Provides the API key for accessing the Gemini model.  The value of GEMINI_API_KEY is read from the .env file.