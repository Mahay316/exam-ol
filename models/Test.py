class Test:
    @staticmethod
    def get_test(examID: str):
        """
        根据考试号返回Test(考试)对象

        :param examID:
        :return: 返回Test对象，如果考试不存在则返回None
        """

    @staticmethod
    def get_all_question_id(examID: str) -> list:
        """
        根据考试号返回考试的全部题目id

        :param examID: 考试号
        :return: 所有id做成一个list返回，每个id均为str类型
        """

    def get_begin_time(self):
        """
        获得考试开始时间，类型是datetime
        """

    def get_end_time(self):
        """
        获取考试结束时间

        :return: 类型是datetime, 如果考试不限时间则返回None
        """

    def get_all_questions(self) -> list:
        """
        获取本考试的所有试题

        :return: 返回list[Question]
        """
