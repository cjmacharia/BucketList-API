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
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate'
                sh 'pip3 install --upgrade pip'
                sh 'pip3 install -r requirements.txt'
            }
        }
    }
}
