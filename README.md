# LangChain v1 Simple Agent

A demonstration project showcasing agent implementations using LangChain v1 with OpenAI's GPT-4o-mini model.

## Overview

This project demonstrates building AI agents using LangChain's latest v1 API. It includes:
- A simple agent implementation with graph visualization
- A DeepAgent implementation with Tavily search integration for advanced research capabilities
- A memory-enabled agent with conversation history tracking

## Features

### Simple Agent
- Simple agent implementation using LangChain v1
- Integration with OpenAI's GPT-4o-mini model
- Agent graph visualization using Mermaid diagrams
- Streaming response support
- Environment-based configuration

### DeepAgent
- Advanced research agent with Tavily search integration
- Multi-source information retrieval and synthesis
- Enhanced reasoning capabilities
- Structured research workflows

### Agent Memory
- Conversation history tracking using checkpointer
- Thread-based memory management
- Streaming response support with async/await
- Interactive chat interface with persistent memory
- Two implementations:
  - **InMemorySaver**: In-memory storage for experimentation
  - **AsyncRedisSaver**: Redis-based persistent storage for production
- Logging configuration to suppress verbose output

## Prerequisites

- Python 3.12 or higher
- OpenAI API key
- Tavily API key (for DeepAgent)
- Redis server (for Agent Memory with Redis)
- [uv](https://github.com/astral-sh/uv) package manager (recommended) or pip

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd langchain_v1
```

### 2. Install dependencies using uv

```bash
uv sync
```

Or using pip:

```bash
pip install -r requirements.txt
```

## Configuration

### Simple Agent Configuration

#### 1. Create a `.env` file in the `Agent` directory

```bash
cd Agent
cp .env.example .env  # Or create manually
```

#### 2. Add your OpenAI API key to the `.env` file

```env
OPENAI_API_KEY=your_api_key_here
```

### DeepAgent Configuration

#### 1. Create a `.env` file in the `DeepAgent` directory

```bash
cd DeepAgent
cp .env.example .env  # Or create manually
```

#### 2. Add your API keys to the `.env` file

```env
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### Agent Memory Configuration

#### 1. Create a `.env` file in the `Agent_Memory` directory

```bash
cd Agent_Memory
cp .env.example .env  # Or create manually
```

#### 2. Add your OpenAI API key to the `.env` file

For InMemorySaver (basic):
```env
OPENAI_API_KEY=your_api_key_here
```

For AsyncRedisSaver (production):
```env
OPENAI_API_KEY=your_api_key_here
REDIS_URL=redis://localhost:6379
```

#### 3. Install and start Redis (for Redis-based implementation)

**macOS (using Homebrew):**
```bash
brew install redis
brew services start redis
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install redis-server
sudo systemctl start redis-server
```

**Docker:**
```bash
docker run -d -p 6379:6379 redis:latest
```

## Usage

### Running Simple Agent

```bash
uv run Agent/simple_agent.py
```

The agent will:

1. Generate and save a visualization of the agent graph to `agent_graph.png`
2. Process a sample question: "What is the capital of USA?"
3. Stream the response to the console

#### Example Output

```text
The capital of the USA is Washington, D.C.
```

### Running DeepAgent

```bash
uv run DeepAgent/deep_agent.py
```

The DeepAgent will:

1. Use Tavily search to gather information from multiple sources
2. Synthesize and analyze the retrieved information
3. Provide comprehensive research-based responses

### Running Agent Memory

#### InMemorySaver Implementation (Basic)

```bash
uv run Agent_Memory/agent_memory.py
```

The Agent Memory will:

1. Start an interactive chat session with conversation history
2. Remember previous messages within the same thread (in RAM)
3. Stream responses in real-time using async/await
4. Maintain context across multiple interactions

**Note**: Memory is lost when the program exits.

#### AsyncRedisSaver Implementation (Production)

```bash
# Make sure Redis is running first
uv run Agent_Memory/agent_memory_redis.py
```

The Redis-based Agent Memory provides:

1. **Persistent Storage**: Conversations survive application restarts
2. **Cross-session Memory**: Resume conversations from any session
3. **Production-ready**: Suitable for real-world deployments
4. **Configurable Logging**: Suppresses verbose Redis logs

#### Example Conversation

```text
>>> Hi! My name is Bob.
Hello Bob! Nice to meet you. How can I help you today?
>>> What's my name?
Your name is Bob, as you just told me!
>>> exit
```

#### Key Features

**Both Implementations:**
- **Thread-based Memory**: Conversations are stored using a thread ID
- **Async Streaming**: Real-time response streaming for better UX
- **Interactive Loop**: Continuous chat until user types "exit"

**InMemorySaver:**
- Stores conversation in RAM (for testing only)
- No external dependencies
- Data lost on exit

**AsyncRedisSaver:**
- Persistent storage in Redis
- Production-ready
- Data survives restarts
- Configurable logging

#### Production Considerations

**TTL (Time-to-Live) Cleanup:**

The `langgraph.json` file contains TTL configuration, but it's **only active when using LangGraph Platform** (`langgraph dev` or `langgraph up`). For standalone Python scripts:

- TTL configuration is **not available** via Python API
- Use Redis server-level eviction policies for memory management
- Implement manual cleanup scripts for old conversations

**Redis Memory Management:**

Configure Redis `maxmemory-policy` in `redis.conf`:
```conf
maxmemory 2gb
maxmemory-policy allkeys-lru  # Evict least recently used keys
```

**Alternative Production Checkpointers:**

For SQL-based persistence:
```python
from langgraph.checkpoint.postgres import PostgresSaver

checkpointer = PostgresSaver(connection_string="postgresql://...")
```

## Project Structure

```
langchain_v1/
├── Agent/
│   ├── .env                     # Environment variables (not tracked in git)
│   └── simple_agent.py          # Simple agent implementation
├── DeepAgent/
│   ├── .env                     # Environment variables (not tracked in git)
│   └── deep_agent.py            # DeepAgent with Tavily integration
├── Agent_Memory/
│   ├── .env                     # Environment variables (not tracked in git)
│   ├── agent_memory.py          # Agent with InMemorySaver
│   └── agent_memory_redis.py    # Agent with AsyncRedisSaver (production)
├── .venv/                       # Virtual environment (not tracked in git)
├── agent_graph.png              # Generated agent graph visualization
├── pyproject.toml               # Project dependencies and metadata
├── uv.lock                      # Locked dependencies
├── .python-version              # Python version specification
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

## How It Works

### Simple Agent

The [simple_agent.py](Agent/simple_agent.py) demonstrates:

1. **Agent Creation**: Uses `create_agent()` from LangChain to instantiate an agent with GPT-4o-mini
2. **Graph Visualization**: Generates a Mermaid diagram showing the agent's execution flow
3. **Message Streaming**: Processes user input and streams responses in real-time

#### Agent Graph

The agent generates a visual representation of its execution graph:

![Agent Graph](agent_graph.png)

This diagram shows the internal workflow of how the agent processes messages.

### DeepAgent

The [deep_agent.py](DeepAgent/deep_agent.py) demonstrates:

1. **Tavily Integration**: Leverages Tavily's search API for comprehensive web research
2. **Multi-Source Research**: Retrieves and synthesizes information from multiple authoritative sources
3. **Enhanced Reasoning**: Combines search results with GPT-4o-mini's reasoning capabilities
4. **Structured Responses**: Provides well-organized, research-backed answers

### Agent Memory

Two implementations are provided:

#### [agent_memory.py](Agent_Memory/agent_memory.py) - InMemorySaver

1. **In-Memory Storage**: Uses `InMemorySaver` for RAM-based conversation persistence
2. **Thread Management**: Each conversation is tracked using a unique `thread_id`
3. **Async Streaming**: Implements `astream()` for real-time response streaming
4. **Interactive Chat Loop**: Continuous conversation until user exits
5. **No External Dependencies**: Works out of the box without additional setup

#### [agent_memory_redis.py](Agent_Memory/agent_memory_redis.py) - AsyncRedisSaver

1. **Persistent Storage**: Uses `AsyncRedisSaver` for Redis-based conversation persistence
2. **Production-Ready**: Conversations survive application restarts
3. **Async Context Manager**: Proper Redis connection management with `async with`
4. **Logging Configuration**: Suppresses verbose Redis and LangGraph logs
5. **Setup Required**: Must call `await checkpointer.setup()` for initialization

#### Code Breakdown

**InMemorySaver (Basic):**
```python
# Create agent with InMemorySaver
agent = create_agent(
    model="gpt-4o-mini",
    system_prompt="You are an AI chatbot that will response to user query.",
    checkpointer=InMemorySaver(),  # In-memory storage
    debug=False
)

# Stream responses
async def stream_agent(user_input: str):
    input = {"messages": [{"role": "user", "content": user_input}]}
    identifier = {"configurable": {"thread_id": "1"}}

    async for results in agent.astream(input, identifier, stream_mode="messages"):
        print(f"{results[0].content}", end="", flush=True)
```

**AsyncRedisSaver (Production):**
```python
import logging

# Suppress Redis logging
logging.getLogger("langgraph.checkpoint.redis").setLevel(logging.WARNING)
logging.getLogger("redisvl.index.index").setLevel(logging.WARNING)
logging.getLogger("redis").setLevel(logging.WARNING)

async def main():
    # Create Redis checkpointer
    async with AsyncRedisSaver.from_conn_string(DB_URI) as checkpointer_redis:
        await checkpointer_redis.setup()  # Required setup

        agent = create_agent(
            model="gpt-4o-mini",
            system_prompt="You are an AI chatbot that will response to user query.",
            checkpointer=checkpointer_redis,  # Redis storage
            debug=False
        )

        # Stream responses (same as InMemorySaver)
        async def stream_agent(user_input: str):
            input = {"messages": [{"role": "user", "content": user_input}]}
            identifier = {"configurable": {"thread_id": "1"}}

            async for results in agent.astream(input, identifier, stream_mode="messages"):
                print(f"{results[0].content}", end="", flush=True)
```

**Key Concepts:**

- **Checkpointer**: Saves conversation state at each step (in-memory or Redis)
- **Thread ID**: Unique identifier for each conversation thread
- **Config Parameter**: Second positional argument containing `{"configurable": {"thread_id": "..."}}`
- **Stream Mode**: `"messages"` mode streams individual message chunks for real-time display
- **Async Context Manager** (Redis): Ensures proper connection cleanup with `async with`
- **Setup Method** (Redis): Must call `await checkpointer.setup()` before use
- **Logging Control** (Redis): Configure logging levels to suppress verbose output

## Dependencies

### Core Dependencies
- **langchain** (>=1.0.3): Core LangChain framework
- **langchain-openai** (>=1.0.2): OpenAI integration for LangChain
- **python-dotenv** (>=1.0.0): Environment variable management
- **ipython** (>=9.6.0): Interactive Python shell and display utilities

### DeepAgent Additional Dependencies
- **tavily-python**: Tavily search API integration for web research
- **langchain-community**: Community integrations including Tavily search tool

### Agent Memory Additional Dependencies
- **langgraph-checkpoint-redis**: Redis-based checkpointer for persistent conversation storage
- **redis**: Redis client for Python (automatically installed with langgraph-checkpoint-redis)

## Development

This project uses:

- **uv**: Fast Python package installer and resolver
- **Python 3.12**: Latest Python features and performance improvements

## Notes

- **Simple Agent**: Minimal implementation with no additional tools, serves as a foundation for understanding LangChain v1
- **DeepAgent**: Advanced implementation with Tavily search integration for research-based tasks
- **Agent Memory**: Demonstrates conversation persistence using checkpointers and thread-based memory management
  - `agent_memory.py`: InMemorySaver for experimentation (no external dependencies)
  - `agent_memory_redis.py`: AsyncRedisSaver for production (requires Redis server)
- Graph visualization requires IPython's display utilities
- All agents use GPT-4o-mini for efficient and cost-effective operation
- Redis-based implementation includes logging configuration to suppress verbose output
- TTL configuration in `langgraph.json` only works with LangGraph Platform, not standalone scripts

## Next Steps

Potential enhancements:

- Add custom tools to extend agent capabilities
- ✅ ~~Implement conversation memory for context-aware interactions~~ (Completed in Agent_Memory)
- ✅ ~~Add Redis-based persistent storage~~ (Completed in agent_memory_redis.py)
- Implement PostgresSaver for SQL-based persistence
- Add RedisStore for long-term cross-thread memory
- Implement TTL cleanup scripts for standalone Redis deployments
- Add error handling and retry logic
- Create more complex agent workflows
- Integrate with different LLM models
- Expand DeepAgent with additional research tools
- Add multi-thread conversation management with user-specific namespaces
- Implement conversation history export/import functionality
- Add conversation summarization for long-running threads

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]
