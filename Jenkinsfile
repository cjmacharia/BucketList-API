pipeline {
    agent {
        docker { 
            image 'python:3.6' 
            args '-u root:root'
        }
    }
    stages {
        stage('build') {
            steps {
                sh 'python --version'
                sh 'pip install -r requirements.txt'
            }
        }
    }
}
