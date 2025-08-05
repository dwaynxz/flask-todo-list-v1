class TodoList:
    def __init__(self, to_do_list):
        self.list = to_do_list

    def add(self, item):
        length_of_list = len(self.list)
        self.list[length_of_list+1] = item

    def is_empty(self):
        if len(self.list) == 0:
            return True

    def clear_list(self):
        self.list.clear()

    def __repr__(self):
        return f"Todo List: {self.list}"

todo = TodoList({})

class ListManager:
    def __init__(self):
        self.lists = {}

    def is_empty(self):
        if len(self.lists) == 0:
            return True

    def add_list(self, title, todolist):
        id_ = len(self.lists)+1
        self.lists[(id_, title)] = todolist

    def get_key_by_id(self, id_):
        for key in self.lists.keys():
            if id_ in key:
                return key

    def __repr__(self):
        return f"Lists: {self.lists}"