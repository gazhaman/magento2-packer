try {
node ('master'){
  withCredentials([string(credentialsId: 'aws_access_key', variable: 'aws_access_key'), string(credentialsId: 'aws_secret_key', variable: 'aws_secret_key')])  {

  stage('Git checkout - job configuration'){
  git branch: 'master', credentialsId: 'github', url: 'https://github.com/gazhaman/magento2-packer.git'
  }

//Vars
  env.BUILD_TIMESTAMP = "${new Date().format('yyyy/MM/dd/hh-MM')}"
  env.PYTHONUNBUFFERED=1

  env.LT_ID_WEB = 'lt-005ab451cba87f311'
  env.SRC_VER_WEB = '27'
  env.ASG_NAME_WEB = 'MagentoWEB-ASG1'

  env.LT_ID_ADMIN = 'lt-0c94b7ada80b6eba0'
  env.SRC_VER_ADMIN = '2'
  env.ASG_NAME_ADMIN = 'MagentoAdmin-ASG'

  env.AWS_DEFAULT_REGION = 'us-east-1'
  env.AWS_ACCESS_KEY_ID = "$aws_access_key"
  env.AWS_SECRET_ACCESS_KEY = "$aws_secret_key"

  stage('Build new AMI'){
    if (params.AMI_ID == ''){
    ansiColor('gnome-terminal') {
    sh "packer build \
        -var 'aws_access_key=$aws_access_key' \
        -var 'aws_secret_key=$aws_secret_key' \
        -var 'jenkins_build=${env.BUILD_NUMBER}' \
        -var 'git_version=${params.BRANCH}' \
        -var 'timestamp=${BUILD_TIMESTAMP}' \
        vm-create.json"
      }
    }
  }

  stage('Update ASGs with new AMI'){
    parallel 'MagentoWEB-ASG': {
      sh "python3 update_ami.py ${env.BUILD_NUMBER}\
                                ${BUILD_TIMESTAMP} \
                                ${params.BRANCH} \
                                ${env.LT_ID_WEB} \
                                ${env.SRC_VER_WEB} \
                                ${env.ASG_NAME_WEB} \
                                ${params.AMI_ID}"
    }, 'MagentoADMIN-ASG': {
      sh "python3 update_ami.py ${env.BUILD_NUMBER}\
                                ${BUILD_TIMESTAMP} \
                                ${params.BRANCH} \
                                ${env.LT_ID_ADMIN} \
                                ${env.SRC_VER_ADMIN} \
                                ${env.ASG_NAME_ADMIN} \
                                ${params.AMI_ID}"

    }
  }


  dir('./ansible-jenkins'){

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
