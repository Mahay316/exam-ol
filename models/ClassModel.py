class Class:
    """
    班级类
    """
    # TODO 待实现
    @classmethod
    def get_tests_by_no(cls, cls_no: str):
        """
        根据课程号返回该课程下所拥有的全部考试对象

        :param cls_no: 课程号
        :return: list[Test]
        """


    # TODO 待实现
    @classmethod
    def get_students_by_no(cls, cls_no: str):
        """
        根据课程号返回该课程下所拥有的全部学生对象

        :param cls_no: 课程号
        :return: list[Student]
        """


    # TODO 待实现
    @classmethod
    def add_class_member(cls, cno, sno):
        """
        为班级增加学生

        :param cno: 课程号
        :param sno: 学生学号
        :return: 成功返回True， 学生已存在返回False
        """


    # TODO 待实现
    @classmethod
    def del_class_member(cls, cno, sno):
        """
        为班级删除学生

        :param cno: 课程号
        :param sno: 学生学号
        :return: 成功返回True，学生不存在返回False
        """
