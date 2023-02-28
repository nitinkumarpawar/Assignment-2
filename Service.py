import os

from pprint import pprint

import boto3 as boto3
from flask import Response

table = os.getenv("freshers-example")
dynamo_client = boto3.resource(service_name='dynamodb', region_name='eu-west-1',
                               aws_access_key_id=',
                               aws_secret_access_key='',)
__connected_table__ = dynamo_client.Table("freshers-example")
print(__connected_table__.table_status)


def get_all_que():
    response = __connected_table__.query(
        KeyConditionExpression="#type = :type",
        ProjectionExpression='question',

        ExpressionAttributeNames={
            "#type": "type",

        },
        ExpressionAttributeValues={
            ":type": "question",

        }
    )
    pprint(response)
    return Response("Fetching questions successfully", status=200)


def get_que(data):
    response = __connected_table__.get_item(
        TableName="freshers-example",
        Key={
            'type': 'question',
            'sortKey': data['sortKey'],
        },

        ProjectionExpression="question"
    )
    pprint(response)

    if "Item" in response and response["Item"] != {}:
        print("SUCCESSFUL")
        return Response("Fetching questions successfully", status=200)
    else:
        print("INVALID UserId and QuestionID ")
        return Response("Bad Request", status=400)


def put_answer(data):
    item = {
        'type': 'answer',
        'sortKey': data['sortKey'],
        'answer': data['answer'],
        'createdAt': data['createdAt'],
        'status': 1,
        'userId': data['userId']

    }

    print(item)
    response = __connected_table__.put_item(
        TableName='freshers-example',
        Item=item
    )
    print(response)
    return Response("Successfully added a answer", status=200)


def edit_question(data):
    response = __connected_table__.update_item(
        Key={
            'type': "question",
            'sortKey': data['sortKey'],

        },
        UpdateExpression='SET question = :newQuestion',
        ExpressionAttributeValues={
            ':newQuestion': data['edited_que']
        },
        ReturnValues="UPDATED_NEW"
    )
    print(response)
    print(Response("Successfully updated", status=200))


def delete_answer(data):
    response = __connected_table__.delete_item(
        Key={
            'type': "answer",
            'sortKey': data['sortKey'],

        },

    )
    pprint(response)
    print(Response("Successfully deleted", status=200))


# --------------------------------------------------------------------------------
def que_by_status(data):
    response = __connected_table__.query(
        KeyConditionExpression='#type = :typeval and sortKey = :sortKey',
        FilterExpression='#status = :statusval',
        ExpressionAttributeNames={
            '#type': 'type',

            '#status': 'status'
        },
        ExpressionAttributeValues={
            ':typeval': 'question',
            ':sortKey': data['sortKey'],
            # ':useridval': data['userId'],
            ':statusval': "1"
        },
        ProjectionExpression="question"
    )

    if "Item" in response and response["Item"] != {}:
        print(response)
        print("SUCCESSFUL")
        return Response(status=200)
    else:
        print("INVALID UserId and QuestionID ")
        return Response(status=400)
