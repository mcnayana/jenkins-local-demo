pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/mcnayana/jenkins-local-demo.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t flask-app .'
            }
        }

        stage('Run Container') {
            steps {
                sh 'docker run -d -p 5000:5000 --name flask-container flask-app || true'
            }
        }
    }

     post {
        success {
            echo 'CI/CD Pipeline SUCCESS 🚀'
        }
        failure {
            echo 'CI/CD Pipeline FAILED ❌'
             sh 'python3 analyze_logs.py'
        }
    }

}
