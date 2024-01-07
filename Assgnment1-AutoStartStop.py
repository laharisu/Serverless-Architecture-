import boto3

ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    # Describe instances with Auto-Stop and Auto-Start tags
    instances_to_stop = ec2.describe_instances(
        Filters=[
            {'Name': 'tag:Action', 'Values': ['Auto-Stop']}
        ]
    )['Reservations']

    instances_to_start = ec2.describe_instances(
        Filters=[
            {'Name': 'tag:Action', 'Values': ['Auto-Start']}
        ]
    )['Reservations']

    # Stop the Auto-Stop instances
    for instance in instances_to_stop:
        for reservation in instance['Instances']:
            instance_id = reservation['InstanceId']
            ec2.stop_instances(InstanceIds=[instance_id])
            print(f'Stopped instance: {instance_id}')

    # Start the Auto-Start instances
    for instance in instances_to_start:
        for reservation in instance['Instances']:
            instance_id = reservation['InstanceId']
            ec2.start_instances(InstanceIds=[instance_id])
            print(f'Started instance: {instance_id}')