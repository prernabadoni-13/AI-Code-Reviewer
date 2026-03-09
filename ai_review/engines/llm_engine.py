import subprocess
import json
import os
from typing import Dict, Any
from .base import ReviewEngine
from .prompt_builder import build_project_review_prompt

class OllamaLLMEngine(ReviewEngine):
    def __init__(self, model: str = None):
        self.model = model or os.getenv("OLLAMA_MODEL", "phi3:mini")

    def _call_model(self, prompt: str) -> Dict[str, Any]:
        try:
            process = subprocess.Popen(
                ["ollama", "run", self.model],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8"
            )
            stdout, stderr = process.communicate(prompt)

            if not stdout.strip():
                raise RuntimeError(f"Model returned no output. stderr: {stderr}")

            # model sometimes wraps output in ```json ... ``` despite being told not to
            cleaned = stdout.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.split("```")[1]  # get content between fences
                if cleaned.startswith("json"):
                    cleaned = cleaned[4:]          # strip the "json" language tag
            return json.loads(cleaned.strip())

        except FileNotFoundError:
            raise RuntimeError(
                "\n❌ Ollama is not installed or not found in PATH.\n"
                "👉 Install it from: https://ollama.com/download\n"
                f"👉 Then run: ollama pull {self.model}"
            )
        except json.JSONDecodeError:
            raise RuntimeError(
                f"\n❌ Model returned invalid JSON.\n"
                f"Raw output: {repr(stdout[:300])}"
            )

    def review_project(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        prompt = build_project_review_prompt(project_data)
        return self._call_model(prompt)