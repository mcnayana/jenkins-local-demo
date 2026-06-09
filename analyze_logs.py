import requests

with open("jenkins.log", "r", encoding="utf-8") as f:
    logs = f.read()

prompt = f"""
Analyze the following Jenkins build log.

Identify:
- Root cause of failure
- Probable responsible team
- Suggested resolution

Log:
{logs}
"""

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "tinyllama",
        "prompt": prompt,
        "stream": False
    }
)

print(response.json()["response"])
