pipeline {
    agent {
        docker { 
            image 'python:3.6.1-alpine' 
            args '-u root:root'
        }
    }
    stages {
        stage('Test') {
            steps {
                sh 'python --version'
            }
        }
    }
}
