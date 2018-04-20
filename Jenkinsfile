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
        stage('test') {
            steps {
                sh 'pip install -r requirements.txt'
                 sh 'python3 manage.py db init'
                 sh 'python3 manage.py db migrate'
                 sh 'python3 manage.py db upgrade'
                 sh  'pytest'
            }
        }
    }
}
