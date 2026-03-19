import json

def build_project_review_prompt(project_data: dict, rule_issues: list = None) -> str:
    project_json = json.dumps(project_data, indent=2)
    rule_findings = json.dumps(rule_issues or [], indent=2)

    return f"""
You are a strict code review engine.

The following issues have ALREADY been identified by a rule-based engine.
DO NOT repeat these. Focus ONLY on deeper issues like logic errors,
security vulnerabilities, bad patterns, and improvements.

ALREADY FOUND ISSUES (do not repeat):
{rule_findings}

STRICT RULES:
- Return ONLY valid JSON. No markdown. No explanation. No text before or after.
- Only report issues that ACTUALLY exist in the provided code.
- Each file has a "path" field — use the file extension to determine the language.
- Do NOT apply Python rules to Java files and vice versa.
- Line numbers must be EXACT — count the actual lines in the code provided.
- Do NOT invent errors. Do NOT assume code that isn't there.
- Do NOT repeat any issue already listed in ALREADY FOUND ISSUES above.

Also analyze the complexity of each file and function:
- Score each function from 1-10 (1=simple, 10=very complex)
- Flag anything above 6 as needing refactoring

OUTPUT FORMAT (follow exactly):
{{
  "issues": [
    {{
      "file": "exact filename",
      "line": 1,
      "severity": "error",
      "message": "description"
    }}
  ],
  "complexity": [
    {{
      "file": "exact filename",
      "function": "function or method name",
      "line": 1,
      "score": 7,
      "message": "Too many nested conditions, consider breaking into smaller functions"
    }}
  ]
}}

Severity must be one of: "error", "warning", "info"
Complexity score must be a number from 1-10.

CODE TO REVIEW:
{project_json}
""".strip()