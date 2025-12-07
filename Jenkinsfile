pipeline {
    agent any
    stages {
        stage('Build and Test') {
            steps {
                script {
                    def customImage = docker.build('selenium-tests')
                    customImage.inside {
                        sh 'pytest test_selenium.py -v'
                    }
                }
            }
        }
    }
    post {
        always {
            emailext body: 'Test results attached', subject: 'Jenkins Test Results', to: '6sumamatahir@gmail.com', attachLog: true
        }
    }
}