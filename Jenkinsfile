//
// Jenkinsfile for Unread Tasks Cleaner
// Executes Redis cleanup script on tomcat1-prod.ezinfra.net
//
def SCRIPT_STATUS = "Not Started"
def SCRIPT_OUTPUT = ""

pipeline {
    agent none
    environment {
        PYTHON_VERSION = "3"
    }
    parameters {
        string(name: 'commit_hash', defaultValue: 'main', description: 'Git commit hash or branch to checkout')
    }
    stages {
        stage ("Run Tasks Cleaner") {
            agent {
                label 'tomcat1-prod.ezinfra.net'
            }
            steps {
                git credentialsId: 'jenkins-github-classic-token1',
                    url: 'https://github.com/ezderm-llc/tasks-cleaner.git',
                    branch: params.commit_hash

                script {
                    // Run the cleanup script
                    def output = sh(
                        script: "python${PYTHON_VERSION} unread-tasks-cleaner.py",
                        returnStdout: true
                    ).trim()

                    SCRIPT_OUTPUT = output
                    echo "Script completed successfully"
                    echo output
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
                label 'tomcat1-prod.ezinfra.net'
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