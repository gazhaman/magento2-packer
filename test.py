ref_status = 'Successful'
asg_name = 'MagentoWEB-ASG1'
asg_res = {'InstanceRefreshId': '2323424'}

if ref_status != 'Pending':
    raise Exeception("ASG update failed.\nASG name:" + asg_name + "\nInstance Refresh ID:" + asg_res['InstanceRefreshId'] + "\nStatus:" + ref_status)
