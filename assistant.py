"""The brain of the project: a LangChain agent with tools and conversation memory."""
import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver

from tools import TOOLS

load_dotenv()

SYSTEM_PROMPT = (
    "You are a helpful, friendly AI assistant. "
    "Answer clearly and simply. Use the tools when they help: "
    "the calculator for maths, wikipedia_search for facts, "
    "get_current_time for date and time. If you are unsure, say so."
)


def build_agent():
    """Create the agent. Memory is stored per thread_id."""
    model = ChatGoogleGenerativeAI(
        model=os.getenv("MODEL_NAME", "gemini-3.8-flash"),
        temperature=0.3,
        thinking_level="low",
        timeout=60,
        max_retries=2,
    )
    return create_agent(
        model=model,
        tools=TOOLS,
        system_prompt=SYSTEM_PROMPT,
        checkpointer=InMemorySaver(),
    )


def ask(agent, user_text: str, thread_id: str) -> str:
    """Send one message and return the assistant's reply as plain text."""
    result = agent.invoke(
        {"messages": [{"role": "user", "content": user_text}]},
        config={"configurable": {"thread_id": thread_id}},
    )
    content = result["messages"][-1].content
    if isinstance(content, list):  # some models return a list of blocks
        content = "".join(
            block.get("text", "") if isinstance(block, dict) else str(block)
            for block in content
        )
    return content


if __name__ == "__main__":  # quick terminal test: python assistant.py
    agent = build_agent()
    print("Chat started. Type 'exit' to quit.")
    while True:
        text = input("You: ")
        if text.strip().lower() == "exit":
            break
        print("AI:", ask(agent, text, thread_id="cli"))
