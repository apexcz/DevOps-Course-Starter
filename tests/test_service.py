"""Unit tests for service.py"""
from dotenv import load_dotenv, find_dotenv
from unittest.mock import Mock, patch
import pytest
from todo_app.service import ItemService
from tests.fixtures import trello_search_response, trello_list_repsonse, get_all_cards


@pytest.fixture
def service():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    with patch('requests.get') as mock_get_requests:
        mock_get_requests.side_effect = mock_trello_get_calls
        yield ItemService()


def mock_trello_get_calls(url, params):
    if url == 'https://api.trello.com/1/search/':
        response = Mock()
        response.json.return_value = trello_search_response
        return response
    elif url == 'https://api.trello.com/1/boards/123ecd32cbc39e8df38a4dd4/lists':
        response = Mock()
        response.json.return_value = trello_list_repsonse
        return response
    elif url == 'https://api.trello.com/1/boards/123ecd32cbc39e8df38a4dd4/cards':
        response = Mock()
        response.json.return_value = get_all_cards
        return response

    return None


def mock_trello_post_calls(url, params):
    if url == 'https://api.trello.com/1/cards/':
        response = Mock()
        response.return_value.status_code = 201
        return response

    return None


def mock_trello_put_calls(url, params):
    if 'https://api.trello.com/1/cards/' in url:
        response = Mock()
        response.return_value.status_code = 201
        return response

    return None


def test_get_all_cards_on_board(service):
    result = service.get_all_items()
    assert len(result) == 3
    assert result[0].title == 'Watch TV'
    assert result[0].status == 'Todo'
    assert result[1].title == 'Wash the dishes'
    assert result[1].status == 'Doing'
    assert result[2].title == 'Make breakfast'
    assert result[2].status == 'Done'
    pass


@patch('requests.post')
def test_create_item(mock_post_requests, service):
    mock_post_requests.side_effect = mock_trello_post_calls
    service.create_item('Take a Stroll', '', '')
    mock_post_requests.assert_called_once_with('https://api.trello.com/1/cards/', params={
                                               'key': 'trello-test-key', 'token': 'trello-test-token', 'name': 'Take a Stroll', 'desc': '', 'due': '', 'idList': '123ecd32cbc39e8df38a4aa1'})
    pass


@patch('requests.put')
def test_move_item_to_doing(mock_put_requests, service):
    mock_put_requests.side_effect = mock_trello_put_calls
    service.move_to_doing('608ed016bd1845410513126d')
    mock_put_requests.assert_called_once_with('https://api.trello.com/1/cards/608ed016bd1845410513126d', params={
                                              'key': 'trello-test-key', 'token': 'trello-test-token', 'idList': '123ecd32cbc39e8df38a4aa2', 'dueComplete': 'false'})
    pass


@patch('requests.put')
def test_move_item_to_done(mock_put_requests, service):
    mock_put_requests.side_effect = mock_trello_put_calls
    service.move_to_done('608ed05799d751331714c209')
    mock_put_requests.assert_called_once_with('https://api.trello.com/1/cards/608ed05799d751331714c209', params={
                                              'key': 'trello-test-key', 'token': 'trello-test-token', 'idList': '123ecd32cbc39e8df38a4aa3', 'dueComplete': 'true'})
    pass


@patch('requests.put')
def test_move_item_to_todo(mock_put_requests, service):
    mock_put_requests.side_effect = mock_trello_put_calls
    service.move_to_todo('60bf444c26adf480c4ab9e31')
    mock_put_requests.assert_called_once_with('https://api.trello.com/1/cards/60bf444c26adf480c4ab9e31', params={
                                              'key': 'trello-test-key', 'token': 'trello-test-token', 'idList': '123ecd32cbc39e8df38a4aa1', 'dueComplete': 'false'})
    pass


@patch('requests.put')
def test_delete_todo(mock_put_requests, service):
    mock_put_requests.side_effect = mock_trello_put_calls
    service.delete_item('608ed016bd1845410513126d')
    mock_put_requests.assert_called_once_with('https://api.trello.com/1/cards/608ed016bd1845410513126d', params={
                                              'key': 'trello-test-key', 'token': 'trello-test-token', 'closed': 'true'})
    pass
