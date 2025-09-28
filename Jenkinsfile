pipeline {
    agent any

    environment {
        // Указываем путь, чтобы Jenkins видел Docker на Mac
        PATH = "/usr/local/bin:${env.PATH}"
        PYTHON_BIN = ""
    }

    stages {
        stage('Checkout') {
            steps {
                // Клонируем репозиторий
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                // Создаём виртуальное окружение
                sh 'python3 -m venv venv'
                script {
                    env.PYTHON_BIN = "${env.WORKSPACE}/venv/bin/python"
                }
                // Обновляем pip
                sh "${env.PYTHON_BIN} -m pip install --upgrade pip"
            }
        }

        stage('Install Dependencies') {
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
                // Запускаем тесты
                sh "${env.PYTHON_BIN} -m pytest --maxfail=1 --disable-warnings -q"
            }
        }

        stage('Build Docker Image') {
            steps {
                // Собираем Docker образ
                sh 'docker build -t telegram-bot:latest .'
            }
        }

        stage('Run Docker Container') {
            steps {
                // Запускаем контейнер в фоне
                sh 'docker rm -f telegram-bot || true' // удаляем старый контейнер, если есть
                sh 'docker run -d --name telegram-bot telegram-bot:latest'
            }
        }
    }

    post {
        failure {
            echo "Сборка или тесты завершились с ошибкой! Проверь лог."
        }
        success {
            echo "Бот успешно протестирован, собран и запущен в Docker!"
        }
    }
}
