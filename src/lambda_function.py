import boto3
import json
import os
import datetime
from pprint import pprint

table_name = os.environ['TABLE_NAME']
print('SET UP')
if 'ENDPOINT' in os.environ and os.getenv('ENDPOINT') != 'default':
    print("USING LOCAL ENDPOINT")
    print(os.getenv('ENDPOINT'))
    dynamodb = boto3.resource('dynamodb', endpoint_url=os.getenv('ENDPOINT'))
else:
    dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(table_name)

def list_handler(event, context):
    print("Using table:" + table_name)
    print("Received event: " + json.dumps(event, indent=2))   
    r = table.scan(Limit=10)
    return {
        'statusCode': '200',
        'body': str(r.get('Items', '')),
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def put_handler(event, context):
    print("Using table:" + table_name)
    print("Received event: " + json.dumps(event, indent=2))   
    ts=datetime.datetime.now().timestamp()
    dt=str(datetime.datetime.now())
    r = table.put_item(
        Item={'mykey': str(ts), 'dt': dt},
        ReturnConsumedCapacity="TOTAL"
    )
    return {
        'statusCode': '200',
        'body': str(r),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


if __name__ == '__main__':
	print(put_handler({}, {}))
