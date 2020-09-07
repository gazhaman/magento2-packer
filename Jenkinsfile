try {
node ('master'){
  withCredentials([string(credentialsId: 'aws_access_key', variable: 'aws_access_key'), string(credentialsId: 'aws_secret_key', variable: 'aws_secret_key')])  {

  stage('Git checkout - job configuration'){
  git branch: 'master', credentialsId: 'github', url: 'https://github.com/gazhaman/magento2-packer.git'
  }

  env.BUILD_TIMESTAMP = "${new Date().format('yyyy/MM/dd/hh-MM-SS')}"

  stage('test'){
     ansiColor('xterm') {
    echo '\033[34mHello\033[0m \033[33mcolorful\033[0m \033[35mworld!\033[0m'
   }
  }
/*
  stage('Build new Image'){
    sh "packer build \
        -var 'aws_access_key=$aws_access_key' \
        -var 'aws_secret_key=$aws_secret_key' \
        -var 'jenkins_build=${env.BUILD_NUMBER}' \
        -var 'git_version=${params.BRANCH}' \
        -var 'timestamp=${BUILD_TIMESTAMP}' \
        vm-create.json"
  }
*/
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
