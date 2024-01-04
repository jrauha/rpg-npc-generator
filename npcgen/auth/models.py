class User:
    def __init__(self, username, email, password, superuser=False, id=None):
        self.username = username
        self.email = email
        self.password = password
        self.superuser = superuser
        self.id = id
