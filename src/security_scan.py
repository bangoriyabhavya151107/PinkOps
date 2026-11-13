import os
import re
import sys
from pathlib import Path

proj_root = Path(__file__).resolve().parent.parent

patterns = [
    r"(?i)api[_-]?key\s*[:=]\s*['\"][a-zA-Z0-9_\-]{16,}['\"]",
    r"(?i)secret[_-]?key\s*[:=]\s*['\"][a-zA-Z0-9_\-]{16,}['\"]",
    r"(?i)bearer\s+[a-zA-Z0-9_\-\.]{20,}",
    r"(?i)ghp_[a-zA-Z0-9]{36}",
    r"(?i)github[_-]?pat[_-]?[a-zA-Z0-9]{22,}",
    r"(?i)password\s*[:=]\s*['\"][^\'\"]{6,}['\"]",
    r"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----"
]

ignored_dirs = {".git", ".venv", "__pycache__", ".pytest_cache"}
findings = []

for root, dirs, files in os.walk(proj_root):
    # Skip ignored dirs
    parts = Path(root).relative_to(proj_root).parts
    if any(p in ignored_dirs for p in parts):
        continue
    for f in files:
        if f.startswith(".env") or f.endswith((".key", ".pem", ".p12", ".pfx", ".secret")):
            findings.append((Path(root) / f, "Tracked credential / env file pattern"))
        if f.endswith((".py", ".json", ".md", ".csv", ".txt", ".yaml", ".yml")):
            fpath = Path(root) / f
            try:
                content = fpath.read_text(encoding="utf-8", errors="ignore")
                for pat in patterns:
                    if re.search(pat, content):
                        findings.append((fpath, f"Matched secret regex: {pat}"))
            except Exception as e:
                pass

print(f"Total findings: {len(findings)}")
if len(findings) > 0:
    for path, reason in findings:
        print(f"FAILED: {path.relative_to(proj_root)} -> {reason}")
    sys.exit(1)
else:
    print("SECURITY_SECRET_SCAN = CLEAN")
    sys.exit(0)
