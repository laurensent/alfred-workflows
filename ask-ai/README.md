# Ask AI

Alfred workflow for AI conversations with multi-provider support.

## Features

- **Multi-provider**: OpenAI, Anthropic, Google Gemini, Ollama
- **Conversation history**: SQLite storage with auto-cleanup
- **Web search**: AI-driven search (optional)
- **Extended thinking**: For reasoning models (optional)

## Usage

- `aa [question]` - Ask a question or continue conversation
- `ah` - View/search conversation history
- `Cmd+Option+I` - Quick access hotkey
- `Cmd+Option+H` - History hotkey

### History Actions

- `Enter` - Continue selected conversation
- `Cmd+Enter` - Delete selected conversation

## Supported Models

| Provider | Models |
|----------|--------|
| OpenAI | GPT-4.1, GPT-4.1 mini/nano, GPT-5.1, GPT-5 mini/nano |
| Anthropic | Claude Sonnet 4.5, Claude Haiku 4.5, Claude Opus 4.5 |
| Google | Gemini 3 Pro, Gemini 2.5 Pro/Flash/Flash-Lite |
| Ollama | Any local model |

## Configuration

**Required**:
- `model` - Select AI model (provider:model format)
- API Key for chosen provider (OpenAI/Anthropic/Google)

**Optional**:
- `keep_history` - Save current chat when starting a new one
- `enable_web_search` - Enable AI-driven web search
- `search_api_key` - Brave Search API key for web search
- `enable_thinking` - Enable extended thinking mode
- `max_context_tokens` - Max tokens for context (default: 8000)
- `auto_delete_months` - Auto-delete old conversations (0 = disabled)

**Ollama**:
- `ollama_model` - Model name
- `ollama_host` - Server URL (default: http://localhost:11434)

## Requirements

- Alfred 5 with Powerpack
- Python 3
- API key for chosen provider

## License

MIT
