pipeline {
    agent {
        docker { image 'python:3.6.1-alpine' }
    }
    stages {
        stage('Test') {
            steps {
                sh 'python --version'
            }
        }
    }
}
