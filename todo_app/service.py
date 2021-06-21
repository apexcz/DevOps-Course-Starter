from datetime import datetime
import requests
from todo_app.Item import Item
from todo_app.board import Board

TRELLO_BASE_URL = 'https://api.trello.com/1'


class ItemService:

    def __init__(self):
        board = Board()
        self.TRELLO_API_KEY = board.get_config().TRELLO_API_KEY
        self.TRELLO_TOKEN = board.get_config().TRELLO_TOKEN
        self.TRELLO_BOARD_NAME = board.get_config().TRELLO_BOARD_NAME

        self.board_id = board.get_board_id()
        self.todo_list_id = board.get_todo_list_id()
        self.doing_list_id = board.get_doing_list_id()
        self.done_list_id = board.get_done_list_id()

    def get_all_items(self):
        query = {
            'key': self.TRELLO_API_KEY,
            'token': self.TRELLO_TOKEN
        }
        response = requests.get(
            f'{TRELLO_BASE_URL}/boards/{self.board_id}/cards', params=query).json()

        items = []
        for card in response:
            due_date = datetime.fromisoformat(
                card['due'][:-1]).strftime('%d/%m/%Y') if card['due'] else None
            status_dict = {
                self.todo_list_id: 'Todo',
                self.doing_list_id: 'Doing',
                self.done_list_id: 'Done'
            }
            card_idList = card['idList']
            status = status_dict[card_idList]
            item = Item(id=card['id'], status=status, title=card['name'],
                        description=card['desc'], due_date=due_date)
            items.append(item)

        return sorted(items, key=lambda x: x.title)

    def create_item(self, title, description, due_date):
        query = {
            'key': self.TRELLO_API_KEY,
            'token': self.TRELLO_TOKEN,
            'name': title,
            'desc': description,
            'due': due_date,
            'idList': self.todo_list_id
        }
        requests.post(f'{TRELLO_BASE_URL}/cards/', params=query)

    def move_to_doing(self, item_id):
        query = {
            'key': self.TRELLO_API_KEY,
            'token': self.TRELLO_TOKEN,
            'idList': self.doing_list_id,
            'dueComplete': 'false'
        }
        requests.put(f'{TRELLO_BASE_URL}/cards/{item_id}', params=query)

    def move_to_done(self, item_id):
        query = {
            'key': self.TRELLO_API_KEY,
            'token': self.TRELLO_TOKEN,
            'idList': self.done_list_id,
            'dueComplete': 'true'
        }
        requests.put(f'{TRELLO_BASE_URL}/cards/{item_id}', params=query)

    def move_to_todo(self, item_id):
        query = {
            'key': self.TRELLO_API_KEY,
            'token': self.TRELLO_TOKEN,
            'idList': self.todo_list_id,
            'dueComplete': 'false'
        }
        requests.put(f'{TRELLO_BASE_URL}/cards/{item_id}', params=query)

    def delete_item(self, item_id):
        query = {
            'key': self.TRELLO_API_KEY,
            'token': self.TRELLO_TOKEN,
            'closed': 'true'
        }
        requests.put(f'{TRELLO_BASE_URL}/cards/{item_id}', params=query)
