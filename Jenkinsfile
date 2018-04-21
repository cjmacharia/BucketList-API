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
                sh 'service postgresql start'
                sh 'sudo -u postgres psql -c 'create database test_db'
                 sh ''' 
                    export APP_SETTING="development"
                    export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/test_db"
                    '''
            }
        }
        stage('test') {
            steps {
                 sh 'python3 manage.py db init'
                 sh 'python3 manage.py db migrate'
                 sh 'python3 manage.py db upgrade'
                 sh  'pytest'
            }
        }
    }
}
