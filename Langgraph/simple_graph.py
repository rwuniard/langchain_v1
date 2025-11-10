from langgraph.graph import StateGraph, START, END, MessagesState


def mock_llm(state: MessagesState):
    return {"messages": [{"role": "assistant", "content": "Hello World, bla bla bla..."}]}


graph = StateGraph(MessagesState)
graph.add_node(mock_llm)
graph.add_edge(START, "mock_llm")
graph.add_edge("mock_llm", END)
graph = graph.compile()

result = graph.invoke({"messages": [{"role": "user", "content": "Hi!?"}]})
print(result)