import os
import glob
import json
import urllib.request

# ============================================
# Ollama Configuration
# ============================================

OLLAMA_URL = "http://host.docker.internal:11434/api/generate"
MODEL = "qwen2.5:1.5b"

# ============================================
# Jenkins Configuration
# ============================================

BUILD_DIR = "/var/jenkins_home/jobs/flask-ci-cd/builds"

# ============================================
# Find Latest Build Log
# ============================================

try:

    builds = []

    for folder in glob.glob(os.path.join(BUILD_DIR, "*")):
        name = os.path.basename(folder)

        if name.isdigit():
            builds.append(folder)

    if len(builds) == 0:
        print("No Jenkins builds found.")
        exit(1)

    latest_build = max(
        builds,
        key=lambda x: int(os.path.basename(x))
    )

    log_file = os.path.join(latest_build, "log")

    with open(log_file, "r", errors="ignore") as f:
        logs = f.read()

except Exception as e:

    print("Unable to read Jenkins log")
    print(e)
    exit(1)

# ============================================
# Prompt for AI
# ============================================

prompt = f"""
You are a Senior DevOps Engineer.

Analyze the Jenkins pipeline log below.

Return ONLY in this format.

Root Cause:
<answer>

Responsible Team:
<answer>

Suggested Fix:
<answer>

Severity:
<Low/Medium/High>

Jenkins Log:

{logs}
"""

payload = json.dumps({
    "model": MODEL,
    "prompt": prompt,
    "stream": False
}).encode("utf-8")

request = urllib.request.Request(
    OLLAMA_URL,
    data=payload,
    headers={
        "Content-Type": "application/json"
    },
    method="POST"
)

# ============================================
# Call Ollama
# ============================================

try:

    response = urllib.request.urlopen(request)

    result = json.loads(
        response.read().decode("utf-8")
    )

    print()
    print("====================================================")
    print("           🤖 AI FAILURE ANALYSIS REPORT")
    print("====================================================")
    print()

    print(result.get("response", "No response received."))

    print()
    print("====================================================")

except Exception as e:

    print()
    print("Unable to connect to Ollama")
    print(e)