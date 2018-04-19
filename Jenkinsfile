pipeline {
    agent {
        docker { 
            image 'python:3.6.1-alpine' 
            args '-u root:root'
        }
    }
    stages {
        stage('build') {
            steps {
                sh 'python --version'
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate'
                sh 'pip install --upgrade pip'
                sh 'pip install -r requirements.txt'
            }
        }
    }
}
