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
    "No module named",
    "Permission denied",
    "permission denied",
    "returned exit code",
    "docker:",
    "failed",
    "Failed",
    "cannot",
    "script returned",
    "Connection refused",
    "port is already allocated",
    "Address already in use",
    "unable to",
    "not found"
]

important_lines = []

for line in full_log.splitlines():

    for keyword in keywords:

        if keyword.lower() in line.lower():
            important_lines.append(line)
            break

if important_lines:
    log = "\n".join(important_lines)
else:
    log = "\n".join(full_log.splitlines()[-100:])

# ==========================================
# AI Prompt
# ==========================================

prompt = f"""
You are an AI Support Engineer working for a production support team.

Your task is to analyze the Jenkins build failure log.

You MUST classify the issue into ONLY ONE of the following support teams.

1. DevOps Team
2. Middleware Team
3. Unix Team

Classification Rules

DevOps Team:
- Jenkins pipeline failures
- Jenkinsfile errors
- Git/GitHub issues
- Docker build failures
- Docker image issues
- Docker compose issues
- CI/CD failures
- Python dependency issues
- Build failures
- Deployment failures
- Kubernetes issues
- Helm issues

Middleware Team:
- Tomcat
- WebLogic
- WebSphere
- JBoss
- Java application errors
- Spring Boot startup issues
- REST API failures
- HTTP 404
- HTTP 500
- Application deployment issues
- Database connectivity
- Application configuration issues

Unix Team:
- Linux permission denied
- Disk full
- Memory issues
- CPU utilization
- Port already in use
- File system issues
- Service not running
- Process failures
- Shell script failures
- OS command failures

Instructions

1. Read the Jenkins log carefully.
2. Identify the actual root cause.
3. Choose ONLY ONE responsible team.
4. Do not guess multiple teams.
5. Return ONLY the format below.
6. Do not add explanations.

Output Format

Pipeline Status:
FAILED

Root Cause:
<one concise sentence>

Responsible Team:
<DevOps Team OR Middleware Team OR Unix Team>

Suggested Fix:
<step-by-step solution>

Severity:
<Low/Medium/High>

Confidence:
<0-100%>

Jenkins Error Log

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
    print("============================================================")
    print("              AI FAILURE ANALYSIS REPORT")
    print("============================================================")
    print()

    print(result.get("response", "No response received."))

    print()
    print("============================================================")

except Exception as e:

    print()
    print("Unable to connect to Ollama")
    print(e)