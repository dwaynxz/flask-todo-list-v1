class TodoList:
    def __init__(self):
        self.list = {}

    def add(self, item):
        length_of_list = len(self.list)
        self.list[length_of_list+1] = item

    def is_empty(self):
        if len(self.list) == 0:
            return True

    def __repr__(self):
        return f"Todo List: {self.list}"

todo = TodoList()