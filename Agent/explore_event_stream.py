import os
import asyncio
from dotenv import load_dotenv
from langchain.agents import create_agent


load_dotenv()


agent = create_agent(
    model="gpt-4o-mini",
    tools=[],
    debug=False,
)


async def stream_agent_response():
    """Stream the agent's response token-by-token as it's generated."""
    input = {"messages": [{"role": "user", "content": "Write me a poem about a cat?"}]}

    # Use astream_events for true token-level streaming
    async for event in agent.astream_events(input, version="v2"):
        kind = event["event"]

        # Stream tokens from the LLM as they arrive
        if kind == "on_chat_model_stream":
            content = event["data"]["chunk"].content
            if content:
                print(content, end="", flush=True)

    print()  # Add a newline at the end


async def explore_event_structure():
    """Explore what's inside the event object."""
    input = {"messages": [{"role": "user", "content": "What is the capital of USA?"}]}

    async for event in agent.astream_events(input, version="v2"):
        print("\n" + "="*60)
        print(f"Event Type: {event['event']}")
        print(f"Event Keys: {list(event.keys())}")

        # Show what's in the data
        if "data" in event:
            print(f"Data Keys: {list(event['data'].keys())}")

        # For streaming events, show the chunk structure
        if event['event'] == "on_chat_model_stream":
            chunk = event["data"]["chunk"]
            print(f"Chunk Type: {type(chunk)}")
            print(f"Chunk Content: {chunk.content}")
            print(f"Chunk: {chunk}")

        # Show first few events in full
        import json
        print(f"\nFull Event (first 500 chars):")
        print(json.dumps(event, indent=2, default=str)[:500])

async def explore_astream_structure():
    """Explore the structure of astream() with different stream modes."""
    input = {"messages": [{"role": "user", "content": "What is the capital of USA?"}]}

    print("=== Exploring astream with stream_mode='messages' ===\n")

    async for event in agent.astream(input, stream_mode="messages"):
        print(f"Event Type: {type(event)}")
        print(f"Event: {event}")

        # If it's a tuple with metadata
        if isinstance(event, tuple):
            print(f"Tuple Length: {len(event)}")
            for i, item in enumerate(event):
                print(f"  Item {i}: {type(item)} = {item}")

        # If it's a message object
        if hasattr(event, '__class__'):
            print(f"Class: {event.__class__.__name__}")
            print(f"Attributes: {dir(event)}")
            if hasattr(event, 'content'):
                print(f"Content: {event.content}")

        print("-" * 60)

async def explore_all_stream_modes():
    """Explore all available stream_mode options for astream()."""
    input = {"messages": [{"role": "user", "content": "What is 2+2?"}]}

    # Available stream modes: "values", "updates", "messages", "custom", "debug"
    stream_modes = ["values", "updates", "messages"]

    for mode in stream_modes:
        print(f"\n{'='*60}")
        print(f"Stream Mode: {mode}")
        print('='*60)

        try:
            event_count = 0
            async for event in agent.astream(input, stream_mode=mode):
                event_count += 1
                print(f"\nEvent #{event_count}")
                print(f"Type: {type(event)}")

                # Handle different types
                if isinstance(event, dict):
                    print(f"Keys: {list(event.keys())}")
                    print(f"Content: {event}")
                elif isinstance(event, tuple):
                    print(f"Tuple length: {len(event)}")
                    print(f"Content: {event}")
                elif hasattr(event, 'content'):
                    print(f"Class: {event.__class__.__name__}")
                    print(f"Content: {event.content}")
                else:
                    print(f"Raw: {event}")

                print("-" * 40)

            print(f"\nTotal events in '{mode}' mode: {event_count}")

        except Exception as e:
            print(f"Error with stream_mode='{mode}': {e}")

# Run the async streaming function
if __name__ == "__main__":
    print("Choose an exploration mode:\n")
    print("1. Token-by-token streaming (astream_events)")
    print("2. Explore astream_events structure")
    print("3. Explore astream with 'messages' mode")
    print("4. Explore all astream stream_modes\n")

    choice = input("Enter choice (1-4, or press Enter for #1): ").strip() or "1"

    if choice == "1":
        asyncio.run(stream_agent_response())
    elif choice == "2":
        asyncio.run(explore_event_structure())
    elif choice == "3":
        asyncio.run(explore_astream_structure())
    elif choice == "4":
        asyncio.run(explore_all_stream_modes())
    else:
        print("Invalid choice. Running option 1 by default.")
        asyncio.run(stream_agent_response())