try {
node ('master'){

  env.KUBECONFIG="${env.WORKSPACE}/kubeconfig/prod/config-prod"
  env.TAG="${params.BRANCH}-${env.BUILD_NUMBER}"
  env.DOCKER_REPO="192.168.30.154:18078"
  env.APP="app"
  env.HELM_CHART="production"
  env.HELM_CHART_DIR="prod"

  stage('Git checkout - job configuration'){
  git branch: 'master', credentialsId: 'github', url: 'https://github.com/gazhaman/magento2-packer.git'
  }

  stage('Build new Image'){
    sh "echo ${BUILD_TIMESTAMP} ${params.BRANCH} ${env.BUILD_NUMBER}"
  }

}
}
catch(err){
   currentBuild.result = "FAILED"
   throw err
 }
finally {
  //do nothing
}
