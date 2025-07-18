pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = 'themryesac'
        IMAGE_NAME = 'itec4299finalproject'
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
                     withCredentials([sshUserPrivateKey(credentialsId: 'laptop-ec2-key', keyFileVariable: 'EC2_PRIVATE_KEY_PATH')]) {
                        sh """
                            mkdir -p ~/.ssh
                            ssh-keyscan -H ${APP_EC2_HOST} >> ~/.ssh/known_hosts 2>/dev/null
                            chmod 600 ~/.ssh/known_hosts
                            
                            # Ensure the remote directory exists
                            ssh -i ${EC2_PRIVATE_KEY_PATH} ${APP_EC2_USER}@${APP_EC2_HOST} "mkdir -p /home/${APP_EC2_USER}/ITEC4299FINALPROJECT/"

                            # Transfer docker-compose-deploy.yml to the EC2 instance
                            scp -i ${EC2_PRIVATE_KEY_PATH} docker-compose-deploy.yml ${APP_EC2_USER}@${APP_EC2_HOST}:/home/${APP_EC2_USER}/ITEC4299FINALPROJECT/

                            # Execute remote commands for deployment
                            ssh -i ${EC2_PRIVATE_KEY_PATH} ${APP_EC2_USER}@${APP_EC2_HOST} << EOF
                                cd /home/${APP_EC2_USER}/ITEC4299FINALPROJECT/
                                docker-compose -f docker-compose-deploy.yml pull
                                docker-compose -f docker-compose-deploy.yml down -v --remove-orphans
                                docker-compose -f docker-compose-deploy.yml up -d
                                docker image prune -f
                            EOF
                        """
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

