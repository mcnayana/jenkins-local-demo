pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                url: 'https://github.com/mcnayana/jenkins-local-demo.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t flask-demo .'
            }
        }

        stage('Remove Old Container') {
            steps {
                bat 'docker rm -f flask-demo-container || exit 0'
            }
        }

        stage('Deploy Container') {
            steps {
                bat 'docker run -d -p 5000:5000 --name flask-demo-container flask-demo'
            }
        }
    }
}