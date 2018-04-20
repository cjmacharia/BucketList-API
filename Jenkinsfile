pipeline {
    agent {
        docker { 
            image 'cjmash/jenkins:jenkins' 
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
