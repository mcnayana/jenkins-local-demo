import requests
import sys

# =====================================================
# Jenkins Configuration
# =====================================================

JENKINS_URL = "http://localhost:8080"
JOB_NAME = "flask-ci-cd"

USERNAME = "nayanamc"
API_TOKEN = "7188e56cee5081c38f1bd74046df20f8"

# =====================================================
# Ollama Configuration
# =====================================================

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "tinyllama"

# =====================================================
# Fetch Latest Jenkins Console Log
# =====================================================

console_url = f"{JENKINS_URL}/job/{JOB_NAME}/lastBuild/consoleText"

try:
    response = requests.get(
        console_url,
        auth=(USERNAME, API_TOKEN),
        timeout=60
    )
except Exception as e:
    print("\nERROR: Unable to connect to Jenkins")
    print(e)
    sys.exit(1)

if response.status_code != 200:
    print("\nERROR: Failed to fetch Jenkins console log")
    print("Status Code:", response.status_code)
    print(response.text)
    sys.exit(1)

logs = response.text

print("\n========================================")
print("Fetched Latest Jenkins Console Log")
print("========================================\n")

# =====================================================
# Prompt for Ollama
# =====================================================

prompt = f"""
You are an experienced DevOps support engineer.

Analyze the Jenkins build log below.

Return ONLY in this format:

Root Cause:
<answer>

Responsible Team:
<answer>

Suggested Fix:
<answer>

Severity:
<Low/Medium/High>

Build Log:

{logs}
"""

payload = {
    "model": MODEL_NAME,
    "prompt": prompt,
    "stream": False
}

try:
    ai_response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=300
    )
except Exception as e:
    print("\nERROR: Unable to connect to Ollama")
    print(e)
    sys.exit(1)

if ai_response.status_code != 200:
    print("\nERROR: Ollama API failed")
    print(ai_response.text)
    sys.exit(1)

result = ai_response.json().get("response", "No response received.")

# =====================================================
# Print AI Report
# =====================================================

print("\n")
print("=" * 60)
print("           AI FAILURE ANALYSIS REPORT")
print("=" * 60)
print(result)
print("=" * 60)