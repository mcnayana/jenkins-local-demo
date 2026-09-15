pipeline {

    agent any

    environment {
        IMAGE_NAME="flask-app"
        CONTAINER_NAME="flask-container"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                url: 'https://github.com/mcnayana/jenkins-local-demo.git'
            }
        }

        stage('Build Docker Image') {
            steps {

                sh '''
                docker build -f Dockerfile123 -t ${IMAGE_NAME} .
                
                '''
            }
        }

        stage('Deploy') {
            steps {

                sh '''
                docker rm -f ${CONTAINER_NAME} || true

                docker run -d \
                -p 5000:5000 \
                --name ${CONTAINER_NAME} \
                ${IMAGE_NAME}
                '''
            }
        }

    }

    post {

        failure {

            echo "===================================="
            echo "AI FAILURE ANALYSIS"
            echo "===================================="

            sh '''
            python3 ai_analyzer.py || true
            '''
        }

        success {

            echo "Application deployed successfully."

        }

        always {

            echo "Pipeline execution completed."

        }

    }

}
