pipeline {

    agent any

    environment {
        IMAGE_NAME = "flask-app"
        CONTAINER_NAME = "flask-container"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/mcnayana/jenkins-local-demo.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t ${IMAGE_NAME} .
                '''
            }
        }

        stage('Remove Old Container') {
            steps {
                sh '''
                docker rm -f ${CONTAINER_NAME} || true
                '''
            }
        }

        stage('Deploy Container') {
            steps {
                sh '''
                docker run -d \
                -p 5000:5000 \
                --name ${CONTAINER_NAME} \
                ${IMAGE_NAME}
                '''
            }
        }
    }

    post {

        success {
            echo "======================================"
            echo "Application deployed successfully."
            echo "======================================"
        }

        failure {

            echo "======================================"
            echo "Pipeline Failed"
            echo "Running AI Analyzer..."
            echo "======================================"

            sh '''
            python3 ai_analyzer.py || true
            '''
        }

        always {
            echo "Pipeline execution completed."
        }
    }
}