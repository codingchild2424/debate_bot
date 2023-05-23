import boto3
import streamlit as st

from boto3.dynamodb.conditions import Key
from dotenv import dotenv_values

config = dotenv_values(".env")

if config:
    AWS_ACCESS_KEY_ID = config.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config.get('AWS_SECRET_ACCESS_KEY')
else:
    AWS_ACCESS_KEY_ID = st.secrets['AWS_ACCESS_KEY_ID'] 
    AWS_SECRET_ACCESS_KEY = st.secrets['AWS_SECRET_ACCESS_KEY']


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

def get_lastest_item(table, name_of_partition_key, value_of_partition_key, limit_num=10):

    response = table.query(
        KeyConditionExpression=Key(name_of_partition_key).eq(value_of_partition_key),
        ScanIndexForward=False,
        Limit=limit_num
    )
    
    return response['Items']

def get_all_items(table, name_of_key):

    response = table.scan()
    data = response['Items']

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])
    
    items = set(d[name_of_key] for d in data)
    return items