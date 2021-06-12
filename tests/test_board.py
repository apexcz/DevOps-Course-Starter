"""Unit tests for board.py"""
from dotenv import load_dotenv, find_dotenv
from unittest.mock import Mock, patch
import pytest
from todo_app.board import Board
from tests.fixtures import trello_search_response, trello_list_repsonse


@pytest.fixture
def board():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    with patch('requests.get') as mock_get_requests:
        mock_get_requests.side_effect = mock_trello_calls
        yield Board()


def mock_trello_calls(url, params):
    if url == 'https://api.trello.com/1/search/':
        response = Mock()
        response.json.return_value = trello_search_response
        return response
    elif url == 'https://api.trello.com/1/boards/123ecd32cbc39e8df38a4dd4/lists':
        response = Mock()
        response.json.return_value = trello_list_repsonse
        return response

    return None


def mock_trello_delete_calls(url, params):
    if 'https://api.trello.com/1/boards/' in url:
        response = Mock()
        response.return_value.status_code = 200
        return response

    return None


def test_board(board):
    assert board.get_board_id() == '123ecd32cbc39e8df38a4dd4'
    assert board.get_todo_list_id() == '123ecd32cbc39e8df38a4aa1'
    assert board.get_doing_list_id() == '123ecd32cbc39e8df38a4aa2'
    assert board.get_done_list_id() == '123ecd32cbc39e8df38a4aa3'
    pass


@patch('requests.delete')
def test_delete_board(mock_put_requests):
    mock_put_requests.side_effect = mock_trello_delete_calls
    Board.delete_board('trello-test-key', 'trello-test-token',
                       '123ecd32cbc39e8df38a4dd4')
    mock_put_requests.assert_called_once_with('https://api.trello.com/1/boards/123ecd32cbc39e8df38a4dd4', params={
                                              'key': 'trello-test-key', 'token': 'trello-test-token'})
    pass
