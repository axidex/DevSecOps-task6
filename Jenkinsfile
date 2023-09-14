// Another port for jenkins
// /opt/homebrew/opt/openjdk@17/bin/java -Dmail.smtp.starttls.enable\=true -jar /opt/homebrew/opt/jenkins-lts/libexec/jenkins.war --httpListenAddress\=127.0.0.1 --httpPort\=7070
def git_ref = params.Git.split('/')

// def rep_name = git_ref[-1].split('.')[0]

pipeline {
    environment {
        PATH="/opt/homebrew/bin/:/usr/local/go/bin/:/usr/local/bin/:${env.PATH}"
    }

    // TODO: MacOS Jenkins can't refer to Mac docker when using agent{docker} 
    // agent {
    //     docker {
    //         image 'axidex/devsecops:latest'
    //     }
    // }
    //agent { dockerfile true }
    agent any

    stages {
        stage('SCM') {
            steps {
                echo 'SCM..'
                
                sh 'https://github.com/axidex/DevSecOps-task6' // https://github.com/0c34/govwa https://github.com/netlify/gocommerce
                sh 'mv ' + git_ref[-1] + ' src'
            }
        }

        stage('Docker') {
            steps {
                echo 'Docker..'

                sh 'docker build -t axidex/api1 .'
                sh 'docker push axidex/api1 '
            }
        }
    }
    
    post {
        // Clean after build
        always {
                cleanWs( patterns: [[pattern: '.log', type: 'EXCLUDE']] )
        }
    }
}