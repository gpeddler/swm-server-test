class InvalidTodoTitleError(Exception):
    def __init__(self):
        super().__init__("Title Field Required")


class DuplicateTodoTitleError(Exception):
    code = "DUPLICATE_TODO_TITLE"
    status_code = 409

    def __init__(self):
        super().__init__(self.code)
