import os
import subprocess

# Maximum file size (optional safety)
MAX_FILE_SIZE = 150_000  # in bytes

def is_git_repo(path: str) -> bool:
    """Check if the given path is inside a Git repository."""
    try:
        subprocess.check_output(
            ["git", "-C", path, "rev-parse", "--is-inside-work-tree"],
            stderr=subprocess.DEVNULL,
        )
        return True
    except subprocess.CalledProcessError:
        return False

def git_ls_files(path: str) -> list[str]:
    """Return a list of files tracked by Git in the repository."""
    result = subprocess.check_output(
        ["git", "-C", path, "ls-files"],
        text=True,
    )
    files = result.strip().split("\n")
    return [f for f in files if f]  # remove empty strings

def read_file_content(file_path: str) -> str | None:
    """Read a file and return its content or None on failure."""
    try:
        if os.path.getsize(file_path) > MAX_FILE_SIZE:
            return None
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        # Skip if binary content detected
        if "\x00" in content:
            return None
        return content
    except Exception:
        return None

def scan_repo(path: str = "."):
    """Scan the Git repository using git ls-files and return structured data."""
    repo_path = os.path.abspath(path)

    if not is_git_repo(repo_path):
        raise Exception(f"Not a Git repository: {repo_path}")

    files = git_ls_files(repo_path)

    scanned_files = []
    for file in files:
        full_path = os.path.join(repo_path, file)
        content = read_file_content(full_path)
        if content is None:
            continue

        scanned_files.append({
            "path": file,
            "lines": content.count("\n") + 1,
            "content": content,
        })

    return {
        "root": repo_path,
        "total_files": len(scanned_files),
        "files": scanned_files
    }
