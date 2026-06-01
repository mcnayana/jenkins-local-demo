pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/mcnayana/jenkins-local-demo.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip3 install -r requirements.txt'
            }
        }

        stage('Build / Run App') {
            steps {
                sh 'python3 app.py'
            }
        }
    }
}