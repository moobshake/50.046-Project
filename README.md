# 50.046-Project
This repository contains the code to the AWS services and our RPI.
# RPI
Simply git clone this repository to the RPI with Raspbian OS installed. Run the following code to get started:  
1. Install all the requirements. Make sure to use python3 (should be pre-installed with Raspbian)
```bash
pip3 install -r requirements.txt
```
2. With all the relevant python library installed, you can now run the main program.
```bash
python3 main.py
```
**NOTE:** Please change all the S3 bucket names and MQTT connection to your own AWS endpoint. The ones that we have are not working anymore.
# AWS Services
We are using AWS Lambda and Rekognition. You can find the relevant codes in the *aws_codes* folder. Refer to our final report for each of the services we used. Simply upload the code in this folder to the relevant services. Please follow the documentation in AWS to get started.