def format_issues(issues: list[dict]) -> str:
    if not issues:
        return "No issues found!"

    output = []
    for issue in issues:
        output.append(
            f"{issue.get('file')}:{issue.get('line')} "
            f"[{issue.get('severity')}] "
            f"{issue.get('message')}"
        )

    return "\n".join(output)