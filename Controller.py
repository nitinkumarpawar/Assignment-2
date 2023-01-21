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
    que = get_que()
    print(que)
    print(Response("Fetching questions successfully", status=200))


# get_by_id()

def get_by_st():
    print("fetching active questions")
    que = que_by_status()
    print(que)
    print(Response("Fetching questions successfully", status=200))


# get_by_st()

def put():
    print("Enter your data")
    ans = put_answer()
    print(ans)
    print(Response("Successfully Enter", status=200))


# put()


def update():
    print("Enter your data")
    ans = edit_question()
    print(ans)
    print(Response("Successfully updated", status=200))


# update()


def delete():
    print("Enter your data")
    delete_answer()
    print(Response("Successfully deleted", status=200))

# delete()
