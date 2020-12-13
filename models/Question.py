class Question:
    qno = None # str
    qtype = None # 'select', 'multi', 'fill'
    qstem = None # str
    qanswer = None # 全体选项json字符串，填空题也是"A":xxx的格式，字母代表顺序
    qselect = None # str for 'select', None for 'fill'
    qsubject = None
    qreference = None
    qisdeleted = None

    def is_fill_in_blanks(self):
        """
        本题是否为填空题

        :return: True if 是填空题 else False
        """