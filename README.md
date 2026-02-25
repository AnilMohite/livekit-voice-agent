# LiveKit Voice AI Agent

Voice AI assistant with Python. Build a real-time voice agent that can listen, understand, and respond to users using AI models.

## Install uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy BypassUser -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or use pip
pip install uv
```

## Setup

Create `.env.local` file with:
```
LIVEKIT_API_KEY=your_api_key
LIVEKIT_API_SECRET=your_api_secret
LIVEKIT_URL=your_livekit_url
OPENAI_API_KEY=your_openai_key
```

Install dependencies:
```bash
uv add "livekit-agents[silero,turn-detector]~=1.4" "livekit-plugins-noise-cancellation~=0.2" "python-dotenv"
uv run agent.py download-files
```

## Run
```bash
uv run agent.py console    # Local testing
uv run agent.py dev        # Connect to cloud
uv run agent.py start      # Production
```

## Deploy
```bash
lk agent create
```

[Docs](https://docs.livekit.io/agents/start/voice-ai-quickstart/)