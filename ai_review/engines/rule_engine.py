from typing import Dict, Any
from .base import ReviewEngine

class RuleBasedEngine(ReviewEngine):
    def review_project(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        issues = []
        for file in project_data.get("files", []):
            issues += self._check_rules(file)
        return {"issues": issues}

    def _check_rules(self, file: dict) -> list:
        issues = []
        lines = file.get("content", "").splitlines()
        path = file.get("path", "unknown")
        ext = path.split(".")[-1].lower()  # detect language from extension

        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            lower = line.lower()

            # ── Universal rules (all languages) ──────────────────────

            # Line too long
            if len(line) > 120:
                issues.append({"file": path, "line": i, "severity": "warning",
                    "message": f"Line too long ({len(line)} chars, max 120)"})

            # TODO/FIXME comments
            if "TODO" in line or "FIXME" in line:
                issues.append({"file": path, "line": i, "severity": "info",
                    "message": "Unresolved TODO/FIXME comment"})

            # Hardcoded credentials
            if any(k in lower for k in ["password=", "secret=", "api_key=", "token="]):
                if "os.getenv" not in line and "os.environ" not in line and "example" not in lower:
                    issues.append({"file": path, "line": i, "severity": "error",
                        "message": "Possible hardcoded credential detected"})

            # ── Python specific rules ─────────────────────────────────
            if ext == "py":

                # print statements
                if "print(" in line:
                    issues.append({"file": path, "line": i, "severity": "info",
                        "message": "Remove print statement before production"})

                # bare except
                if stripped in ("except:", "except Exception:"):
                    issues.append({"file": path, "line": i, "severity": "warning",
                        "message": "Bare except block — handle specific exceptions"})

                # mutable default argument
                if "def " in line and ("=[]" in line or "={}" in line or "=[]" in line):
                    issues.append({"file": path, "line": i, "severity": "warning",
                        "message": "Mutable default argument — use None instead"})

                # == None instead of is None
                if "== None" in line:
                    issues.append({"file": path, "line": i, "severity": "warning",
                        "message": "Use 'is None' instead of '== None'"})

                # missing function docstring (def with no docstring on next line)
                if stripped.startswith("def ") and not stripped.endswith(":"):
                    issues.append({"file": path, "line": i, "severity": "info",
                        "message": "Function definition may be missing colon"})

            # ── Java specific rules ───────────────────────────────────
            if ext == "java":

                # System.out.println
                if "System.out.println" in line:
                    issues.append({"file": path, "line": i, "severity": "info",
                        "message": "Remove System.out.println before production"})

                # empty catch block
                if "catch" in line and "{}" in line:
                    issues.append({"file": path, "line": i, "severity": "warning",
                        "message": "Empty catch block — handle the exception properly"})

                # raw types (List, Map, Set without generics)
                if any(t in line for t in ["List ", "Map ", "Set ", "ArrayList "]):
                    if "<" not in line and "import" not in line:
                        issues.append({"file": path, "line": i, "severity": "warning",
                            "message": "Raw type used — specify generic type e.g. List<String>"})

                # missing semicolon (basic check)
                if stripped and not stripped.startswith("//") and not stripped.endswith(("{", "}", ";")):
                    if any(stripped.startswith(k) for k in ["int ", "String ", "double ", "float ", "boolean "]):
                        issues.append({"file": path, "line": i, "severity": "error",
                            "message": "Possible missing semicolon at end of statement"})

            # ── JavaScript specific rules ─────────────────────────────
            if ext == "js":

                # console.log
                if "console.log" in line:
                    issues.append({"file": path, "line": i, "severity": "info",
                        "message": "Remove console.log before production"})

                # == instead of ===
                if " == " in line and "=== " not in line:
                    issues.append({"file": path, "line": i, "severity": "warning",
                        "message": "Use '===' instead of '==' for strict equality"})

                # var instead of let/const
                if stripped.startswith("var "):
                    issues.append({"file": path, "line": i, "severity": "warning",
                        "message": "Use 'let' or 'const' instead of 'var'"})

        return issues