### Demo Project:
Website Monitoring and Recovery

### Technologies used:
Python, Linode, Docker, Linux

### Project Description:

1- Create a EC2 instance server on a AWS 

2- Install Docker and run a Nginx website as a container on the EC2 instance server

3- Write a Python script that monitors the website by accessing it and validating the HTTP response

4- Write a Python script that sends an email notification when website is down 

5- Write a Python script that automatically restarts the application & server when the application is down

### Usage Instruction

###### Step 1- Create a EC2 Instance server on AWS

![image](images/Screenshot%202023-04-16%20at%208.21.03%20pm.png)

###### Step 2- Install Docker on EC2 Instance server

###### Step 3- Create a nginx website as a docker container on EC2 Instance server.

![image](images/Screenshot%202023-04-16%20at%208.21.29%20pm.png)

#Update the security group with port 8080 to allow all traffic can get access to the website via port 8080

![image](images/Screenshot%202023-04-16%20at%208.10.31%20pm.png)

###### Step 4: Fill the env variables in to a .env file under the root directory
```
EMAIL_ADDRESS=
PASSWORD=

NGINX_WEB_PORT=

USERNAME=
KEY_FILENAME=
NGINX_CONTAINER_ID=

WEBSITE_NGINX_SEVER_INSTANCE_ID=
```

###### Step 5-Create requirements.txt and install the related libraries
```
pip freeze > requirements.txt
```
#Install boto3, schedule, paramiko, requests, python-dotenv library 
```
pip install -r requirements.txt
```

###### Step 6- Monitor the website by accessing it and validating the HTTP response
![image](images/Screenshot%202023-04-16%20at%208.33.03%20pm.png)

###### Step 7- Send an email notification when website is down or timeout

![image](images/Screenshot%202023-04-16%20at%2010.31.47%20pm.png)
![image](images/Screenshot%202023-04-16%20at%2010.38.55%20pm.png)

###### Step 8- Reboot and restart the server and container 
![image](images/Screenshot%202023-04-17%20at%201.48.51%20pm.png)