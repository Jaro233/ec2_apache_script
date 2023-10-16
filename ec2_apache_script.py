import boto3
import paramiko

# EC2 instance configuration
ec2_key_pair_name = 'ec2_apache'
instance_type = 't2.micro'
ami_id = 'ami-0bb4c991fa89d4b9b'  # Replace with an appropriate AMI ID
security_group_id = 'sg-0be228f63e272e0fb'  # Replace with your security group ID


# Connect to AWS EC2
ec2 = boto3.resource('ec2')

# Launch the EC2 instance
instance = ec2.create_instances(
    ImageId=ami_id,
    InstanceType=instance_type,
    KeyName=ec2_key_pair_name,
    SecurityGroupIds=[security_group_id],
    MinCount=1,
    MaxCount=1
)[0]

instance.wait_until_running()  # Wait for the instance to be in the running state

# Get the public IP address of the new instance
instance.load()
public_ip = instance.public_ip_address

# SSH into the instance to install Apache and upload the index.html file
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(public_ip, username='ec2-user', key_filename='ec2_apache.pem')

# Install Apache
ssh.exec_command('sudo yum update')
ssh.exec_command('sudo yum install httpd -y')
ssh.exec_command('sudo systemctl start httpd')
ssh.exec_command('sudo systemctl enable httpd')

# Create an SFTP client
sftp = ssh.open_sftp()

# Now, you can open the file without specifying the full path
with open('index.html', 'r') as html_file:
    sftp.putfo(html_file, '/var/www/html/index.html')

sftp.close()

# Close the SSH connection
ssh.close()

print(f'Instance with public IP {public_ip} created and configured.')

