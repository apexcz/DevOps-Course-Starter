TODO = 'Todo'
DOING = 'Doing'
DONE = 'Done'


class ViewModel:
    def __init__(self, items):
        self._items = items

    @property
    def to_do_items(self):
        return [x for x in self._items if x.status == TODO]

    @property
    def doing_items(self):
        return [x for x in self._items if x.status == DOING]

    @property
    def done_items(self):
        return [x for x in self._items if x.status == DONE]
