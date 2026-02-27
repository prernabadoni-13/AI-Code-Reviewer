import json

def build_project_review_prompt(project_data: dict) -> str:
    project_json = json.dumps(project_data, indent=2)

    return f"""
You are a strict AI code review engine.

Return ONLY valid JSON.
Do not explain.
Do not add markdown.
Do not add text before or after JSON.

If there are no issues, return:
{{"issues":[]}}


Review the following project:

{project_json}
""".strip()