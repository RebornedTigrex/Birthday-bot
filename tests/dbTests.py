from db import User, BirthdayRemind

class BaseTest:
    pass

class UserTest(BaseTest):
    User.get_or_create("0")
    User.get(kwargs="0")
    