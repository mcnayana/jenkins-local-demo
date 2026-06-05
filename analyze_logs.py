import requests

with open("jenkins.log", "r", encoding="utf-8") as f:
    logs = f.read()

prompt = f"""
Analyze this Jenkins build failure.

Provide:
1. Root Cause
2. Severity
3. Responsible Team
4. Recommended Fix

Log:
{logs}
"""

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False
    }
)

print(response.json()["response"])
