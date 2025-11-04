import os
from dotenv import load_dotenv
from langchain.agents import create_agent


load_dotenv()


agent = create_agent(
    model="gpt-4o-mini",
    tools=[],
    debug=False,   
)

from IPython.display import Image, display
mermaid = agent.get_graph(xray=True).draw_mermaid_png()
with open("agent_graph.png", "wb") as f:
    f.write(mermaid)

display(Image(mermaid))

input = {"messages": [{"role": "user", "content": "What is the capital of USA?"}]}
results = agent.stream(
    input,
    stream_mode="values"
    )


for chunk in results:
    print(chunk.get("messages")[-1].content)