import os
from datetime import date
from pprint import pprint
from email_validator import validate_email

import boto3 as boto3
from flask import Response

table = os.getenv("freshers-example")
dynamo_client = boto3.resource(service_name='dynamodb', region_name='eu-west-1',
                               aws_access_key_id='ASIAX2KHRAJA3K6KYR6G',
                               aws_secret_access_key='E02euMniPu8qLO3zLBSJFHZr1YuQhctBN5uZuOn/',
                               aws_session_token='IQoJb3JpZ2luX2VjECYaCWV1LXdlc3QtMSJHMEUCIQD6pac9qq88McSMi7Fri5dPoR4ta9l3/mC0pEDj6VZfygIgVqUQik48w8bESziSljROiKK7ufA+4xkAI8R5Y7BlnZAqnAMIn///////////ARADGgw1Mzc1NTc3OTUzOTMiDFqxv2doigOJMJUX9yrwAnV8gIMf5bDlowsZdJgvW27KnSShDe8qPHY8x0blVBVmy+B/FKAuH13U0FVQQcbx7A7rkE3TRapmHyNH0TCIrHFXnIGuBJW2m95ppebPzPW7BWd5/NSYf+erfzuVxIWpWuHaqIWUpeoEq2cle8d6qs9Fytfb8qyJLAjJX/nBqSzfSGDzb85OgNjFimRZbn/5bHQUZWcwyc+U+f9JB3Oe++ULJ8Hf3v8iZayj02PpTUDfnGdu4K+rcsXBYVc5OVzCAiio58GahdJZwt0JICEM3ZHLG5STLS8oeaB2NIA4mW1xF8bJkftDjCQo7LC00cmIpczbFk6gZ+h9or0Dghi9QnMyvpkOB1B4RzCJhArknkrnZtL3YZaIXbQ1PpQ+HZKEFc6GDKaWre7OVXQM6sZHm8IsMmH24fZK65hmYD+h9AsNUxKjgGLRHncwZb9xvdSi7/eeiEGh/HNdmhpGgWHUtXqOzUcn+oXA4BRQCRkg34gyMIrT4p4GOqYB1yAaIBCXJc33+geaY+UB3lriHhspmr73n4iNTJ7knhcUwhvdXSrxUjmtXjENANcwVfmbG5/ncFut/PiF6x+7etZQc2xAATC/oZwMVJfRCu4VbWT1xbQKZPLIgxT0gelbsT0WVFeykYnWF5tcKwgel6QKJbZhpsBUYJOkz0gxo0FWcOLrTLXBGrjpVOhZxJf7R6XfDB3Y1Evk1R/HcluvEz2rwCWBMQ=='
                               )
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


def get_que(data):
    response1 = __connected_table__.get_item(
        TableName="freshers-example",
        Key={
            'type': 'question',
            'sortKey': data['sortKey'],
        },

        ProjectionExpression="question"
    )
    pprint(response1)
    return Response("Fetching questions successfully", status=200)


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


def delete_answer(data):
    response = __connected_table__.delete_item(
        Key={
            'type': "answer",
            'sortKey': data['sortKey'],

        },

    )
    pprint(response)


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
            #':useridval': data['userId'],
            ':statusval': "1"
        },
        ProjectionExpression="question"
    )
    print(response)
