import subprocess
import json
import urllib.request

OLLAMA_URL = "http://host.docker.internal:11434/api/generate"
MODEL = "qwen2.5:1.5b"

try:

    log = subprocess.check_output(
        [
            "bash",
            "-c",
            "tail -200 $JENKINS_HOME/jobs/flask-ci-cd/builds/lastBuild/log"
        ],
        stderr=subprocess.STDOUT,
        text=True
    )

except Exception as e:

    print("Unable to read Jenkins log")
    print(e)
    exit()

prompt = f"""
You are a Senior DevOps Engineer.

Analyze the Jenkins failure log.

Return ONLY in this format.

Root Cause:
<root cause>

Responsible Team:
<team>

Suggested Fix:
<solution>

Severity:
<Low/Medium/High>

Jenkins Log:

{log}
"""

payload = json.dumps({
    "model": MODEL,
    "prompt": prompt,
    "stream": False
}).encode()

request = urllib.request.Request(
    OLLAMA_URL,
    data=payload,
    headers={
        "Content-Type":"application/json"
    },
    method="POST"
)

try:

    response = urllib.request.urlopen(request)

    result = json.loads(
        response.read().decode()
    )

    print()

    print("==========================================")
    print("🤖 AI FAILURE ANALYSIS")
    print("==========================================")
    print()

    print(result["response"])

    print()
    print("==========================================")

except Exception as e:

    print()

    print("Unable to connect to Ollama")

    print(e)