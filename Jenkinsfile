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
                 
                    psql -U postgres -p 5432 -c "CREATE DATABASE test_db  OWNER postgres"
                    export APP_SETTING="test"
                    export FLASK_APP="run.py"
                    export SECRET="this is a very long string"
                    '''
                sh 'pip3 install -r requirements.txt'
            }
        }
        stage('test') {
            steps {
                sh 'export DATABASE_URL="postgresql://postgres:postgres@35.204.7.185:5432/test_db"'
                 sh  'pytest'
            }
        }
    }
}
