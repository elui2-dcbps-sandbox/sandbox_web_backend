pipeline {
  agent {
    kubernetes {
      yaml '''
apiVersion: v1
kind: Pod
spec:
  automountServiceAccountToken: false
  containers:
  - name: python
    image: python:3.13
    command: ['cat']
    tty: true
'''
    }
  }
  options { skipDefaultCheckout(true) }
  stages {
    stage('Checkout') {
      steps { container('jnlp') { checkout scm } }
    }
    stage('Synthetic tests') {
      steps {
        container('python') {
          sh '''
set -eu
python -m pip install --disable-pip-version-check -q uv==0.12.13
uv sync --frozen
uv run pytest -q
'''
        }
      }
    }
    stage('SonarQube Analysis') {
      steps {
        script {
          def statusSha
          container('jnlp') {
            statusSha = sh(returnStdout: true, script: 'git rev-parse HEAD').trim()
          }
          withEnv(['STATUS_SHA=' + statusSha]) {
            withCredentials([usernamePassword(credentialsId: 'sandbox-checks-app', usernameVariable: 'APP_USER', passwordVariable: 'CHECKS_TOKEN')]) {
              container('python') {
                sh '''
set +x
python - <<'PY'
import json, os, urllib.request
url = 'https://api.github.com/repos/elui2-dcbps-sandbox/sandbox_web_backend/statuses/' + os.environ['STATUS_SHA']
body = json.dumps({'state': 'success', 'context': 'stage/SonarQube Analysis', 'description': 'Synthetic sandbox stage passed'}).encode()
request = urllib.request.Request(url, data=body, method='POST', headers={'Authorization': 'Bearer ' + os.environ['CHECKS_TOKEN'], 'Accept': 'application/vnd.github+json', 'Content-Type': 'application/json'})
with urllib.request.urlopen(request, timeout=30) as response:
    if response.status != 201:
        raise SystemExit('status post failed')
print('synthetic stage status posted')
PY
'''
              }
            }
          }
        }
      }
    }
  }
}
