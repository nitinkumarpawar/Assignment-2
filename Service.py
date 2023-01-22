import os
from datetime import date
from pprint import pprint
from email_validator import validate_email

import boto3 as boto3

table = os.getenv("freshers-example")
dynamo_client = boto3.resource(service_name='dynamodb', region_name='eu-west-1',
                               aws_access_key_id='ASIAX2KHRAJA3OC5XT44',
                               aws_secret_access_key='Cevb/2SSZPTc0C0v5pqyPjPpj1ljicKS0IEntiyl',
                               aws_session_token='IQoJb3JpZ2luX2VjEEAaCWV1LXdlc3QtMSJHMEUCIEfwwIdhlJsEpvXkqEB7vbuDAFtfHUci8ULO5Wp8PcotAiEA0+rG7IAKJMgImM+EbNbNkx0WKrqFHjIhrhihV/R02Q4qnAMIqf//////////ARADGgw1Mzc1NTc3OTUzOTMiDGeOc3j8vmE6+upafirwAt3zvz9V23jTwMOZ2XNQCoiBWtkjFrZqaojMXkN3OYh2sqsNryDl/a9QjHrom4tDwfeq7pz0QdrEPlipz20ReS+jpkAjLyrBjePxL1fZn8SLtQZvOrRHu8a9FJ3t1yfuueToVvjd4LOrft0zwM5X+5AKMo+ksLomPW4Ajs77+tyrNVq3J7KwNHwk5EIUaiqpx3xPuCbFUnbE0i9i8TWxS3SCCye0cLZJ5yUEd7f4jkRE7KJ1MuC+/NWvbDKlXQT0QSUaPWTPC6TkbMV7LZG+yinA9nLrPF7jx92Mt0KcQ+TKBoIajLUHTWKkJsHDarxkGkLmx5FRMFZpvHt2cbQGHoiDH6oSKEhaQe16cTEsUAhonA6AhS7BHqc2dZ2tBnY8J34X3CqBSrTUfTCcRwLo8xu8mzTDlGpOZHUR4+4y6VSVOYBRzA/5Yp9KgQZCW9z2hTUbY1Vtn/rSySD0SiaIzvgrXqbPdMzRFokLoZt9z0STMM+TsJ4GOqYBgfVYqt65mZIt19WsX0ZxjTt94VcKbkuH8yRQP4GgGz9ksBJ67ATF9xrnYqsIS1NtyEyUJ8QN2IpBvaE/tr12ucZVuS2bzejvOpmHz7iWWB6cdPVA9x6r0KHDL3dEji9qAWFwjwu3JNBiVsh1UnD9+OOCIsvM/cilXN3RRsCN4DAk4vw2bBKYQjXIkX8gPkXHMBPHQ2scBm43VPK1zi/fCCub2vrc1Q=='
                               )
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


# --------------------------------------------------------------------------------
def que_by_status():
    userId = input("enter your userId: ")
    questionId = input("enter question Id: ")
    sortKey = "question#" + userId + "#" + questionId

    response = __connected_table__.query(
       KeyConditionExpression='#type = :typeval and sortKey = :sortKey',
       FilterExpression='#status = :statusval and userId = :useridval ',
       ExpressionAttributeNames={
        '#type': 'type',

        '#status': 'status'
       },
       ExpressionAttributeValues={
        ':typeval': 'question',
        ':sortKey': sortKey,
        ':useridval': userId,
        ':statusval': 1
       },
       ProjectionExpression="question"
    )
    print(response['Items'])
