pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = 'themryesac'
        IMAGE_NAME = 'itec4299finalproject'
        APP_EC2_USER = 'ubuntu'
        APP_EC2_HOST = 'ec2-3-134-109-237.us-east-2.compute.amazonaws.com'
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
                    withCredentials([usernamePassword(credentialsId: 'docker', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                        bat "echo ${DOCKER_PASSWORD} | docker login -u ${DOCKER_USERNAME} --password-stdin"
                        bat "docker push ${DOCKER_REGISTRY}/${IMAGE_NAME}-app:latest"
                        bat "docker push ${DOCKER_REGISTRY}/${IMAGE_NAME}-proxy:latest"
                    }
                }
            }
        }

        stage('Deploy to AWS EC2') {
            steps {
                script{
                    sshagent(credentials: ['laptop-ec2-key'], agentBin: 'C\\Windows\\System32\\OpenSSH\\ssh-agent.exe') {
                        def remoteDir = "/home/${APP_EC2_USER}/itec4299finalproject"
                        
                        bat "ssh ${APP_EC2_USER}@${APP_EC2_HOST} \"mkdir -p ${remoteDir}\""
                        
                        bat "scp \"${workspace}/docker-compose-deploy.yml\" ${APP_EC2_USER}@${APP_EC2_HOST}:${remoteDir}/"
                
                        bat "ssh ${APP_EC2_USER}@${APP_EC2_HOST} \"cd ${remoteDir} && docker-compose -f docker-compose-deploy.yml pull && docker-compose -f docker-compose-deploy.yml up -d --remove-orphans\""
            
                    }
            }
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

