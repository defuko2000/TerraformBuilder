pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                echo 'Running build automation'
                sh './gradlew build --no-daemon'
            }
        }
        stage('Build Docker Image') {
            when {
                branch 'main'
            }
            steps {
                script {
                    app = docker.build("defuko2000/terraformbuilder")
                    app.inside {
                        sh 'echo $(curl localhost:8080)'
                    }
                }
            }
        }
        stage('Push Docker Image') {
            when {
                branch 'main'
            }
            steps {
                script {
                    docker.withRegistry('https;//registry.hub.docker.com', 'dockerhub_key') {
                        app.push("${env.BUILD_NUMBER}")
                        app.push("latest")
                    }
                }
            }
        }
        stage ('Deploy To Staging') {
            when {
                branch 'main'
            }
            steps {
                input 'Deploy to Staging'
                milestone(1)
                withCredentials ([usernamePassword(credentialsId: 'staging_webserver', usernameVariable: 'USERNAME', passwordVariable: 'USERPASS')]) {
                    script {
                        sh "sshpass -p '$USERPASS' -v ssh -o StrictHostKeyChecking=no $USERNAME@${env.staging_ip} \"docker pull defuko2000/terraformbuilder:${env.BUILD_NUMBER}\""
                        try {
                           sh "sshpass -p '$USERPASS' -v ssh -o StrictHostKeyChecking=no $USERNAME@${env.staging_ip} \"docker stop terraformbuilder\""
                           sh "sshpass -p '$USERPASS' -v ssh -o StrictHostKeyChecking=no $USERNAME@${env.staging_ip} \"docker rm terraformbuilder\""
                        } catch (err) {
                            echo: 'caught error: $err'
                        }
                        sh "sshpass -p '$USERPASS' -v ssh -o StrictHostKeyChecking=no $USERNAME@${env.staging_ip} \"docker run --restart always --name terraformbuilder -p 8080:8080 -d defuko2000/terraformbuilder:${env.BUILD_NUMBER}\""
                    }
                }
            }
        }
    }
}
