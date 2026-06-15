import urllib.request
import urllib.parse
import json
import base64
import sys

# ==========================
# Jenkins Configuration
# ==========================

JENKINS_URL = "http://localhost:8080"
JOB_NAME = "flask-ci-cd"

USERNAME = "nayanamc"
API_TOKEN = "7188e56cee5081c38f1bd74046df20f8"

# ==========================
# Ollama Configuration
# ==========================

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:1.5b"

# ==========================
# Fetch Jenkins Console Log
# ==========================

console_url = f"{JENKINS_URL}/job/{JOB_NAME}/lastBuild/consoleText"

credentials = f"{USERNAME}:{API_TOKEN}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()

req = urllib.request.Request(console_url)
req.add_header("Authorization", f"Basic {encoded_credentials}")

try:
    with urllib.request.urlopen(req, timeout=60) as response:
        logs = response.read().decode("utf-8")
except Exception as e:
    print("ERROR: Unable to fetch Jenkins logs")
    print(e)
    sys.exit(1)

# ==========================
# Prompt
# ==========================

prompt = f"""
You are an experienced DevOps engineer.

Analyze the following Jenkins build log.

Do not invent technologies that are not present.

Return ONLY in this format:

Root Cause:
Responsible Team:
Suggested Fix:
Severity:

Build Log:

{logs}
"""

payload = {
    "model": MODEL_NAME,
    "prompt": prompt,
    "stream": False
}

data = json.dumps(payload).encode("utf-8")

request = urllib.request.Request(
    OLLAMA_URL,
    data=data,
    headers={"Content-Type": "application/json"},
    method="POST"
)

try:
    with urllib.request.urlopen(request, timeout=300) as response:
        result = json.loads(response.read().decode("utf-8"))
except Exception as e:
    print("ERROR: Unable to connect to Ollama")
    print(e)
    sys.exit(1)

print("\n")
print("=" * 60)
print("AI FAILURE ANALYSIS REPORT")
print("=" * 60)
print(result.get("response", "No response"))
print("=" * 60)
