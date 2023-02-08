from unittest.mock import MagicMock, patch

from flask import Response
from pytest_mock import mocker

import Service
from Service import get_all_que, __connected_table__, get_que, que_by_status, delete_answer, put_answer


def test_get_all_que_failed(mocker):
    mock_get_all_que = MagicMock()
    mocker.patch.object(__connected_table__, "query", mock_get_all_que)
    mock_get_all_que.return_value = {'Items': {}}
    response = get_all_que()
    assert response.status_code == 404


def test_get_all_que_pass(mocker):
    mock_get_all_que = MagicMock()
    mocker.patch.object(__connected_table__, "query", mock_get_all_que)
    mock_get_all_que.return_value = {'Items': [{'question': 'What is Pytest?'}]}
    response = get_all_que()
    assert response.status_code == 200


def test_get_que_failed(mocker):
    mock_get_item = MagicMock()
    mocker.patch.object(__connected_table__, "query", mock_get_item)
    mock_get_item.return_value = {'Items': {}}
    response = get_que({'sortKey': '123'})
    assert response.status_code == 400
    assert response.get_data(as_text=True) == "Bad Request"


def test_get_que_pass(mocker):
    mock_get_item = MagicMock()
    mocker.patch.object(__connected_table__, "query", mock_get_item)
    mock_get_item.return_value = {'Items': [{'question': 'Explain about serverless?'}]}
    response = get_que({'sortKey': 'question#mugdha@harakirimail.com#5'})
    assert response.status_code == 200
    assert response.get_data(as_text=True) == "Fetching questions successfully"


def test_que_by_status_failed(mocker):
    mock_get_item = MagicMock()
    mocker.patch.object(__connected_table__, "query", mock_get_item)
    mock_get_item.return_value = {'Items': {}}
    response = que_by_status({'sortKey': '123'})
    assert response.status_code == 400
    assert response.get_data(as_text=True) == "Bad Request"


def test_que_by_status_pass(mocker):
    mock_get_item = MagicMock()
    mocker.patch.object(__connected_table__, "query", mock_get_item)
    mock_get_item.return_value = {'Items': [{'question': 'Explain about serverless?'}]}
    response = que_by_status({'sortKey': 'question#mugdha@harakirimail.com#5'})
    assert response.status_code == 200
    assert response.get_data(as_text=True) == "Fetching questions successfully"


def test_delete_answer_successful(mocker):
    response = {'ResponseMetadata': {'HTTPStatusCode': 200}}
    delete_ans = MagicMock()
    delete_ans.delete_item.return_value = response
    mocker.patch.object(Service.__connected_table__, 'delete_item', delete_ans)

    data = {'sortKey': 'answer#5#chetanarera111@gmail.com'}
    result = delete_answer(data)

    assert result.status_code == 200, "Unexpected status code"
    assert result.data == b'Successfully deleted', "Unexpected response data"


def test_put_answer(mocker):
    response_mock = MagicMock()
    mocker.patch.object(Service.__connected_table__, 'put_item', response_mock)
    # put_item_mock = mocker.patch('Service.put_answer', return_value=response_mock)
    data = {
        'sortKey': 'answer#5#chet_12@gmail.com',
        'answer': 'sample answer',
        'createdAt': '2023-02-03',
        'userId': 'chet_12@gmail.com'
    }
    print(response_mock)

    result = put_answer(data)

    # if result.status_code == 200:
    #     assert result.status_code == 200
    #     assert result.get_data() == b'Successfully added a answer'
    assert result.status_code == 200
    response_mock.assert_called_with(
        TableName='freshers-example',
        Item={
            'type': 'answer',
            'sortKey': data['sortKey'],
            'answer': data['answer'],
            'createdAt': data['createdAt'],
            'status': '1',
            'userId': data['userId']
        }
    )


def test_edit_question(mocker):
    response_mock = MagicMock()
    mocker.patch.object(Service.__connected_table__, 'update_item', response_mock)
    data = {
        'sortKey': 'question#nkp@gmail.com#10',
        'edited_que': 'new question text'
    }

    expected_update_response = {
        'Attributes': {
            'question': 'new question text'
        }
    }
    response_mock.update_item.return_value = expected_update_response
    response = Service.edit_question(data)

    # assert response == Response("Successfully updated", status=200)
    assert response.data == b'Successfully updated'
    assert response.status_code == 200

    response_mock.assert_called_with(
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
