class TodoList:
    def __init__(self):
        self.to_do_list = {}

    def add(self, item):
        length_of_list = len(self.to_do_list)
        self.to_do_list[length_of_list+1] = item

    def __repr__(self):
        return f"Todo List: {self.to_do_list}"

todo = TodoList