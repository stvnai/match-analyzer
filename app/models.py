from flask_login import UserMixin

class User(UserMixin):

    """
    Description:
    -----
        Class used to pass User type objects to Login Manager. 

    """
    def __init__(self, user_id, username):
        self.id= user_id
        self.username= username

    def get_id(self):
        return str(self.id)
    
    def __repr__(self):
        return f"<User {self.username}"