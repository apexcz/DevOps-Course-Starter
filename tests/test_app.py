"""Integration tests for app.py"""
from dotenv import load_dotenv, find_dotenv
from unittest.mock import Mock, patch
import pytest
from todo_app import app
from tests.fixtures import trello_search_response, trello_list_repsonse, get_all_cards

@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    with patch('requests.get') as mock_get_requests:
        mock_get_requests.side_effect = mock_get_lists
        test_app = app.create_app()
        yield test_app.test_client()


def mock_get_lists(url, params):
    if url == 'https://api.trello.com/1/search/':
        response = Mock()
        response.json.return_value = trello_search_response
        response.return_value.status_code = 200
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


def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Watch TV' in response.data
    assert b'Wash the dishes' in response.data
    assert b'Make breakfast' in response.data
    pass


@patch('requests.post')
def test_create_item(mock_post_requests, client):
    mock_post_requests.side_effect = mock_trello_post_calls
    body = {
        'title': 'Visit Sarah'
    }
    response = client.post('/', data=body)
    assert response.status_code == 302
    pass


@patch('requests.put')
def test_move_item_to_doing(mock_put_requests, client):
    mock_put_requests.side_effect = mock_trello_put_calls
    body = {
        'todo_id': '608ed016bd1845410513126d'
    }
    response = client.post('/move-to-doing', data=body)
    assert response.status_code == 302
    pass


@patch('requests.put')
def test_move_item_to_done(mock_put_requests, client):
    mock_put_requests.side_effect = mock_trello_put_calls
    body = {
        'todo_id': '608ed05799d751331714c209'
    }
    response = client.post('/move-to-done', data=body)
    assert response.status_code == 302
    pass


@patch('requests.put')
def test_move_item_to_todo(mock_put_requests, client):
    mock_put_requests.side_effect = mock_trello_put_calls
    body = {
        'todo_id': '60bf444c26adf480c4ab9e31'
    }
    response = client.post('/move-to-todo', data=body)
    assert response.status_code == 302
    pass


@patch('requests.put')
def test_delete_item(mock_put_requests, client):
    mock_put_requests.side_effect = mock_trello_put_calls
    body = {
        'todo_id': '608ed016bd1845410513126d'
    }
    response = client.post('/delete-item', data=body)
    assert response.status_code == 302
    pass
