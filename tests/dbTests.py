from db import User

class BaseTest:
    pass

class UserTest(BaseTest): # TODO: Дописать
    User.get_or_create("0")
    User._get()
    