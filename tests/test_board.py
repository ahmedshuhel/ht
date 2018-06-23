import mock
from h.models.board import Board
from h.models.list import List
from datetime import datetime


title = 'Board title'
desc = 'This is description'
created_at = datetime.min


def create_board():
    return Board(title=title, description=desc)


def create_list():
    return List(title=title)


@mock.patch('h.models.base.uuid4')
def test_create_board(mock_uuid4):
    uuid = 'a1b2c3'
    mock_uuid4.return_value = uuid
    board = create_board()
    assert board.title == title
    assert board.description == desc
    assert board.id == uuid


@mock.patch('h.models.base.datetime')
def test_has_created_at(mock_datetime):
    mock_datetime.now.return_value = datetime.min
    board = create_board()
    assert board.created_at == created_at


def test_add_list():
    list = create_list()
    board = create_board()

    board.add_list(list)

    assert len(board.lists) == 1
    assert board.lists[0].title == title


def test_remove_list():
    list = create_list()
    board = create_board()

    board.add_list(list)
    assert len(board.lists) == 1
    board.remove_list(list)
    assert len(board.lists) == 0
