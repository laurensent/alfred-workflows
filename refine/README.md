# Refine

Rewrite text to sound more natural and native using AI.

## Features

- Automatically selects all text or uses current selection
- Rewrites using AI to sound like a native speaker
- Multi-language support with auto-detect or specific target language
- Supports multiple AI providers: Claude, OpenAI, Gemini, Ollama
- Context-aware rewriting for different platforms
- History logging to SQLite database

## Usage

1. Open the workflow settings in Alfred
2. Select your preferred AI model and add the required API key
3. Set your preferred hotkey (default: Cmd+Option+R)
4. Focus on any text input field
5. Press the hotkey
6. The text will be rewritten and automatically replaced

## Configuration

| Option | Description |
|--------|-------------|
| Choose Model | Select from various AI models |
| Context | Optimize for specific platforms |
| Target Language | Auto (same as input) or choose a specific language |
| Selection Mode | Select All & Replace or Selection Only |
| Output Mode | Paste directly, Copy only, or Show in Large Type |
| Max Tokens | Maximum tokens for AI response (default: 500) |
| Temperature | Controls randomness: 0=deterministic, 1+=creative (default: 0.7) |
| Save History | Enable/disable saving rewrites to database |
| Database Folder | Folder for history.db |
| API Keys | OpenAI, Claude, Gemini API keys |
| Ollama URL | Server address (default: http://localhost:11434) |
| Ollama Model | Local model name (default: translategemma) |

### Contexts

| Context | Description |
|---------|-------------|
| General | Default, clean and natural |
| Casual | Contractions OK, natural informal |
| Reddit/Social | Brief and direct, keeps abbreviations |
| Tech/Dev/GitHub | Preserves technical terms and code |
| Business | Professional but not stiff |

### Providers

| Provider | API Key Required | Notes |
|----------|-----------------|-------|
| Claude | Yes | Anthropic API |
| OpenAI | Yes | OpenAI API |
| Gemini | Yes | Google AI API |
| Ollama | No | Runs locally |

## Requirements

- Alfred 5 with Powerpack
- Python 3
- API key for your chosen provider (except Ollama)

## License

MIT License - see [LICENSE](../LICENSE) file
