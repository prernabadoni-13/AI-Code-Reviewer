import subprocess
import json
from typing import Dict, Any
from .base import ReviewEngine
from .prompt_builder import build_project_review_prompt


class OllamaLLMEngine(ReviewEngine):

    def __init__(self, model: str = "phi3:mini"):
        self.model = model

    def _call_model(self, prompt: str) -> Dict[str, Any]:
        process = subprocess.Popen(
            ["ollama", "run", self.model],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        stdout, stderr = process.communicate(prompt)

        if stderr:
            raise RuntimeError(stderr.strip())

        return json.loads(stdout.strip())

    def review_project(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        prompt = build_project_review_prompt(project_data)
        return self._call_model(prompt)