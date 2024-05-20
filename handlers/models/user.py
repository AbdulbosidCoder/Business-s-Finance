from pydantic import BaseModel


class User(BaseModel):
    id: int = 1
    username: str
    password: str
    phone: str
    telegram_id: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = User.id_counter()

    @staticmethod
    def id_counter():
        if not hasattr(User, 'counter'):
            User.id_counter = 0
        User.id_counter += 1
        return User.id_counter

    def save(self, db):
        return db.create_user(self)



    @staticmethod
    def get_user_by_username(username,db):
        return db.find_user_by_username(username)











