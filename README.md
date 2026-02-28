# LiveKit Voice AI Agent

A collection of real-time voice AI agents built with Python and LiveKit. These agents can listen, understand, and respond to users using advanced AI models with features like noise cancellation, turn detection, and metrics collection.

## Features

- **Real-time Voice Interaction**: Live audio streaming with low-latency response
- **Multiple AI Models**: Integration with OpenAI, Google, Deepgram, and AssemblyAI
- **Fallback Adapters**: Automatic failover between multiple STT, LLM, and TTS providers
- **Noise Cancellation**: Advanced audio preprocessing for clear speech recognition
- **Metrics Collection**: Monitor agent performance and API usage
- **Turn Detection**: Multilingual turn detection for natural conversations

## Project Structure

- **`agent.py`** - Basic voice agent with OpenAI GPT-4 and Cartesia TTS
- **`agent-with-fallback-adapter.py`** - Enhanced agent with fallback providers (Deepgram/AssemblyAI for STT, Google Gemini fallback for LLM, Google TTS fallback)
- **`agent-with-metrics-collection.py`** - Production-ready agent with metrics collection, performance monitoring, and usage tracking
- **`agent-with-tools-and-mcp.py`** - Advanced agent with custom function tools, MCP (Model Context Protocol) server integration for LiveKit documentation search, and real-time weather lookup

## Prerequisites

- Python 3.13+
- LiveKit server (sign up at [livekit.io](https://livekit.io))
- API keys for:
  - OpenAI (or Google Gemini)
  - Deepgram or AssemblyAI (for STT)
  - Cartesia or Google (for TTS)

## Installation

### Install uv Package Manager

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy BypassUser -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or use pip
pip install uv
```

## Setup

### 1. Configure Environment Variables

Create a `.env.local` file in the project root:

```bash
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_api_secret
LIVEKIT_URL=wss://your-livekit-instance.com
OPENAI_API_KEY=your_openai_api_key
DEEPGRAM_API_KEY=your_deepgram_api_key
ASSEMBLYAI_API_KEY=your_assemblyai_api_key
CARTESIA_API_KEY=your_cartesia_api_key
GOOGLE_API_KEY=your_google_api_key
```

### 2. Install Dependencies

Install required packages:

```bash
uv sync
```

Or install dependencies with pip:

```bash
uv add "livekit-agents[silero,turn-detector]~=1.3" "livekit-plugins-noise-cancellation~=0.2" "python-dotenv"
```

### 3. Download Required Files

```bash
uv run agent.py download-files
```

## Usage

### Run Locally

Choose which agent implementation to run:

```bash
# Basic agent
uv run agent.py console

# Agent with fallback providers
uv run agent-with-fallback-adapter.py console

# Agent with metrics collection
uv run agent-with-metrics-collection.py console

# Agent with tools and MCP servers
uv run agent-with-tools-and-mcp.py console
```

### Connect to LiveKit Cloud

```bash
# Connect to your cloud instance
uv run agent.py dev
```

### Run in Production

```bash
# Production mode
uv run agent.py start
```

## Deployment

Deploy your agent to LiveKit Cloud:

```bash
lk agent create
```

For detailed deployment instructions, see the [LiveKit Agents Documentation](https://docs.livekit.io/agents/start/voice-ai-quickstart/).

## Configuration

### Custom Instructions

Edit the `instructions` parameter in the `Assistant` class to customize agent behavior:

```python
class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="Your custom instructions here.",
        )
```

### AI Model Selection

Modify the `AgentSession` configuration to change AI providers:

- **STT**: `deepgram/nova-3:multi`, `assemblyai/assemblyai-1:multi`
- **LLM**: `openai/gpt-4.1-mini`, `google/gemini-2.5-flash`
- **TTS**: `cartesia/sonic-3:...`, `google/tts:multi`

## Tools and MCP Integration

The `agent-with-tools-and-mcp.py` includes advanced capabilities:

### Function Tools
- **`get_current_weather`**: Look up real-time weather for any location using Open-Meteo API (no API key required)

### MCP Servers
- **LiveKit Documentation Server**: Provides intelligent search and retrieval of LiveKit documentation to answer questions about features, APIs, and implementation patterns

The agent automatically uses these tools when needed based on user queries. For example:
- "What's the weather in San Francisco?" → Uses the weather tool
- "How do I implement real-time translation?" → Queries the LiveKit docs MCP server

## Session Reports and Metrics

The `agent-with-metrics-collection.py` automatically generates session reports and collects metrics stored in a **local `reports/` folder**:

- **Session Reports**: Generated at the end of each session and saved to `./reports/` directory as JSON files
- **Report Filename Format**: `session_report_{room_name}_{timestamp}.json`
- **Metrics Collection**: Real-time tracking of:
  - STT/LLM/TTS latencies
  - Token usage and costs
  - Agent state transitions
  - Time to first audio response
  - End-of-utterance (EOU) metrics

All session data is stored locally in the `reports/` folder for easy access and analysis. Reports persist after session ends for historical tracking and performance analysis.

## Troubleshooting

### Windows Path Issues
If you encounter `FileNotFoundError` for `/tmp/`, the code now automatically creates a `reports/` directory in your project root for cross-platform compatibility.

### Missing API Keys
Ensure all required environment variables are set in `.env.local`:
- Check that your API keys are valid and have appropriate permissions
- Verify the `LIVEKIT_URL` is accessible from your machine

### Fallback Providers
If using `agent-with-fallback-adapter.py`:
- The first STT model (Deepgram) will attempt first; if it fails, AssemblyAI will be used
- The LLM will fall back to Google Gemini if the primary OpenAI model fails
- TTS will fall back to Google if Cartesia is unavailable

## Documentation

- [LiveKit Agents Documentation](https://docs.livekit.io/agents/start/voice-ai-quickstart/)
- [LiveKit Voice SDK](https://github.com/livekit/livekit-agents)
- [Deepgram STT Documentation](https://developers.deepgram.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)

## License

MIT License - Feel free to use this project for your own applications.