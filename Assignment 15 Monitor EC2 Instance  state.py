Assignment 15: Monitor EC2 Instance State Changes Using AWS Lambda, Boto3, and SNS

import boto3
import json

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    sns = boto3.client('sns')

    instances = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['stopped', 'RUNNING', 'Rebooted']}])['Reservations']

    stopped_instances = []
    for reservation in instances:
        for instance in reservation['Instances']:
            stopped_instances.append(instance['InstanceId'])

    if stopped_instances:
        message = "The following EC2 instances have been stopped:\n" + "\n".join(stopped_instances)
        sns.publish(TopicArn="arn:aws:sns:ap-south-1:179482357736:EC2StateChanges", Message=message, Subject="EC2 Instance State Change")

    RUNNING_instances = []
    for reservation in instances:
        for instance in reservation['Instances']:
            RUNNING_instances.append(instance['InstanceId'])

    if RUNNING_instances:
        message = "The following EC2 instances have been running:\n" + "\n".join(RUNNING_instances)
        sns.publish(TopicArn="arn:aws:sns:ap-south-1:179482357736:EC2StateChanges", Message=message, Subject="EC2 Instance State Change")

    Rebooted_instances = []
    for reservation in instances:
        for instance in reservation['Instances']:
            Rebooted_instances.append(instance['InstanceId'])

    if Rebooted_instances:
        message = "The following EC2 instances have been rebooted:\n" + "\n".join(Rebooted_instances)
        sns.publish(TopicArn="arn:aws:sns:ap-south-1:179482357736:EC2StateChanges", Message=message, Subject="EC2 Instance State Change")
