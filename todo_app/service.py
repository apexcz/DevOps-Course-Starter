from datetime import datetime
import os
import requests
from todo_app.Item import Item

TRELLO_API_KEY = os.environ.get('TRELLO_API_KEY')
TRELLO_TOKEN = os.environ.get('TRELLO_TOKEN')
TRELLO_BASE_URL = 'https://api.trello.com/1'
TRELLO_BOARD_NAME = 'Tasky_1_2_3_'

class ItemService:
    def __init__(self):
        self.board_id = None
        self.todo_list_id = None
        self.done_list_id = None

        self.setup_board()
        
    def setup_board(self):
        self.board_id = self.search_board()
        if self.board_id == None:
            self.create_board()
        self.todo_list_id, self.done_list_id = self.get_board_lists(self.board_id)
        print('Set-up completed')

    def search_board(self):
        query = {
            'key': TRELLO_API_KEY,
            'token': TRELLO_TOKEN,
            'query': TRELLO_BOARD_NAME
        }
        response = requests.get(f'{TRELLO_BASE_URL}/search/', params=query).json()
        if response['boards']:
            return response['boards'][0]['id']
        return None

    def create_board(self):
        query = {
            'key': TRELLO_API_KEY,
            'token': TRELLO_TOKEN,
            'name': TRELLO_BOARD_NAME
        }
        response = requests.post(f'{TRELLO_BASE_URL}/boards/', params=query).json()
        self.board_id = response['id']
    
    def get_board_lists(self, board_id):
        query = {
            'key': TRELLO_API_KEY,
            'token': TRELLO_TOKEN
        }
        response = requests.get(f'{TRELLO_BASE_URL}/boards/{board_id}/lists', params=query).json()
        return response[0]['id'], response[2]['id']    


    def get_all_items(self):
        board_id = '608d26db02c3080bdee28ab7'
        query = {
            'key': TRELLO_API_KEY,
            'token': TRELLO_TOKEN
        }
        response = requests.get(f'{TRELLO_BASE_URL}/boards/{self.board_id}/cards', params=query).json()
        
        items = []
        for card in response:
            due_date= datetime.fromisoformat(card['due'][:-1]).strftime('%d/%m/%Y') if card['due'] else None
            status = 'Completed' if card['dueComplete'] == True else 'Not Started'
            item = Item(id=card['id'], status = status, title=card['name'], description=card['desc'], due_date=due_date)
            items.append(item)
        
        return items

    def create_item(self, title, description, due_date):
        query = {
            'key': TRELLO_API_KEY,
            'token': TRELLO_TOKEN,
            'name': title,
            'desc': description,
            'due': due_date,
            'idList': self.todo_list_id
        }
        requests.post(f'{TRELLO_BASE_URL}/cards/', params=query)
    
    def complete_item(self, item_id):
        query = {
            'key': TRELLO_API_KEY,
            'token': TRELLO_TOKEN,
            'idList': self.done_list_id,
            'dueComplete': 'true'
        }
        requests.put(f'{TRELLO_BASE_URL}/cards/{item_id}', params=query)

    def repeat_item(self, item_id):
        query = {
            'key': TRELLO_API_KEY,
            'token': TRELLO_TOKEN,
            'idList': self.todo_list_id,
            'dueComplete': 'false'
        }
        requests.put(f'{TRELLO_BASE_URL}/cards/{item_id}', params=query)
    
    def delete_item(self, item_id):
        query = {
            'key': TRELLO_API_KEY,
            'token': TRELLO_TOKEN,
            'closed': 'true'
        }
        requests.put(f'{TRELLO_BASE_URL}/cards/{item_id}', params=query)