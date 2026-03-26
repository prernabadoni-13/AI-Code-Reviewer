import os
import webbrowser
from typing import List

def generate_html_report(issues: list, complexity: list, project_path: str) -> str:
    
    # count severities
    errors = len([i for i in issues if i.get("severity") == "error"])
    warnings = len([i for i in issues if i.get("severity") == "warning"])
    infos = len([i for i in issues if i.get("severity") == "info"])

    # build issues rows
    issue_rows = ""
    for issue in issues:
        severity = issue.get("severity", "info")
        color = {"error": "#ff4444", "warning": "#ffaa00", "info": "#4488ff"}.get(severity, "#888")
        badge_bg = {"error": "#ffe0e0", "warning": "#fff3cd", "info": "#e0eaff"}.get(severity, "#eee")
        source = issue.get("source", "llm")
        source_tag = "🤖 LLM" if source == "llm" else "📏 Rule"
        issue_rows += f"""
        <tr>
            <td><code>{issue.get('file', '')}</code></td>
            <td style="text-align:center">{issue.get('line', '')}</td>
            <td style="text-align:center">
                <span style="background:{badge_bg}; color:{color}; padding:3px 8px; border-radius:12px; font-weight:bold; font-size:12px">
                    {severity.upper()}
                </span>
            </td>
            <td>{issue.get('message', '')}</td>
            <td style="text-align:center; font-size:12px">{source_tag}</td>
        </tr>"""

    # build complexity rows
    complexity_rows = ""
    for c in complexity:
        score = c.get("score", 0)
        if score <= 3:
            color = "#28a745"
            label = "Simple"
            bg = "#d4edda"
        elif score <= 6:
            color = "#ff8800"
            label = "Moderate"
            bg = "#fff3cd"
        else:
            color = "#ff4444"
            label = "Complex"
            bg = "#ffe0e0"

        complexity_rows += f"""
        <tr>
            <td><code>{c.get('file', '')}</code></td>
            <td><code>{c.get('function', '')}</code></td>
            <td style="text-align:center">{c.get('line', '')}</td>
            <td style="text-align:center">
                <span style="background:{bg}; color:{color}; padding:3px 8px; border-radius:12px; font-weight:bold">
                    {score}/10 — {label}
                </span>
            </td>
            <td>{c.get('message', '')}</td>
        </tr>"""

    if not complexity_rows:
        complexity_rows = """
        <tr>
            <td colspan="5" style="text-align:center; color:#888; padding:20px">
                ✅ No complexity issues found
            </td>
        </tr>"""

    if not issue_rows:
        issue_rows = """
        <tr>
            <td colspan="5" style="text-align:center; color:#888; padding:20px">
                ✅ No issues found! Great code.
            </td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Code Review Report</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f0f2f5; color: #333; }}
        
        .header {{ background: linear-gradient(135deg, #1a1a2e, #16213e); color: white; padding: 40px; }}
        .header h1 {{ font-size: 28px; margin-bottom: 8px; }}
        .header p {{ color: #aaa; font-size: 14px; }}
        
        .stats {{ display: flex; gap: 20px; padding: 30px 40px; flex-wrap: wrap; }}
        .stat-card {{ background: white; border-radius: 12px; padding: 20px 30px; flex: 1; min-width: 150px;
                     box-shadow: 0 2px 8px rgba(0,0,0,0.08); text-align: center; }}
        .stat-card .number {{ font-size: 36px; font-weight: bold; }}
        .stat-card .label {{ font-size: 13px; color: #888; margin-top: 4px; }}
        .stat-card.errors .number {{ color: #ff4444; }}
        .stat-card.warnings .number {{ color: #ffaa00; }}
        .stat-card.infos .number {{ color: #4488ff; }}
        .stat-card.total .number {{ color: #333; }}

        .section {{ margin: 0 40px 30px; }}
        .section h2 {{ font-size: 18px; margin-bottom: 15px; color: #1a1a2e; }}
        
        table {{ width: 100%; border-collapse: collapse; background: white;
                border-radius: 12px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }}
        th {{ background: #1a1a2e; color: white; padding: 14px 16px; text-align: left; font-size: 13px; }}
        td {{ padding: 12px 16px; border-bottom: 1px solid #f0f0f0; font-size: 14px; }}
        tr:last-child td {{ border-bottom: none; }}
        tr:hover td {{ background: #f9f9f9; }}

        .footer {{ text-align: center; padding: 30px; color: #aaa; font-size: 13px; }}
        code {{ background: #f0f0f0; padding: 2px 6px; border-radius: 4px; font-size: 13px; }}
    </style>
</head>
<body>

    <div class="header">
        <h1>🤖 AI Code Review Report</h1>
        <p>Project: {project_path}</p>
    </div>

    <div class="stats">
        <div class="stat-card total">
            <div class="number">{len(issues)}</div>
            <div class="label">Total Issues</div>
        </div>
        <div class="stat-card errors">
            <div class="number">{errors}</div>
            <div class="label">🔴 Errors</div>
        </div>
        <div class="stat-card warnings">
            <div class="number">{warnings}</div>
            <div class="label">🟡 Warnings</div>
        </div>
        <div class="stat-card infos">
            <div class="number">{infos}</div>
            <div class="label">🔵 Info</div>
        </div>
    </div>

    <div class="section">
        <h2>📋 Issues Found</h2>
        <table>
            <tr>
                <th>File</th>
                <th>Line</th>
                <th>Severity</th>
                <th>Message</th>
                <th>Source</th>
            </tr>
            {issue_rows}
        </table>
    </div>

    <div class="section">
        <h2>📊 Complexity Analysis</h2>
        <table>
            <tr>
                <th>File</th>
                <th>Function</th>
                <th>Line</th>
                <th>Score</th>
                <th>Message</th>
            </tr>
            {complexity_rows}
        </table>
    </div>

    <div class="footer">
        Generated by AI Code Reviewer 🤖 | Powered by Ollama
    </div>

</body>
</html>"""

    # save report
    report_path = os.path.join(os.getcwd(), "review_report.html")
    with open(report_path, "w") as f:
        f.write(html)

    # open in browser automatically
    webbrowser.open(f"file://{report_path}")

    return report_path