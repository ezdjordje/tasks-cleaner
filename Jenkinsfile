//
// Jenkinsfile for Unread Tasks Cleaner
// Executes Redis cleanup script on tomcat1-prod.ezinfra.net via SSH
//
def SCRIPT_STATUS = "Not Started"
def SCRIPT_OUTPUT = ""

pipeline {
    agent none
    environment {
        ANSIBLE_VER = "11.8.0"
        PYTHON_VERSION = "3"
        REMOTE_SERVER = "tomcat1-prod.ezinfra.net"
        REMOTE_USER = "ubuntu"
        REMOTE_DIR = "/tmp/tasks-cleaner"
    }
    parameters {
        string(name: 'commit_hash', defaultValue: 'main', description: 'Git commit hash or branch to checkout')
    }
    stages {
        stage ("Run Tasks Cleaner") {
            agent {
                docker {
                    image "nexus.ezinfra.net:5001/ezderm/ansible:${ANSIBLE_VER}"
                    registryUrl "https://nexus.ezinfra.net:5001/"
                    registryCredentialsId "user_for_nexus_docker_repo"
                    args "--entrypoint='' -u root"
                }
            }
            steps {
                git credentialsId: 'jenkins-github-classic-token1',
                    url: 'https://github.com/ezderm-llc/tasks-cleaner.git',
                    branch: params.commit_hash

                script {
                    sshagent(['jenkins-deploy-key']) {
                        // Create remote directory
                        sh "ssh -o StrictHostKeyChecking=no ${REMOTE_USER}@${REMOTE_SERVER} 'mkdir -p ${REMOTE_DIR}'"

                        // Copy script to remote server
                        sh "scp -o StrictHostKeyChecking=no unread-tasks-cleaner.py ${REMOTE_USER}@${REMOTE_SERVER}:${REMOTE_DIR}/"

                        // Execute the script on remote server
                        def output = sh(
                            script: "ssh -o StrictHostKeyChecking=no ${REMOTE_USER}@${REMOTE_SERVER} 'cd ${REMOTE_DIR} && python${PYTHON_VERSION} unread-tasks-cleaner.py'",
                            returnStdout: true
                        ).trim()

                        // Cleanup remote directory
                        sh "ssh -o StrictHostKeyChecking=no ${REMOTE_USER}@${REMOTE_SERVER} 'rm -rf ${REMOTE_DIR}'"

                        SCRIPT_OUTPUT = output
                        echo "Script completed successfully"
                        echo output
                    }
                }
            }
            post {
                success {
                    script {
                        SCRIPT_STATUS = "Success"
                        echo "✓ Tasks Cleaner completed successfully"
                        echo "Output: ${SCRIPT_OUTPUT}"
                    }
                }
                failure {
                    script {
                        SCRIPT_STATUS = "Failed"
                        echo "✗ Tasks Cleaner failed"
                    }
                }
            }
        }
        stage ("Cleanup") {
            agent {
                docker {
                    image "nexus.ezinfra.net:5001/ezderm/ansible:${ANSIBLE_VER}"
                    registryUrl "https://nexus.ezinfra.net:5001/"
                    registryCredentialsId "user_for_nexus_docker_repo"
                    args "--entrypoint='' -u root"
                }
            }
            steps {
                cleanWs(deleteDirs: true)
            }
        }
    }
    post {
        success {
            script {
                echo "=========================================="
                echo "✓ Job Successful"
                echo "Job duration: ${currentBuild.durationString}"
                echo "Commit: ${params.commit_hash}"
                echo "Script Status: ${SCRIPT_STATUS}"
                echo "=========================================="
            }
        }
        failure {
            script {
                echo "=========================================="
                echo "✗ Job Failed"
                echo "Job duration: ${currentBuild.durationString}"
                echo "Commit: ${params.commit_hash}"
                echo "Script Status: ${SCRIPT_STATUS}"
                echo "=========================================="
            }
        }
    }
}