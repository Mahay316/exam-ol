from . import Test


class User:
    def __init__(self, role):
        self.role = role

    def is_mentor(self):
        pass

    def is_student(self):
        pass

    def is_admin(self):
        pass


class Student(User):
    def has_this_Test(test: Test):
        # 返回
        pass