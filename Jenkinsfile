pipeline {
    agent any
    environment {
        SLACK_WEBHOOK = credentials('slack-webhook')
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/your-repo/syfe-qa-automation.git'
            }
        }
        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Run Tests') {
            steps {
                script {
                    try {
                        sh 'pytest --headless --html=report.html'
                        currentBuild.result = 'SUCCESS'
                    } catch (Exception e) {
                        currentBuild.result = 'FAILURE'
                    }
                }
            }
        }
        stage('Slack Notification') {
            steps {
                script {
                    def status = (currentBuild.result == 'SUCCESS') ? "✅ SUCCESS" : "❌ FAILED"
                    sh """
                    curl -X POST -H 'Content-type: application/json' --data '{"text": "🚀 Selenium Tests: ${status}"}' ${SLACK_WEBHOOK}
                    """
                }
            }
        }
    }
}
