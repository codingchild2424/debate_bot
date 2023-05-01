
import boto3
from boto3.dynamodb.conditions import Key
from dotenv import dotenv_values

config = dotenv_values(".env")

AWS_ACCESS_KEY_ID = config.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config.get('AWS_SECRET_ACCESS_KEY')

# AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
# AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']


def get_db():

    dynamodb = boto3.resource(
        'dynamodb', 
        region_name='ap-northeast-2',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
    print("dynamodb connected", dynamodb)
    
    return dynamodb

# put_item
def put_item(table, item):

    print("item", item)

    response = table.put_item(Item=item)

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print('Item successfully inserted')
    else:
        print('Error inserting item')

# get_item
def get_item(table, item):

    response = table.get_item(Key=item)
    
    if 'Item' in response:
        print('Item successfully retrieved')
        return response['Item']
    else:
        print('Item not found')
        return None

def get_lastest_item(table, name_of_partition_key, value_of_partition_key):

    response = table.query (
        KeyConditionExpression=Key(name_of_partition_key).eq(value_of_partition_key),
        ScanIndexForward=True,
        Limit=10 # 1
    )
    
    return response['Items']