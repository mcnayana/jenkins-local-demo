import os
import glob
import json
import urllib.request

# ==========================================
# Configuration
# ==========================================

OLLAMA_URL = "http://host.docker.internal:11434/api/generate"
MODEL = "qwen2.5:1.5b"

BUILD_DIR = "/var/jenkins_home/jobs/flask-ci-cd/builds"

# ==========================================
# Read Latest Jenkins Build Log
# ==========================================

try:

    build_dirs = []

    for folder in glob.glob(os.path.join(BUILD_DIR, "*")):
        if os.path.basename(folder).isdigit():
            build_dirs.append(folder)

    if not build_dirs:
        print("No Jenkins builds found.")
        exit(1)

    latest_build = max(
        build_dirs,
        key=lambda x: int(os.path.basename(x))
    )

    log_file = os.path.join(latest_build, "log")

    with open(log_file, "r", errors="ignore") as f:
        full_log = f.read()

except Exception as e:

    print("Unable to read Jenkins log")
    print(e)
    exit(1)

# ==========================================
# Extract Important Error Lines
# ==========================================

keywords = [
    "ERROR",
    "Error",
    "error",
    "FAILURE",
    "FAILED",
    "Failure",
    "Exception",
    "Traceback",
    "ModuleNotFoundError",
    "No such file",
    "cannot",
    "returned exit code",
    "docker:",
    "failed",
    "Failed",
    "script returned"
]

important_lines = []

for line in full_log.splitlines():

    for keyword in keywords:

        if keyword in line:
            important_lines.append(line)
            break

if important_lines:
    log = "\n".join(important_lines)
else:
    # fallback: use last 100 lines
    log = "\n".join(full_log.splitlines()[-100:])

# ==========================================
# Build Prompt
# ==========================================

prompt = f"""
You are a Senior DevOps Engineer.

Analyze the Jenkins failure log.

Return ONLY in the following format.

Root Cause:
<one concise sentence>

Responsible Team:
<one team only>

Suggested Fix:
<clear fix>

Severity:
<Low/Medium/High>

Do not provide introductions, explanations, or extra text.

Jenkins Error Log:

{log}
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

# ==========================================
# Call Ollama
# ==========================================

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