from langchain.agents import create_agent
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.types import Command

from tavily import TavilyClient
from typing import Literal
import os
from dotenv import load_dotenv
import asyncio
import logging


# This Human in the loop is working for accepted and rejected decisions.
# It is not working for edited decisions.

load_dotenv()
logging.getLogger("tavily").setLevel(logging.WARNING)

print("TAVILY_API_KEY: ", os.getenv("TAVILY_API_KEY"))

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "finance", "news"] = "general",
    include_raw_content: bool = False):
    """Search the internet for information on a given topic"""
    results = tavily_client.search(
        query=query,
        max_results=max_results,
        topic=topic,
        include_raw_content=include_raw_content
    )
    return results

# Correct middleware configuration
middleware_human_in_the_loop = [HumanInTheLoopMiddleware(
    interrupt_on={"internet_search": True},  # Fixed: Use True for default behavior
    description_prefix="Tool execution pending approval",
)]

agent = create_agent(
    model="gpt-4o-mini",
    checkpointer=InMemorySaver(),
    system_prompt="You are a helpful travel agent that can answer questions about various travel trips planning.",
    tools=[internet_search],
    middleware=middleware_human_in_the_loop,
)

async def stream_agent(user_input: str):
    input_messages = {"messages": [{"role": "user", "content": user_input}]}
    identifier = {"configurable": {"thread_id": "1"}}

    # Use stream_mode="values" for proper interrupt handling
    async for step in agent.astream(input_messages, identifier, stream_mode="values"):
        # Check for interruption
        if "__interrupt__" in step:
            interrupt = step["__interrupt__"][0]

            print(f"\n\n🛑 INTERRUPTION DETECTED:")
            print(f"Interrupt ID: {interrupt.id if hasattr(interrupt, 'id') else 'N/A'}")

            # Display action requests
            if hasattr(interrupt, 'value') and isinstance(interrupt.value, dict):
                action_requests = interrupt.value.get("action_requests", [])
                for request in action_requests:
                    print(f"\n{request.get('description', 'No description')}")
                    print(f"Tool: {request.get('name', 'Unknown')}")
                    print(f"Args: {request.get('arguments', {})}")

            # Ask for approval
            approval = input("\nApprove this action? (approve/reject/edit): ").strip().lower()

            if approval == "approve":
                # Resume with approval
                print("\n✅ Approving action...\n")
                async for resumed_step in agent.astream(
                    Command(resume={"decisions": [{"type": "approve"}]}),
                    identifier,
                    stream_mode="values"
                ):
                    # Handle resumed messages
                    if "messages" in resumed_step:
                        last_msg = resumed_step["messages"][-1]
                        if hasattr(last_msg, 'content'):
                            print(last_msg.content, end="", flush=True)

            elif approval == "reject":
                # Resume with rejection
                print("\n❌ Rejecting action...\n")
                rejection_reason = input("Reason for rejection: ").strip()
                async for resumed_step in agent.astream(
                    Command(resume={"decisions": [{"type": "reject", "feedback": rejection_reason}]}),
                    identifier,
                    stream_mode="values"
                ):
                    if "messages" in resumed_step:
                        last_msg = resumed_step["messages"][-1]
                        if hasattr(last_msg, 'content'):
                            print(last_msg.content, end="", flush=True)

            elif approval == "edit":
                # Resume with edited arguments
                print("\n✏️ Editing action...")
                print("Enter new query (or press Enter to keep original):")
                new_query = input().strip()

                if new_query:
                    # Get original action request
                    if hasattr(interrupt, 'value') and isinstance(interrupt.value, dict):
                        action_requests = interrupt.value.get("action_requests", [])
                        if action_requests:
                            original_action = action_requests[0]

                            # Create edited action with modified query
                            # Need to properly copy the nested structure
                            import copy
                            edited_action = copy.deepcopy(original_action)

                            # Update the query argument
                            if 'arguments' in edited_action:
                                edited_action['arguments']['query'] = new_query
                            elif 'args' in edited_action:
                                edited_action['args']['query'] = new_query
                            else:
                                # Debug: print structure if neither key exists
                                print(f"DEBUG: action structure = {original_action}")
                                print("Cannot find arguments field!")
                                continue

                            async for resumed_step in agent.astream(
                                Command(resume={"decisions": [{"type": "edit", "edited_action": edited_action}]}),
                                identifier,
                                stream_mode="values"
                            ):
                                if "messages" in resumed_step:
                                    last_msg = resumed_step["messages"][-1]
                                    if hasattr(last_msg, 'content'):
                                        print(last_msg.content, end="", flush=True)
                else:
                    print("No changes made, approving original...")
                    async for resumed_step in agent.astream(
                        Command(resume={"decisions": [{"type": "approve"}]}),
                        identifier,
                        stream_mode="values"
                    ):
                        if "messages" in resumed_step:
                            last_msg = resumed_step["messages"][-1]
                            if hasattr(last_msg, 'content'):
                                print(last_msg.content, end="", flush=True)

            break  # Exit after handling interrupt

        # Normal message handling
        elif "messages" in step:
            last_msg = step["messages"][-1]
            if hasattr(last_msg, 'type') and last_msg.type == "ai":
                if hasattr(last_msg, 'content'):
                    print(last_msg.content, end="", flush=True)

    print()  # Add a newline at the end


# Main loop
while True:
    print("\n>>> ", flush=True, end="")
    user_input = input()
    if user_input.strip().lower() == "exit":
        break
    asyncio.run(stream_agent(user_input))
