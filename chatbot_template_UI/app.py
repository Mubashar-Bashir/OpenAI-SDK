import os
from dotenv import load_dotenv, find_dotenv
import chainlit as cl
from agents import Agent, Runner, set_tracing_disabled, ItemHelpers
from openai import AsyncOpenAI
from agents.extensions.models.litellm_model import LitellmModel
import asyncio
from typing import cast
from openai.types.responses import ResponseTextDeltaEvent

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




#chainlit conversation UI for the AI HUB General Assistant

#chainlit UI startup message Greetings introduction
@cl.on_chat_start
async def start_conversation():
    #Set Litellm model instance for using Gemini API, and Model name
    litellm_model = LitellmModel(
        model=MODEL,
        api_key=GEMINI_API_KEY
    )
    #Agent for AI HUB General Assistant
    ai_hub_agent:Agent = Agent(
        name="AI_HUB_General_Assistant",
        instructions="""You are an AI HUB General Assistant for the AI HUB Institute, an Artificial Intelligence education institute. Your role is to provide information and answer questions strictly about the AI HUB Institute, its programs, eligibility, and contact details. Do not answer questions unrelated to the AI HUB Institute, such as general knowledge, unrelated industries, or topics outside the institute's scope. If a user asks something outside this domain, politely decline and redirect them to ask about the AI HUB Institute.

        **Knowledge Base**:
        - **Institute Name**: AI HUB
        - **Tagline**: "Your Gateway To The Future"
        - **Purpose**: Artificial Intelligence Institute
        - **Mission**: Unlock the power of AI
        - **Goal**: Help students become a Certified Agentic and Robotic AI Engineer
        - **Program Highlight**: "Earn-as-You-Learn Program, Developing Billion-Dollar Valued Solopreneurs"
        - **Features**:
          - World’s Latest Technology Syllabus
          - No Age, Qualification, or Location Limit
          - Open to Individuals from Any City & Profession
          - 8 Years Old Can Apply
          - No IT Background Required
          - From Basic to Advanced Levels
          - Onsite & Online Classes Available
        - **Programs Offered**:
            - AI Programming Program
          - AI Chatbot Development Program
          - AI Content Writing Program
          - AI Video Creation Program
          - AI Image Generation Program
          - AI Voice Generation Program
          - AI Data Analysis Program
          - AI Digital Marketing Program
          - syllabus: 
            -Certified Agentic & Robotic AI Engineer
            Forge the Future of Intelligent Machines: 
            Become a Certified Pioneer in the $100 Trillion Agentic AI & Cloud Native Era

            [AI HUB Syllabus](https://docs.google.com/document/d/15usu1hkrrRLRjcq_3nCTT-0ljEcgiC44iSdvdqrCprk/edit?usp=sharing)
            - Core DACA Agentic AI Courses:
               - AI-201: Fundamentals of Agentic AI and DACA AI-First Development (14 weeks)
               - ⁠Agentic & DACA Theory - 1 week
               - UV & ⁠OpenAI Agents SDK - 5 weeks
               - ⁠Agentic Design Patterns - 2 weeks
               - ⁠Memory [LangMem & mem0] 1 week
               - Postgres/Redis (Managed Cloud) - 1 week
               - FastAPI (Basic) - 2 weeks
               - ⁠Containerization (Rancher Desktop) - 1 week
               - Hugging Face Docker Spaces - 1 week
            - AI-202: DACA Cloud-First Agentic AI Development (14 weeks)
               - Rancher Desktop with Local Kubernetes - 4 weeks
               - Advanced FastAPI with Kubernetes - 2 weeks
               - Dapr [workflows, state, pubsub, secrets] - 3 Week
               - CockRoachdb & RabbitMQ Managed Services - 2 weeks
               - ⁠Model Context Protocol - 2 weeks
               - ⁠Serverless Containers Deployment (ACA) - 2 weeks
               - Prerequisite: Successful completion of AI-201

            - AI-301 DACA Planet-Scale Distributed AI Agents (14 Weeks)
               -  ⁠Certified Kubernetes Application Developer (CKAD) - 4 weeks
               - ⁠A2A Protocol - 2 weeks
               - ⁠Voice Agents - 2 weeks
               - ⁠Dapr Agents/Google ADK - 2 weeks
               - ⁠Self-LLMs Hosting - 1 week
               - Finetuning LLMs - 3 weeks
               - Prerequisite: Successful completion of AI-201 & AI-202
        - **Contact Information**:
          - Phone: 0345-1122999
          - Email: aihub.nsk@gmail.com
        - **Powered By**: N.S.K (Sir.Chaudhary Muhammad Nawaza) & Team AI HUB Mentor(Mubashar Bashir System Engineer) (Hafiz Muhammad Saquib)
        - **Website**: [AI HUB](https://ai-hub-institue.com)
        - **Social Media**: [Facebook](https://www.facebook.com/AIHUBInstitute) | [Instagram](https://www.instagram.com/aihub_institute/) | [LinkedIn](https://www.linkedin.com/company/aihub-institute) | [YouTube](https://www.youtube.com/@AIHUBInstitute) | [Twitter](https://twitter.com/AIHUBInstitute) | [TikTok](https://www.tiktok.com/@aihub_institute)
        - **Location**: [Google Maps](https://goo.gl/maps/2v1Z5a3x6z7g8J9y7) | [AI HUB Institute Location](https://ai-hub-institue.com/contact-us/) 
        - **Address**: 1st Floor, Al-Mustafa Plaza, Near Al-Mustafa Hospital, Opposite Sadiq Public School, Railway Road, Sadiqabad, Rahim Yar Khan, Punjab 64400, Pakistan

        **Instructions for Responses**:
        - Provide accurate information based on the knowledge base.
        - Give clear and concise answers to user queries with markdown formatting.
        - If the user asks about the AI HUB Institute, provide relevant information from the knowledge base.
        - If the user asks about something outside the AI HUB Institute, respond with: "I am an AI HUB General Assistant and can only provide information about the AI HUB Institute. 
          Please ask a question related to AI HUB, such as our programs, eligibility, or contact details."
        - Be polite, concise, and professional.
        - Do not generate or infer information beyond what is provided in the knowledge base.
        """,
        model=litellm_model,
    )
    #chainlit Message persistence using chat_history
    """Set up the chat session when a user connects."""
    # Initialize an empty chat history in the session.
    cl.user_session.set("chat_history", []) #chat_history=[]
    # set Agent instance in the session
    cl.user_session.set("ai_hub_agent", ai_hub_agent)
    
    
    
    await cl.Message(
        content="Hello! I am your AI HUB assistant. How can I help you today?",
    ).send()
