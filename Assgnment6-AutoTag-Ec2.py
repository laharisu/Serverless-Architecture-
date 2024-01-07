import boto3
import datetime

def lambda_handler(event, context):
    try:
        # Check if the event has a 'detail' field
        if 'detail' in event and 'instance-id' in event['detail']:
            # Initialize EC2 client
            ec2_client = boto3.client('ec2')

            # Retrieve the instance ID from the event
            instance_id = event['detail']['instance-id']

            # Define tags
            tags = [
                {'Key': 'BusinessOwner', 'Value': 'Subhra'},
                {'Key': 'production', 'Value': 'Lambda Boto3'},
                {'Key': 'LaunchDate', 'Value': datetime.datetime.utcnow().isoformat()}
                # You can add more custom tags as needed
            ]

            # Tag the new instance
            ec2_client.create_tags(Resources=[instance_id], Tags=tags)

            # Print a confirmation message for logging purposes
            print(f"Instance {instance_id} tagged successfully.")
        else:
            print("Event does not contain necessary details for EC2 instance tagging.")
    except Exception as e:
        print(f"Error: {e}")

    return {
        'statusCode': 200,
        'body': 'Instance tagged successfully.'
    }
