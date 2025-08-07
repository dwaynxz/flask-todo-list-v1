class TodoList:
    def __init__(self, to_do_list):
        self.list = to_do_list

    def add(self, item):
        length_of_list = len(self.list)
        self.list[(length_of_list+1, False)] = item

    def is_empty(self):
        if len(self.list) == 0:
            return True

    def clear_list(self):
        self.list.clear()

    def delete_task(self, key):
        self.list.pop(key)

    def get_status_by_task_id(self, inp_task_id):
        for task_id, status in self.list.keys():
            if inp_task_id == task_id:
                return status

    def mark_task_done(self, inp_task_id):
        change_status(self.list, inp_task_id, True)

    def mark_task_undone(self, inp_task_id):
        change_status(self.list, inp_task_id, False)

    def get_key_by_id(self, inp_task_id):
        for task_id, status in self.list.keys():
            if inp_task_id == task_id:
                return (task_id, status)


    @staticmethod
    def get_id_by_status_id(status_id):
        return status_id[0]

    def __repr__(self):
        return f"Todo List: {self.list}"

def change_status(inp_dict, inp_task_id, new_status):
    for key in list(inp_dict.keys()):
        id_, status = key
        if inp_task_id == id_:
            new_key = (id_, new_status)
            inp_dict[new_key] = inp_dict[key]
            inp_dict.pop(key)
            break

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

    def delete_list(self, key):
        self.lists.pop(key)

    def __repr__(self):
        return f"Lists: {self.lists}"