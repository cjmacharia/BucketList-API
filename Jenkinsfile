pipeline {
    agent {
        docker { 
            image 'cjmash/jenkins:1.0.0' 
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
