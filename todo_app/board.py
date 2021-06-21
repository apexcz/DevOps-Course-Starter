import requests
from todo_app.flask_config import Config

TRELLO_BASE_URL = 'https://api.trello.com/1'


class Board:
    """ 
    A representation of the trello board
    """

    def __init__(self):
        self.config, self.board_id, self.todo_list_id, self.doing_list_id, self.done_list_id = Board.setup_board()

    """
    Returns information about the trello board with the specified name, it creates a new board if board is not found
    """
    @staticmethod
    def setup_board():
        config = Config()
        TRELLO_API_KEY = config.TRELLO_API_KEY
        TRELLO_TOKEN = config.TRELLO_TOKEN
        TRELLO_BOARD_NAME = config.TRELLO_BOARD_NAME

        board_id = Board.find_board(
            TRELLO_API_KEY, TRELLO_TOKEN, TRELLO_BOARD_NAME)
        if board_id == None:
            board_id = Board.create_board(
                TRELLO_API_KEY, TRELLO_TOKEN, TRELLO_BOARD_NAME)
        todo_list_id, doing_list_id, done_list_id = Board.get_board_lists(
            TRELLO_API_KEY, TRELLO_TOKEN, board_id)
        print('Set-up completed')
        return config, board_id, todo_list_id, doing_list_id, done_list_id

    @staticmethod
    def find_board(trello_api_key, trello_token, trello_board_name):
        query = {
            'key': trello_api_key,
            'token': trello_token,
            'query': trello_board_name
        }
        response = requests.get(
            f'{TRELLO_BASE_URL}/search/', params=query).json()
        if response['boards']:
            return response['boards'][0]['id']
        return None

    @staticmethod
    def create_board(trello_api_key, trello_token, trello_board_name):
        query = {
            'key': trello_api_key,
            'token': trello_token,
            'name': trello_board_name
        }
        response = requests.post(
            f'{TRELLO_BASE_URL}/boards/', params=query).json()
        return response['id']

    @staticmethod
    def get_board_lists(trello_api_key, trello_token, board_id):
        query = {
            'key': trello_api_key,
            'token': trello_token
        }
        response = requests.get(
            f'{TRELLO_BASE_URL}/boards/{board_id}/lists', params=query).json()
        return response[0]['id'], response[1]['id'], response[2]['id']

    @staticmethod
    def delete_board(trello_api_key, trello_token, board_id):
        query = {
            'key': trello_api_key,
            'token': trello_token
        }
        response = requests.delete(
            f'{TRELLO_BASE_URL}/boards/{board_id}', params=query)
        return response

    def get_config(self):
        return self.config

    def get_board_id(self):
        return self.board_id

    def get_todo_list_id(self):
        return self.todo_list_id

    def get_doing_list_id(self):
        return self.doing_list_id

    def get_done_list_id(self):
        return self.done_list_id
