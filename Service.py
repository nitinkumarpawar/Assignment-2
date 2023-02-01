import os

from pprint import pprint

import boto3 as boto3
from flask import Response

table = os.getenv("freshers-example")
dynamo_client = boto3.resource(service_name='dynamodb', region_name='eu-west-1',
                               aws_access_key_id='ASIAX2KHRAJAWARNJJFC',
                               aws_secret_access_key='R3k5t65iDBDJBerzmorCAvuYuHzzDTmjKpEiZv3z',
                               aws_session_token='IQoJb3JpZ2luX2VjED4aCWV1LXdlc3QtMSJHMEUCIHjfs9G8w80n82FootQKaheiMwXoJiAAYzmCkE06zLV3AiEAt85CseuHja/9N1+i/1QJs2vAf7n4TnhJivp7NMZkaFQqnAMIt///////////ARADGgw1Mzc1NTc3OTUzOTMiDMiqx+6c2gkOXBfGDSrwAnnk+PnYYx33WBqZVkE8MJicd3oN7ElfiwaBbOJSuanIxaeRUpaRM/YnB/FB2WRFP5xQwX5CoEeTdYFF13/pooSv7FxccAvaA/3ICa5aY9HFGe/3oiJbMqYJqkOAafr51sPcsF+lo6zbs6OCJGNV6xReQX0x2JV6u04RYpsxqYxfx1HgI1kc+hQu7NHOoET+bjEra4RicAKc0bGRZgCJZXD5Px15XmuZoyGrMbkzZCdG3JBfgs7vJ/f5pMPQmCv4m4xXKa3OH6UMCjhKZuMmsnBFsZRRGzC1O/cxvRTHBzjEVmt/IWczu8yw6T+7h9+dLgN1UBza9TEsUUbw5qFCWzFmUescfGBgwaf5I75Ja7+/SqqdPhPA6tFlU9cX25UCs/VqiPF+IC10m0kON7EIDPM7sfs3B9k/kJx0QlrXzXTJO3y/SGn0WAY7X0DO89oGHlRvddMLaw28kLlqk23dhrmThr8d6Hh4kmaOHo0ZHsZKMLz6554GOqYBTckjKC+US97eyUGGGxGDahZcrZD4DW6QcCXEXRxXe7smKcHo2DrAYIJPG+4VVjmO77kdrFBEjmiHrFYeKuenLI2MgJzonIPbXZIw4WsG2rajX5uNXBUpC1IIh2vU7vu6thwCFSy9m27dztsF86PujQqpAmBCcu1PvzgE2M8fWTRA35G52a0K5MJlNbXGgWJteXMipHK5elJsiN5C7HALNImJLBLDTA==')
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
