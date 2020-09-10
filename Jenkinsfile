try {
node ('master'){
  withCredentials([string(credentialsId: 'aws_access_key', variable: 'aws_access_key'), string(credentialsId: 'aws_secret_key', variable: 'aws_secret_key')])  {

  stage('Git checkout - job configuration'){
  git branch: 'master', credentialsId: 'github', url: 'https://github.com/gazhaman/magento2-packer.git'
  }

// general vars
  env.BUILD_TIMESTAMP = "${new Date().format('yyyy/MM/dd/hh-MM')}"
  env.PYTHONUNBUFFERED=1

// packer vars
  env.SOURCE_AMI = 'ami-0d15bdf2c7c21ffa7'
  env.INSTANCE_TYPE = 't2.micro'
  env.VPC_ID = 'vpc-1639e66e'
  env.SUBNET_ID = 'subnet-24a4001b'

// MagentoWEB ASG vars
  env.LT_ID_WEB = 'lt-005ab451cba87f311'
  env.SRC_VER_WEB = '27'
  env.ASG_NAME_WEB = 'MagentoWEB-ASG1'

//MagentoAdmin ASG vars
  env.LT_ID_ADMIN = 'lt-0c94b7ada80b6eba0'
  env.SRC_VER_ADMIN = '2'
  env.ASG_NAME_ADMIN = 'MagentoAdmin-ASG'

// AWS vars
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
        -var 'source_ami=${env.SOURCE_AMI}' \
        -var 'instance_type=${env.INSTANCE_TYPE}' \
        -var 'vpc_id=${env.VPC_ID}' \
        -var 'subnet_id=${env.SUBNET_ID}' \
        vm-create.json"
      }
    }
  }
/*
  dir('./ansible-jenkins'){
    stage('Enable maintenance'){
      sh "ansible-playbook -t maintenance_enable_web deploy.yml -vv"
    }
  }
*/
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

  stage('Update hosts file'){
    sh "python3 ec2.py"
  }

  dir('./ansible-jenkins'){

  stage('Setup upgrade'){
    sh "ansible-playbook -t setup_upgrade deploy.yml -vv"
  }

  stage('Enable Magento cache'){
    sh "ansible-playbook -t enable_magento_cache deploy.yml -vv"
  }

  stage('Clean Magento cache'){
    sh "ansible-playbook -t clean_magento_cache deploy.yml -vv"
  }

  stage('Enable crontab'){
    sh "ansible-playbook -t enable_crontab deploy.yml -vv"
  }
/*
  stage('Disable maintenance'){
    sh "ansible-playbook -t maintenance_disable_web deploy.yml -vv"
  }
*/
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
