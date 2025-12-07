pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/ScriptSorcerer23/DevOps_WebApp_seleniumtests.git'
            }
        }
        stage('Build and Test') {
            steps {
                script {
                    docker.build('selenium-tests').inside {
                        sh 'pytest test_selenium.py -v'
                    }
                }
            }
        }
    }
    post {
        always {
            emailext body: 'Test results attached', subject: 'Jenkins Test Results', to: 'collaborator@example.com', attachLog: true
        }
    }
}