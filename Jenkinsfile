pipeline {
    agent any

    environment {
        PYTHON_BIN = "" // Будет определяться после создания venv
    }

    stages {
        stage('Checkout') {
            steps {
                // Клонируем репозиторий в рабочую директорию Jenkins
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                // Создаём виртуальное окружение внутри workspace
                sh 'python3 -m venv venv'
                // Определяем путь к Python виртуального окружения
                script {
                    env.PYTHON_BIN = "${env.WORKSPACE}/venv/bin/python"
                }
                // Обновляем pip
                sh "${env.PYTHON_BIN} -m pip install --upgrade pip"
            }
        }

        stage('Install dependencies') {
            steps {
                // Устанавливаем зависимости из requirements.txt, если файл есть
                sh """
                    if [ -f requirements.txt ]; then
                        ${env.PYTHON_BIN} -m pip install -r requirements.txt
                    fi
                """
            }
        }

        stage('Run Telegram Bot') {
            steps {
                // Запускаем бота в виртуальном окружении
                sh "${env.PYTHON_BIN} main.py"
            }
        }
    }

    post {
        failure {
            echo "Произошла ошибка! Проверь лог."
        }
        success {
            echo "Бот успешно запущен!"
        }
    }
}
