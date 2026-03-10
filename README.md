# AI Code Reviewer

A CLI tool that reviews your code locally using Ollama — no API keys, no internet required.

## Prerequisites

### 1. Install Ollama
Download from https://ollama.com/download (Windows / Mac / Linux)

### 2. Pull a model
```bash
ollama pull phi3:mini
```

### 3. Install the tool
```bash
pip install -e .
```

---

## Usage
```bash
# Review current directory
ai-review review

# Review a specific path
ai-review review /path/to/project

# Use a different model
ai-review review --model codellama
```

---

## Configuration

| Method | Example |
|---|---|
| CLI flag | `ai-review review --model codellama` |
| Env var | `OLLAMA_MODEL=llama3 ai-review review` |

**Recommended models** (pull with `ollama pull <model>`):

| Model | Size | Notes |
|---|---|---|
| `phi3:mini` | ~2GB | Default, fast, lightweight |
| `codellama` | ~4GB | Better code understanding |
| `llama3` | ~5GB | Most capable |

---

## Troubleshooting

**` Ollama is not installed or not found in PATH`**
→ Install from https://ollama.com/download

**`Model returned no output`**
→ Make sure you've pulled the model: `ollama pull phi3:mini`

**`Model returned invalid JSON`**
→ Try a better model: `ai-review review --model codellama`