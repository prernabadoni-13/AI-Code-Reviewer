import json

def build_project_review_prompt(project_data: dict) -> str:
    project_json = json.dumps(project_data, indent=2)

    return f"""
You are a strict code review engine. Review the code below and return ONLY a JSON object.

STRICT RULES:
- Return ONLY valid JSON. No markdown. No explanation. No text before or after.
- Only report issues that ACTUALLY exist in the provided code.
- Do NOT invent code that isn't there. Do NOT assume variables or imports.
- Do NOT review imaginary code. Only review what is shown below.
- If there are no issues, return {{"issues": []}}

OUTPUT FORMAT (follow exactly):
{{
  "issues": [
    {{
      "file": "filename.py",
      "line": 1,
      "severity": "error",
      "message": "description of the issue"
    }}
  ]
}}

Severity must be one of: "error", "warning", "info"

CODE TO REVIEW:
{project_json}
""".strip()