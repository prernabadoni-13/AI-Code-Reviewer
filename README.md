# AI Code Reviewer

A CLI tool that reviews your code locally using Ollama.

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

# Review using a specific model
ai-review review --model llama3.2

# Review a GitHub PR and post inline comments
ai-review pr https://github.com/owner/repo/pull/1

# Check setup and dependencies
ai-review setup

# See all commands
ai-review --help
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

## GitHub PR Integration

> A GitHub Personal Access Token is required for PR reviews.

### How to get a token:
1. Go to https://github.com/settings/tokens
2. Click **"Generate new token (classic)"**
3. Give it a name e.g. `ai-code-reviewer`
4. Tick the **`repo`** scope
5. Click **"Generate token"** and copy it

### Set the token:
```bash
# Mac/Linux (add to ~/.zshrc to make it permanent)
export GITHUB_TOKEN=your_token_here

# Windows
set GITHUB_TOKEN=your_token_here
```

### Then run:
```bash
ai-review pr https://github.com/owner/repo/pull/1
```
The tool will post inline comments on each issue directly on the PR! 

> The `ai-review review` command does NOT need a GitHub token — it works fully offline.

---

## Troubleshooting

**` Ollama is not installed or not found in PATH`**
→ Install from https://ollama.com/download

**`Model returned no output`**
→ Make sure you've pulled the model: `ollama pull phi3:mini`

**`Model returned invalid JSON`**
→ Try a better model: `ai-review review --model codellama`
