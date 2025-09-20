# Textualize - Smart OCR Translation Workflow

One-click OCR and AI-powered smart translation for Alfred.

## Features

- Screen text recognition with CleanShot X
- Smart Universal Action: auto-detects word vs sentence
  - Single word: shows definition with IPA, meaning, example
  - Sentence/phrase: translates to Simplified Chinese
- AI powered by OpenAI, Claude, xAI, or Ollama (local)
- Hotkey triggered workflow
- Multiple model support
- Zero external dependencies

## Usage

### Hotkey (Screen Capture)

1. Press `Cmd + Shift + 1`
2. Select text area (CleanShot X launches)
3. View result

### Universal Action - Textualize

1. Select text anywhere
2. Trigger Alfred Universal Actions
3. Choose "Textualize"
4. View result (definition for single word, translation for sentence)

## Setup

### 1. Choose Model
- GPT-5 Mini (recommended)
- GPT-5
- GPT-5 Nano
- Sonnet 4
- Grok 4
- Ollama (Local)

### 2. Max Tokens
- Default: 1200
- Adjust based on your needs

### 3. Configure API Key / Ollama

**Cloud Models**: Add your API key based on chosen model:
- OpenAI: https://platform.openai.com/api-keys
- Claude: https://console.anthropic.com/
- xAI: https://console.x.ai/

**Ollama (Local)**:
- URL: Default `http://localhost:11434`
- Model: Default `translategemma`

## Requirements

- Alfred 5 with Powerpack
- macOS 10.15+
- CleanShot X (for hotkey mode)
- Python 3.7+
- Ollama (if using local models)

## License

MIT License - see [LICENSE](../LICENSE) file
