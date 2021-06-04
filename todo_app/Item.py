class Item:
    def __init__(self, id, status, title, description='', due_date=None):
        self.id = id
        self.status = status
        self.title = title
        self.description = description
        self.due_date = due_date
