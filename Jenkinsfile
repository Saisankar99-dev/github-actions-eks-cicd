pipeline {
  agent any

  environment {
    AWS_REGION     = 'us-east-1'
    CLUSTER_NAME   = 'my-eks-cluster'
    DOCKER_REGISTRY = 'docker.io'
    DOCKER_REPO     = 'saisankar99/ultimate-flask-app'
    IMAGE_TAG       = ''
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build & Push Docker Image') {
      steps {
        script {
          // Define IMAGE_TAG explicitly using Windows-compatible syntax
          def IMAGE_TAG = bat(script: "git rev-parse --short HEAD", returnStdout: true).trim()

          // login & push to Docker registry (use bat for Windows)
          withCredentials([usernamePassword(
            credentialsId: 'docker-cred',
            usernameVariable: 'DOCKER_USER',
            passwordVariable: 'DOCKER_PASS'
          )]) {
            bat """
              docker login ${DOCKER_REGISTRY} -u %DOCKER_USER% -p %DOCKER_PASS%
              docker build -t ${DOCKER_REGISTRY}/${DOCKER_REPO}:${IMAGE_TAG} .
              docker push ${DOCKER_REGISTRY}/${DOCKER_REPO}:${IMAGE_TAG}
            """
          }
        }
      }
    }

    // stage('Assume IAM Role & Update kubeconfig') {
    //   steps {
    //     withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-creds']]) {
    //       script {
    //         def resp = sh(script: """
    //           aws sts assume-role \
    //             --role-arn arn:aws:iam::123456789012:role/eks-deployment-role \
    //             --role-session-name jenkins-${BUILD_NUMBER} \
    //             --region ${AWS_REGION} \
    //             --output json
    //         """, returnStdout: true).trim()

    //         def creds = readJSON text: resp
    //         env.AWS_ACCESS_KEY_ID     = creds.Credentials.AccessKeyId
    //         env.AWS_SECRET_ACCESS_KEY = creds.Credentials.SecretAccessKey
    //         env.AWS_SESSION_TOKEN     = creds.Credentials.SessionToken

    //         sh "aws eks update-kubeconfig --name ${CLUSTER_NAME} --region ${AWS_REGION}"
    //       }
    //     }
    //   }
    // }

    // stage('Deploy with Helm') {
    //   steps {
    //     dir("chart") {
    //       sh """
    //         helm upgrade --install myapp-python . \
    //           --namespace default \
    //           --set image.repository=${DOCKER_REGISTRY}/${DOCKER_REPO} \
    //           --set image.tag=${IMAGE_TAG} \
    //           --wait
    //       """
    //     }
    //   }
    // }
  }

//   post {
//     success { echo "✅ Deployed ${DOCKER_REGISTRY}/${DOCKER_REPO}:${IMAGE_TAG}" }
//     failure { echo "❌ Deployment failed" }
//     always  { cleanWs() }
//   }
}
