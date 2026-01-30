import os

SUPPORTED_EXTENSIONS = [".py", ".js", ".ts", ".java", ".cpp", ".c"]


def scan_repo(path="."):
    scanned_files = []

    for root, dirs, files in os.walk(path):
        # Skip hidden folders like .git
        dirs[:] = [d for d in dirs if not d.startswith(".")]

        for file in files:
            if file.endswith(tuple(SUPPORTED_EXTENSIONS)):
                file_path = os.path.join(root, file)

                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    scanned_files.append({
                        "file_path": file_path,
                        "content": content,
                        "lines": content.count("\n") + 1
                    })

                except Exception as e:
                    print(f"⚠️ Could not read {file_path}: {e}")

    return scanned_files
