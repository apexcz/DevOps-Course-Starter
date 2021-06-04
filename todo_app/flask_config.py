import os


class Config:
    """Base configuration variables."""
    SECRET_KEY = os.environ.get('SECRET_KEY')
    TRELLO_API_KEY = os.environ.get('TRELLO_API_KEY')
    TRELLO_TOKEN = os.environ.get('TRELLO_TOKEN')
    TRELLO_BOARD_NAME = 'Tasky_1_2_3_'

    if not SECRET_KEY:
        raise ValueError(
            "No SECRET_KEY set for Flask application. Did you follow the setup instructions?")
    if not TRELLO_API_KEY:
        raise ValueError(
            "No TRELLO_API_KEY set for Flask application. Did you follow the setup instructions?")
    if not TRELLO_TOKEN:
        raise ValueError(
            "No TRELLO_TOKEN set for Flask application. Did you follow the setup instructions?")
