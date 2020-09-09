try {
node ('master'){
  withCredentials([string(credentialsId: 'aws_access_key', variable: 'aws_access_key'), string(credentialsId: 'aws_secret_key', variable: 'aws_secret_key')])  {

  stage('Git checkout - job configuration'){
  git branch: 'master', credentialsId: 'github', url: 'https://github.com/gazhaman/magento2-packer.git'
  }

  env.BUILD_TIMESTAMP = "${new Date().format('yyyy/MM/dd/hh-MM')}"
  env.PYTHONUNBUFFERED=1
/*
  stage('Build new Image'){
    ansiColor('css') {
    sh "packer build \
        -var 'aws_access_key=$aws_access_key' \
        -var 'aws_secret_key=$aws_secret_key' \
        -var 'jenkins_build=${env.BUILD_NUMBER}' \
        -var 'git_version=${params.BRANCH}' \
        -var 'timestamp=${BUILD_TIMESTAMP}' \
        vm-create.json"
      }
  }
*/
  dir('./ansible-jenkins'){

  stage('Packer build'){
    ansiColor('css') {
    sh "ansible-playbook -t packer_build deploy.yml -e 'aws_access_key=$aws_access_key \
                                                        aws_secret_key=$aws_secret_key \
                                                        jenkins_build=${env.BUILD_NUMBER} \
                                                        git_version=${params.BRANCH} \
                                                        timestamp=${BUILD_TIMESTAMP}' -vv"
    }
  }
}
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
