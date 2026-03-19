import requests
import json
import os
from typing import Dict, Any
from .base import ReviewEngine
from .prompt_builder import build_project_review_prompt

class OllamaLLMEngine(ReviewEngine):

    def __init__(self, model: str = None):
        self.model = model or os.getenv("OLLAMA_MODEL", "llama3.2")

    def _call_model(self, prompt: str) -> Dict[str, Any]:
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": 2048,  # allow longer responses
                        "temperature": 0.1    # less creative = less hallucination
                    }
                }
            )

            result = response.json()
            stdout = result.get("response", "")

            if not stdout.strip():
                raise RuntimeError("Model returned no output")

            # strip markdown fences if model adds them
            cleaned = stdout.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.split("```")[1]
                if cleaned.startswith("json"):
                    cleaned = cleaned[4:]

            return json.loads(cleaned.strip())

        except requests.exceptions.ConnectionError:
            raise RuntimeError(
                "\n❌ Ollama is not running.\n"
                "👉 Start it with: ollama serve\n"
                f"👉 Then pull model: ollama pull {self.model}"
            )
        except json.JSONDecodeError:
            raise RuntimeError(
                f"\n❌ Model returned invalid JSON.\n"
                f"Raw output: {repr(stdout[:300])}"
            )

    def review_project(self, project_data: Dict[str, Any], rule_issues: list = None) -> Dict[str, Any]:
        prompt = build_project_review_prompt(project_data, rule_issues or [])
        return self._call_model(prompt)