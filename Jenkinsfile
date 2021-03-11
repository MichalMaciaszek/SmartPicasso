pipeline {
    agent { docker { image 'python:3.7.2' } }

    stages {
        stage('Build and test') {
            steps {
                sh 'pwd'
                sh 'ls'
                dir("${env.WORKSPACE}/rest-app"){
                    sh 'pwd'
                    sh 'ls'
                    sh 'python3 -m venv venv && . venv/bin/activate && pip3 install -r requirements.txt && python3 manage.py migrate && python3 manage.py test'
                }
            }
        }
    }
}
