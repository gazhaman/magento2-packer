import sys
build_number = sys.argv[1]
timestamp = sys.argv[2]
branch = sys.argv[3]
lt_id = sys.argv[4]
src_vers = sys.argv[5]
asg_name = sys.argv[6]
print(sys.argv)
ami_id = sys.argv[7] if len(sys.argv) == 8 else None

def update_ami(build_number, timestamp, branch, lt_id, src_vers, asg_name, ami_id):
    print(build_number, timestamp, branch, lt_id, src_vers, asg_name, ami_id)

    if ami_id is None:
        print(ami_id)
        print('is empty')
    else:
        print(ami_id)

update_ami(build_number, timestamp, branch, lt_id, src_vers, asg_name, ami_id)
