import os


class Config:

    def __init__(self):
        """Base configuration variables."""
        self.SECRET_KEY = os.environ.get('SECRET_KEY')
        self.TRELLO_API_KEY = os.environ.get('TRELLO_API_KEY')
        self.TRELLO_TOKEN = os.environ.get('TRELLO_TOKEN')
        self.TRELLO_BOARD_NAME = os.environ.get('TRELLO_BOARD_NAME')

        if not self.SECRET_KEY:
            raise ValueError(
                "No SECRET_KEY set for Flask application. Did you follow the setup instructions?")
        if not self.TRELLO_API_KEY:
            raise ValueError(
                "No TRELLO_API_KEY set for Flask application. Did you follow the setup instructions?")
        if not self.TRELLO_TOKEN:
            raise ValueError(
                "No TRELLO_TOKEN set for Flask application. Did you follow the setup instructions?")
        if not self.TRELLO_BOARD_NAME:
            raise ValueError(
                "No TRELLO_BOARD_NAME set for Flask application. Did you follow the setup instructions?")
