pipeline {
  agent { label 'slave1' }
  environment {GIT_HASH = gitHash() }
  options {
    timeout(time: 20, unit: 'MINUTES')
  }
  stages {
    stage("build images") {
      when { branch 'master' }
      steps {
        withCredentials([string(credentialsId: 'ssh_private_key', variable: 'SSH_PRIVATE_KEY')]) {
          makeDocker()
        }
      }
    }
    stage('test') {
      steps {
        script {
          docker.withRegistry('https://registry.hub.docker.com', 'dockerhub') {
            image = docker.image('investabit/images:reporting-master')
            image.pull()
          }
          image.inside ('--entrypoint="" -u root:root') {
            sh 'cd /usr/src/reporting && python -m pytest --junitxml=$WORKSPACE/build/results.xml || true'
            sh 'chown -R 10000:10000 $WORKSPACE/build'
            junit allowEmptyResults: true, testResults: 'build/results.xml'
          }
        }
      }
    }
    stage('flake8') {
      steps {
        script {
          docker.withRegistry('https://registry.hub.docker.com', 'dockerhub') {
            image = docker.image('investabit/images:reporting-master')
            image.pull()
          }
          image.inside ('--entrypoint="" -u root:root') {
            sh 'cd /usr/src/reporting && flake8 --exit-zero --ignore E501,W503,E203 --max-line-length 100 --select C,E,F,W,B,B950 --output-file=$WORKSPACE/flake8.log backtest'
            sh 'chown -R 10000:10000 $WORKSPACE/flake8.log'
            recordIssues enabledForFailure: true, tools: [flake8(pattern: 'flake8.log')]
          }
        }
      }
    }
    stage('mypy') {
      steps {
        script {
          docker.withRegistry('https://registry.hub.docker.com', 'dockerhub') {
            image = docker.image('investabit/images:reporting-master')
            image.pull()
          }
          image.inside ('--entrypoint="" -u root:root') {
            sh 'cd /usr/src/reporting && mypy --ignore-missing-imports --follow-imports normal --warn-unused-configs --disallow-subclassing-any --disallow-untyped-calls --disallow-untyped-defs --disallow-incomplete-defs --check-untyped-defs --no-implicit-optional --warn-redundant-casts --warn-unused-ignores --warn-return-any backtest > $WORKSPACE/mypy.log || true'
            sh 'chown -R 10000:10000 $WORKSPACE/mypy.log'
            recordIssues enabledForFailure: true, tools: [myPy(pattern: 'mypy.log')]
          }
        }
      }
    }

  }

  post {
    always {
      deleteDir()
      sendNotifications currentBuild.result
    }
  }
}
