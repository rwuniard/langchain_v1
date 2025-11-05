from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import tool
from datetime import datetime
from langchain_core.messages import AIMessageChunk
from IPython.display import Image
import asyncio


@tool
def get_current_time(city: str = "New York") -> str:
    """Get the current time in a given city"""
    return f"The current time in {city} is {datetime.now().strftime('%H:%M:%S')}"


@tool
def get_weather(city: str = "Atlanta") -> str:
    """Get the weather in a given city"""
    return f"The weather in {city} is sunny."

@tool
def get_news(topic: str = "technology") -> str:
    """Get the news on a given topic"""
    return f"The news on {topic} is no news...Sorry"


load_dotenv()

agent = create_agent(
    model="gpt-4o-mini",
    tools=[get_current_time, get_weather, get_news],
    debug=False,
    system_prompt="you are a helpful assistant that can use tools to help the user. Please use to the tools first if the tools can help answer the user questions."
)

# This is just to show the graph of the agent.
# This agent has tools, so it will show the tools in the graph.
mermaid = agent.get_graph(xray=True).draw_mermaid_png()
with open("agent_graph_with_tools.png", "wb") as f:
    f.write(mermaid)


async def stream_agent():
    input = {"messages": [{"role": "user", "content": "What is the current time in Sydney?"}]}
    async for result in agent.astream(input, stream_mode="messages"):
        message = result[0]
        if isinstance(message, AIMessageChunk):
            print(result[0].content, end="", flush=True)

    print()  # Add a newline at the end



asyncio.run(stream_agent())