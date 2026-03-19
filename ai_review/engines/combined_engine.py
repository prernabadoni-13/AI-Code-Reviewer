from typing import Dict, Any
from .rule_engine import RuleBasedEngine
from .llm_engine import OllamaLLMEngine

class CombinedEngine:
    def __init__(self, model: str = None):
        self.rule_engine = RuleBasedEngine()
        self.llm_engine = OllamaLLMEngine(model=model)

    def review_project(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        # Step 1 — rule engine first (instant, no AI)
        rule_result = self.rule_engine.review_project(project_data)
        rule_issues = rule_result.get("issues", [])

        # tag rule issues with source
        for issue in rule_issues:
            issue["source"] = "rule-engine"

        # Step 2 — LLM gets code + rule findings so it doesn't repeat them
        llm_result = self.llm_engine.review_project(
            project_data,
            rule_issues=rule_issues
        )
        llm_issues = llm_result.get("issues", [])
        complexity = llm_result.get("complexity", [])

        # tag llm issues with source
        for issue in llm_issues:
            issue["source"] = "llm"

        # Step 3 — merge everything
        return {
            "issues": rule_issues + llm_issues,
            "complexity": complexity
        }