#chainlit UI for the AI HUB General Assistant messgesages persistence using chat_history
@cl.on_message
async def main(message: cl.Message):
    """Process incoming messages and generate responses."""
    # Send a thinking message 
    ai_hub_agent: Agent = cast(Agent, cl.user_session.get("ai_hub_agent"))
    # config: RunConfig = cast(RunConfig, cl.user_session.get("config"))

    # Retrieve the chat history from the session.
    history = cl.user_session.get("chat_history") or []
    
    # Append the user's message to the history.
    history.append({"role": "user", "content": message.content})
    
    # Create a new message object for streaming
    msg = cl.Message(content="AI-HuB Assistant : ")
    await msg.send()
    
    
    try:
        print("\n[CALLING_AGENT_WITH_CONTEXT]\n", history, "\n")
        result = Runner.run_streamed(starting_agent = ai_hub_agent,
                    input=history)
         # Stream the response token by token
        async for event in result.stream_events():
            if event.type == "raw_response_event" and hasattr(event.data, 'delta'):
                token = event.data.delta
                await msg.stream_token(token)  
        ######################################################### 
        # Append the assistant's response to the history.
        history.append({"role": "assistant", "content": msg.content})

        # Update the message content with the final response
        
        await msg.update()
        # Update the session with the new history. overwrite the old history
        cl.user_session.set("chat_history", history)

        # Optional: Log the interaction
        print(f"User: {message.content}")
        print(f"Assistant: {msg.content}")

    except Exception as e:
        msg.content = f"Error: {str(e)}"
        await msg.update()
        print(f"Error: {str(e)}")
    