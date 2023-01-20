import os
from datetime import date
from pprint import pprint
from email_validator import validate_email

import boto3 as boto3

table = os.getenv("freshers-example")
dynamo_client = boto3.resource(service_name='dynamodb', region_name='eu-west-1',
                               aws_access_key_id='ASIAX2KHRAJA742WACP2',
                               aws_secret_access_key='qOZzSJF+Af2WQpnzULYAmDLnNje79IbzfDGByFpk',
                               aws_session_token='IQoJb3JpZ2luX2VjEB0aCWV1LXdlc3QtMSJGMEQCIGEd0BIdEX7R2vTWNDiFWbuhD/HJ/xZYxhzAZCPy+ZVnAiAKh7LOoFrQX2qdwUtPxaiX02KV9OLIAsbgyaYAHV9nXiqcAwiG//////////8BEAMaDDUzNzU1Nzc5NTM5MyIMUDTiYaFrI18iajfxKvACcZnJ4x9qX+ZotPYWl26naDGnV36WCLgpNznE70edo8vW706gpnJ6/H9Hle/cqc+3hsRSWMFgXYH32a2+YiK3kca0+JzaX264jesI/V5AZlfnbAZPimYttDnUJGKot6G+GcDGSGtkOCAQfxWS+0fbXIyTExJsOYT1o8QHd4gDfPTRm5v9/lOvBmlnr5GrCBsq5m406uY0gVL6AXgmp2wqNCjwFBGv0aosU84GfUe0wlg03GFm4h5kE1JUItgBlyCnDV96H/FNF8dtEfRSYp6x2kS2jsWetIuscfiUEmpQfpE4HJ8k5M39wwjW1uu0ujLMFFTmzPDDGlX3DPH86Elhh2iCcdvUbmjVYRoCtFSrnn41ZhzXuX5wNTcIpvv+FH4Ltma9SHjuxfIvb3RuQ1uKsL5LOyYj1LEWwUODYLrfPgMk7LJYEUzqPQ9l9ww04mNkkwivjx85oc37irr0E5yjbLm+CjGv5XjSM+XGOIfiDCcw8reongY6pwHDSQ/qqwrCu2drt0NhEKHPPkbYj45E/nUjwj57ms7ivskd3C9uhIPtuVzTgt0kNwX7R9eHLHYPg2c1SnESRMR0NF0eBNHzI7M9nMETBzuFzOWaYDZllgoWS/C/D3mS2Yk91VUOpwLGMIyjIf0amU/Q7xDJ2wYNrsFgDG4BcLVYL4DduTKX675BjNaFQHSQrCGAqyQNTEu549SPS/sF0krkJB+YgicLtw==')
__connected_table__ = dynamo_client.Table("freshers-example")
print(__connected_table__.table_status)


def get_all_que():
    response = __connected_table__.query(
        KeyConditionExpression="#type = :type",
        ProjectionExpression='question',
        ExpressionAttributeNames={
            "#type": "type"

        },
        ExpressionAttributeValues={
            ":type": "question",

        }
    )
    pprint(response)


def get_que():
    userId = input("enter your userId: ")
    questionId = input("enter question Id: ")
    sortKey = "question#" + userId + "#" + questionId

    response1 = __connected_table__.get_item(
        TableName="freshers-example",
        Key={
            'type': 'question',
            'sortKey': sortKey,
        },

        ProjectionExpression="question"
    )

    pprint(response1)


def put_answer():
    answer = input("enter answer: ")
    userId = input("enter your userId: ")
    questionId = input("enter question Id: ")
    sortKey = "answer#" + questionId + "#" + userId
    createdAt = str(date.today())

    print(createdAt)

    item = {
        'type': 'answer',
        'sortKey': sortKey,
        'answer': answer,
        'createdAt': createdAt,
        'status': 1,
        'userId': userId

    }

    print(item)
    response = __connected_table__.put_item(
        TableName='freshers-example',
        Item=item
    )
    print(response)


def edit_question():
    userId = input("enter your userId: ")
    questionId = input("enter question Id: ")
    edited_que = input("edited question: ")
    sortKey = "question#" + userId + "#" + questionId

    response = __connected_table__.update_item(
        Key={
            'type': "question",
            'sortKey': sortKey,

        },
        UpdateExpression='SET question = :newQuestion',
        ExpressionAttributeValues={
            ':newQuestion': edited_que
        },
        ReturnValues="UPDATED_NEW"
    )
    print(response)


def delete_answer():
    userId = input("enter your userId: ")
    questionId = input("enter question Id: ")
    sortKey = "answer#" + questionId + "#" + userId
    response = __connected_table__.delete_item(
        Key={
            'type': "answer",
            'sortKey': sortKey,

        },

    )
    pprint(response)
