pipeline {
    agent {
        docker { 
            image 'cjmash/cp:cp3' 
            args '-u root:root'
        }
    }
    stages {
        stage('build') {
            steps {
                sh 'python --version'
                sh 'pip3 install -r requirements.txt'
            }
        }
        stage('test') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'export APP_SETTING="development"'
                 sh 'python3 manage.py db init'
                 sh 'python3 manage.py db migrate'
                 sh 'python3 manage.py db upgrade'
                 sh  'pytest'
            }
        }
    }
}
