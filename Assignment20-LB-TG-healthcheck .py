import boto3
import json

def lambda_handler(event, context):
    elb_name = 'ASG-nginx-test-LB'  # Replace with your ELB name
    sns_topic_arn = 'arn:aws:sns:ap-south-1:179482357736:LoadBalancerHealthTopic'  # Replace with your SNS Topic ARN

    elbv2_client = boto3.client('elbv2')
    sns_client = boto3.client('sns')

    # Check the health of registered instances behind the ELB
    response = elbv2_client.describe_target_health(TargetGroupArn='arn:aws:elasticloadbalancing:ap-south-1:179482357736:targetgroup/ASG-nginx-test-LB-TG/f475161afe303257')  # Replace with your Target Group ARN

    unhealthy_instances = [instance['Target']['Id'] for instance in response['TargetHealthDescriptions'] if
                           instance['TargetHealth']['State'] != 'healthy']

    if unhealthy_instances:
        # Publish detailed message to SNS if any instances are unhealthy
        message = f"Unhealthy instances found behind {elb_name}: {', '.join(unhealthy_instances)}"
        sns_client.publish(TopicArn=sns_topic_arn, Message=message, Subject='Unhealthy Instances Alert')
