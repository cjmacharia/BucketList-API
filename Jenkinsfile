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
                sh 'chmod +x create_db.sh'
                sh './create_db.sh'
                sh 'pip3 install -r requirements.txt'
                 sh ''' 
                     /etc/init.d/postgresql start'
                     su postgres
                     psql -U postgres -c create database test_db
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
