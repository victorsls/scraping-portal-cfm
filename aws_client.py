import boto3
from decouple import config


class AWSClient:
    def __init__(self):
        self.credentials = {
            'aws_access_key_id': config('ACCESS_KEY'),
            'aws_secret_access_key': config('SECRET_KEY'),
            'region_name': config('REGION_NAME')
        }
        self.dynamo_db_client = boto3.resource('dynamodb', **self.credentials)


class DynamoDBClient(AWSClient):
    def create_or_patch_item(self, table, item):
        return self.dynamo_db_client.Table(table).put_item(Item=item)
