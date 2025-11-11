from dotenv import load_dotenv
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
import os
import asyncio




load_dotenv()
# The InMemorySaver is used to store the conversation history in memory.
# This is for experimentation purposes only.
# For production, you should use a persistent storage solution
# Use PostgresSaver -> from langgraph.checkpoint.postgres import PostgresSaver
agent = create_agent(
    model="gpt-4o-mini",
    system_prompt="You are an AI chatbot that will response to user query.",
    checkpointer=InMemorySaver(),
    debug=False
)


async def stream_agent(user_input: str):
    input = {"messages": [{"role": "user", "content": user_input}]}
    identifier = {"configurable": {"thread_id": "1"}}
    async for results in agent.astream(input, identifier, stream_mode="messages"):
        print(f"{results[0].content}", end="", flush=True)

    print()  # Add a newline at the end


while True:
    print (">>> ", flush=True, end="")
    user_input = input()
    if user_input.strip().lower() == "exit":
        break
    asyncio.run(stream_agent(user_input))
    

