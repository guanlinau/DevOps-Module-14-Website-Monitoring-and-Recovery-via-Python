import boto3
import requests
import smtplib
import os
import paramiko
import time
import schedule
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
PASSWORD = os.getenv('PASSWORD')
NGINX_WEB_PORT= os.getenv('NGINX_WEB_PORT')

USERNAME=os.getenv('USERNAME')
KEY_FILENAME=os.getenv('KEY_FILENAME')
NGINX_CONTAINER_ID=os.getenv('NGINX_CONTAINER_ID')

#Get the ec2 instance id
WEBSITE_NGINX_SEVER_INSTANCE_ID=os.getenv('WEBSITE_NGINX_SEVER_INSTANCE_ID')


#Get all ec2 instances in sydney region
ec2_client = boto3.client('ec2', region_name='ap-southeast-2')


#Send notification
def send_notification (email_msg):
    print('Sending an notification email!')
    with smtplib.SMTP('smtp.gmail.com',587) as smtp:
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, PASSWORD)
        message =f"Subject: SITE DOWN!!!\n{email_msg}"
        smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS,message )


def get_instance_current_public_ip_address():
    # use the describe_instances method to get the public IP address of the instance
    nginx_server_instance = ec2_client.describe_instances(InstanceIds=[WEBSITE_NGINX_SEVER_INSTANCE_ID])
    # extract the public IP address from the response
    public_ip_address = nginx_server_instance['Reservations'][0]['Instances'][0]['PublicIpAddress']
    return  public_ip_address 

#Restart the nginx web container
def restart_container():
    print('Restarting the application container!')
    public_ip_address=get_instance_current_public_ip_address()

    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=public_ip_address, port=22, username=USERNAME, key_filename=KEY_FILENAME )
    stdin, stdout, stderr = ssh.exec_command(f'docker start {NGINX_CONTAINER_ID}')
    print(stdout.readlines())
    ssh.close()

#Reboot the host server: EC2 Instance 
def reboot_server_container():
    print('Restarting the server...')
   
    #Restart the EC2 instance server
    ec2_client.start_instances(
        InstanceIds=[
            WEBSITE_NGINX_SEVER_INSTANCE_ID,
        ],
    )
    print("started !!!!!!!!!!!!!!!!!")
    while True:
        server=ec2_client.start_instances(
            InstanceIds=[
                WEBSITE_NGINX_SEVER_INSTANCE_ID,
            ],
          )
        print(server['StartingInstances'][0]['CurrentState']['Name'])
        if server['StartingInstances'][0]['CurrentState']['Name'] == 'running':
            time.sleep(10)
            restart_container()
            break;

def monitor_application():
    try:
        public_ip_address=get_instance_current_public_ip_address()
        
        NGINX_WEB_URL= f'http://{public_ip_address}:{int(NGINX_WEB_PORT)}'
        response = requests.get(NGINX_WEB_URL)
        if response.status_code==200:
            print('Application is running successfully!')
        else:
            print("Application Down. Fix it!")
            # Send email to me
            email_msg = f"Application returned {response.status_code}, should be fixed soon!"
            send_notification(email_msg)
            restart_container()
    except Exception as ex:
        print(f'Connection error happened:{ex}')
        email_msg="Application not accessible at all!"
        send_notification(email_msg)
        time.sleep(20)
        reboot_server_container()

    
schedule.every(10).minutes.do(monitor_application)

while True:
    schedule.run_pending()