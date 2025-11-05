from dotenv import load_dotenv
from langchain.agents import create_agent
import asyncio

load_dotenv()


# If you want to understand the structore of the object returned by the agent.astream, 
# Please read the explore_event_stream.py file.
# It will print the structure of the object returned by the agent.astream and agent.astream_events.

agent = create_agent(
    model="gpt-4o-mini",
    tools=[],
    debug=False,
)

async def stream_agent():
    input = {"messages": [{"role": "user", "content": "What is the capital of USA?"}]}
    async for results in agent.astream(input, stream_mode="messages"):
        print(f"{results[0].content}", end="", flush=True)

    print()  # Add a newline at the end

asyncio.run(stream_agent())
