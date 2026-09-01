class InvalidTodoTitleError(Exception):
    def __init__(self):
        super().__init__("Title Field Required")
