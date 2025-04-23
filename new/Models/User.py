class User:
    def __init__(self, username, password, user_id=None):
        self.id = user_id
        self.username = username
        self.password = password
