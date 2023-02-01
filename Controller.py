from datetime import date

from Service import get_que, put_answer, delete_answer, get_all_que, edit_question, que_by_status
from flask import Response


def get_all():
    print("fetching all questions")
    que = get_all_que()
    print(que)
    print(Response("Fetching questions successfully", status=200))


# get_all()


def get_by_id():
    print("fetching question by ID")
    userId = input("enter your userId: ")
    questionId = input("enter question Id: ")
    sortKey = "question#" + userId + "#" + questionId

    data = {
        "userId": userId,
        "questionId": questionId,
        "sortKey": sortKey
    }
    que = get_que(data)
    print(que)


# get_by_id()


def get_by_st():
    print("fetching active questions")
    userId = input("enter your userId: ")
    questionId = input("enter question Id: ")
    sortKey = "question#" + userId + "#" + questionId
    data = {
        "userId": userId,
        "questionId": questionId,
        "sortKey": sortKey
    }
    que = que_by_status(data)
    print(que)
    print(Response("Fetching questions successfully", status=200))


get_by_st()


def put():
    print("Enter your data")
    answer = input("enter answer: ")
    userId = input("enter your userId: ")
    questionId = input("enter question Id: ")
    sortKey = "answer#" + questionId + "#" + userId
    createdAt = str(date.today())
    data = {
        "userId": userId,
        "questionId": questionId,
        "sortKey": sortKey,
        "createdAt": createdAt,
        "answer": answer
    }
    ans = put_answer(data)
    print(ans)
    print(Response("Successfully Enter", status=200))


# put()

def update():
    print("Enter your data")
    userId = input("enter your userId: ")
    questionId = input("enter question Id: ")
    edited_que = input("edited question: ")
    sortKey = "question#" + userId + "#" + questionId
    data = {
        "userId": userId,
        "questionId": questionId,
        "sortKey": sortKey,
        "edited_que": edited_que
    }
    ans = edit_question(data)
    print(ans)
    print(Response("Successfully updated", status=200))


# update()


def delete():
    print("Enter your data")
    userId = input("enter your userId: ")
    questionId = input("enter question Id: ")
    sortKey = "answer#" + questionId + "#" + userId
    data = {
        "userId": userId,
        "questionId": questionId,
        "sortKey": sortKey
    }
    delete_answer(data)
    print(Response("Successfully deleted", status=200))

# delete()
