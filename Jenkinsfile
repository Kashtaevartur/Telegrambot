pipeline {
    agent any

    environment {
        PYTHON_BIN = "" // будет определяться после создания venv
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh 'python3 -m venv venv'
                script {
                    env.PYTHON_BIN = "${env.WORKSPACE}/venv/bin/python"
                }
                sh "${env.PYTHON_BIN} -m pip install --upgrade pip"
            }
        }

        stage('Install dependencies') {
            steps {
                sh """
                    if [ -f requirements.txt ]; then
                        ${env.PYTHON_BIN} -m pip install -r requirements.txt
                    fi
                """
            }
        }

        stage('Run Tests') {
            steps {
                sh "${env.PYTHON_BIN} -m pytest"
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t telegram-bot:latest .'
            }
        }

        stage('Run Docker Container') {
            steps {
                sh 'docker run -d --name mybot telegram-bot:latest'
            }
        }
    }

    post {
        success {
            echo "Бот успешно собран и запущен!"
        }
        failure {
            echo "Произошла ошибка! Проверь лог."
        }
    }
}
