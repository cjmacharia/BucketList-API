pipeline {
    agent {
        docker { 
            image 'cjmash/cp:cp6' 
            args '-u root:root'
        }
    }
    stages {
        stage('build') {
            steps {
                sh 'python --version'
                sh 'chmod +x create_db.sh'
                sh './create_db.sh'
                 sh ''' 
                    chmod 0600 ~/.pgpass
                    psql -U postgres -p 5432 -c "CREATE DATABASE flask_db  OWNER postgres"
                    export APP_SETTING="development"
                    export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/test_db"
                    '''
                sh 'pip3 install -r requirements.txt'
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
