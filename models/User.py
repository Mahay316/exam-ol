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
    def has_this_Test(self, test: Test):
        """
        返回该学生是否有本次考试

        :return True or False
        """
