pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = 'TheMrYesac'
        IMAGE_NAME = 'ITEC4299FinalProject'
        APP_EC2_USER = 'ubuntu'
        APP_EC2_HOST = 'ec2-3-134-109-237.us-east-2.compute.amazonaws.com'
        APP_EC2_KEY_ID = 'ec2'
    }

    stages {
        stage('Checkout Source') {
            steps {
                git branch: 'main', credentialsId: 'github', url: 'https://github.com/TheMrYesac/ITEC4299FinalProject'
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    // Build app image
                    bat "docker build -t ${DOCKER_REGISTRY}/${IMAGE_NAME}-app:latest -f Dockerfile ."
                    // Build proxy image
                    bat "docker build -t ${DOCKER_REGISTRY}/${IMAGE_NAME}-proxy:latest -f proxy/Dockerfile proxy/"
                }
            }
        }

        stage('Push Docker Images') {
            steps {
                script {
                    // Authenticate with Docker Hub/ECR
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                        bat "echo ${DOCKER_PASSWORD} | docker login -u ${DOCKER_USERNAME} --password-stdin"
                        bat "docker push ${DOCKER_REGISTRY}/${IMAGE_NAME}-app:latest"
                        bat "docker push ${DOCKER_REGISTRY}/${IMAGE_NAME}-proxy:latest"
                    }
                }
            }
        }

        stage('Deploy to AWS EC2') {
            steps {
                sshPublisher(publishers: [
                    sshPublisherEntry(
                        configName: 'ITEC4299FinalProject', 
                        transfers: [
                            sshTransfer(
                                sourceFiles: 'docker-compose-deploy.yml',
                                removePrefix: '',
                                remoteDirectory: '/home/${APP_EC2_USER}/ITEC4299FINALPROJECT/',
                                execCommand: '''
                                    cd /home/${APP_EC2_USER}/ITEC4299FINALPROJECT/
                                    docker-compose -f docker-compose-deploy.yml pull
                                    docker-compose -f docker-compose-deploy.yml down -v --remove-orphans
                                    docker-compose -f docker-compose-deploy.yml up -d
                                    docker image prune -f
                                '''
                            )
                        ]
                    )
                ])
            }
        }
    }

    post {
        always {
            // Clean up workspace
            cleanWs()
        }
        failure {
            // Send notification on failure
            echo 'Pipeline failed!'
        }
        success {
            // Send notification on success
            echo 'Pipeline successful!'
        }
    }
}
