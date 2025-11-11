from dotenv import load_dotenv

from langchain.agents import create_agent
from langgraph.checkpoint.redis import AsyncRedisSaver
import asyncio
import logging
import os

load_dotenv()
logging.getLogger("langgraph.checkpoint.redis").setLevel(logging.WARNING)
logging.getLogger("redisvl.index.index").setLevel(logging.WARNING)
logging.getLogger("redis").setLevel(logging.WARNING)

DB_URI = os.getenv("REDIS_URL")

async def main():

    # Set the Redis checkpointer.
    async with (
        AsyncRedisSaver.from_conn_string(DB_URI) as checkpointer_redis,
    ):
        await checkpointer_redis.setup()

        # Set TTL strategy is not available unless you are using langgraph.json file.
        #await checkpointer_redis.ttl.set_ttl_strategy("delete", sweep_interval_minutes=10, default_ttl=43200)


        # Create the agent with the Redis checkpointer.
        agent = create_agent(
        model="gpt-4o-mini",
        system_prompt="You are an AI chatbot that will response to user query.",
        checkpointer=checkpointer_redis,
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
        await stream_agent(user_input)

if __name__ == "__main__":
    asyncio.run(main())