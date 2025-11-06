# LangChain v1 Simple Agent

A demonstration project showcasing agent implementations using LangChain v1 with OpenAI's GPT-4o-mini model.

## Overview

This project demonstrates building AI agents using LangChain's latest v1 API. It includes:
- A simple agent implementation with graph visualization
- A DeepAgent implementation with Tavily search integration for advanced research capabilities

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

## Prerequisites

- Python 3.12 or higher
- OpenAI API key
- Tavily API key (for DeepAgent)
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

## Project Structure

```
langchain_v1/
├── Agent/
│   ├── .env                 # Environment variables (not tracked in git)
│   └── simple_agent.py      # Simple agent implementation
├── DeepAgent/
│   ├── .env                 # Environment variables (not tracked in git)
│   └── deep_agent.py        # DeepAgent with Tavily integration
├── .venv/                   # Virtual environment (not tracked in git)
├── agent_graph.png          # Generated agent graph visualization
├── pyproject.toml           # Project dependencies and metadata
├── uv.lock                  # Locked dependencies
├── .python-version          # Python version specification
├── .gitignore               # Git ignore rules
└── README.md                # This file
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

## Dependencies

### Core Dependencies
- **langchain** (>=1.0.3): Core LangChain framework
- **langchain-openai** (>=1.0.2): OpenAI integration for LangChain
- **python-dotenv** (>=1.0.0): Environment variable management
- **ipython** (>=9.6.0): Interactive Python shell and display utilities

### DeepAgent Additional Dependencies
- **tavily-python**: Tavily search API integration for web research
- **langchain-community**: Community integrations including Tavily search tool

## Development

This project uses:

- **uv**: Fast Python package installer and resolver
- **Python 3.12**: Latest Python features and performance improvements

## Notes

- **Simple Agent**: Minimal implementation with no additional tools, serves as a foundation for understanding LangChain v1
- **DeepAgent**: Advanced implementation with Tavily search integration for research-based tasks
- Graph visualization requires IPython's display utilities
- Both agents use GPT-4o-mini for efficient and cost-effective operation

## Next Steps

Potential enhancements:

- Add custom tools to extend agent capabilities
- Implement conversation memory for context-aware interactions
- Add error handling and retry logic
- Create more complex agent workflows
- Integrate with different LLM models
- Expand DeepAgent with additional research tools
- Add multi-turn conversation support

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]
