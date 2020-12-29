-- ----------------------------
-- 含有密码字段的表均加入了两种记录：未加密版本和MD5加密版本
-- 且密码均为123456
-- 用于支持系统开发的不同阶段的测试工作
-- ----------------------------
INSERT INTO `admin`(`Ano`, `Apassword`) VALUES ('admin', '123456');
INSERT INTO `admin`(`Ano`, `Apassword`) VALUES ('admin_en', 'e10adc3949ba59abbe56e057f20f883e');

INSERT INTO `mentor`(`Mno`, `Mname`, `Mgender`, `Mtitle`, `Mpassword`) VALUES ('teacher1', '张三', '男', '副教授', '123456');
INSERT INTO `mentor`(`Mno`, `Mname`, `Mgender`, `Mtitle`, `Mpassword`) VALUES ('teacher1_en', '张三', '男', '副教授', 'e10adc3949ba59abbe56e057f20f883e');
INSERT INTO `mentor`(`Mno`, `Mname`, `Mgender`, `Mtitle`, `Mpassword`) VALUES ('teacher2', '李四', '女', '教授', '123456');
INSERT INTO `mentor`(`Mno`, `Mname`, `Mgender`, `Mtitle`, `Mpassword`) VALUES ('teacher2_en', '李四', '女', '教授', 'e10adc3949ba59abbe56e057f20f883e');
INSERT INTO `mentor`(`Mno`, `Mname`, `Mgender`, `Mtitle`, `Mpassword`) VALUES ('teacher3', 'Peter', '男', '讲师', '123456');
INSERT INTO `mentor`(`Mno`, `Mname`, `Mgender`, `Mtitle`, `Mpassword`) VALUES ('teacher3_en', 'Peter', '男', '讲师', 'e10adc3949ba59abbe56e057f20f883e');

INSERT INTO `student`(`Sno`, `Sname`, `Sgender`, `Smajor`, `Spassword`) VALUES ('student1', '李明', '男', '软件工程', '123456');
INSERT INTO `student`(`Sno`, `Sname`, `Sgender`, `Smajor`, `Spassword`) VALUES ('student1_en', '李明', '男', '软件工程', 'e10adc3949ba59abbe56e057f20f883e');
INSERT INTO `student`(`Sno`, `Sname`, `Sgender`, `Smajor`, `Spassword`) VALUES ('student2', 'Mary', '女', '信息安全', '123456');
INSERT INTO `student`(`Sno`, `Sname`, `Sgender`, `Smajor`, `Spassword`) VALUES ('student2_en', 'Mary', '女', '信息安全', 'e10adc3949ba59abbe56e057f20f883e');
INSERT INTO `student`(`Sno`, `Sname`, `Sgender`, `Smajor`, `Spassword`) VALUES ('student3', '王丽', '女', '软件工程', '123456');
INSERT INTO `student`(`Sno`, `Sname`, `Sgender`, `Smajor`, `Spassword`) VALUES ('student3_en', '王丽', '女', '软件工程', 'e10adc3949ba59abbe56e057f20f883e');
INSERT INTO `student`(`Sno`, `Sname`, `Sgender`, `Smajor`, `Spassword`) VALUES ('student4', 'Антон', '男', '核工程', '123456');
INSERT INTO `student`(`Sno`, `Sname`, `Sgender`, `Smajor`, `Spassword`) VALUES ('student4_en', 'Антон', '男', '核工程', 'e10adc3949ba59abbe56e057f20f883e');

INSERT INTO `subject`(`Subname`) VALUES ('软件工程');
INSERT INTO `subject`(`Subname`) VALUES ('数据库原理');
INSERT INTO `subject`(`Subname`) VALUES ('编译原理');
INSERT INTO `subject`(`Subname`) VALUES ('流体力学');
INSERT INTO `subject`(`Subname`) VALUES ('工程热力学');
INSERT INTO `subject`(`Subname`) VALUES ('C语言程序设计');
INSERT INTO `subject`(`Subname`) VALUES ('Java高级语言程序设计');

INSERT INTO `course`(`Cname`, `Subno`, `Mno`) VALUES ('数据库教学班1', 2, 'teacher1');
INSERT INTO `course`(`Cname`, `Subno`, `Mno`) VALUES ('数据库教学班2', 2, 'teacher1');
INSERT INTO `course`(`Cname`, `Subno`, `Mno`) VALUES ('数据库教学班3', 2, 'teacher1_en');
INSERT INTO `course`(`Cname`, `Subno`, `Mno`) VALUES ('流体力学1', 4, 'teacher2');
INSERT INTO `course`(`Cname`, `Subno`, `Mno`) VALUES ('流体力学2', 4, 'teacher2_en');

INSERT INTO `paper`(`Pname`, `Pnum`, `Pscore`, `Preference`, `Pisdeleted`, `Subno`) VALUES ('数据库基础卷', 3, 17, 0, 0, 2);
INSERT INTO `paper`(`Pname`, `Pnum`, `Pscore`, `Preference`, `Pisdeleted`, `Subno`) VALUES ('数据库提高卷', 0, 0, 0, 0, 2);
INSERT INTO `paper`(`Pname`, `Pnum`, `Pscore`, `Preference`, `Pisdeleted`, `Subno`) VALUES ('流体力学基础卷', 1, 4, 0, 1, 4);
INSERT INTO `paper`(`Pname`, `Pnum`, `Pscore`, `Preference`, `Pisdeleted`, `Subno`) VALUES ('软件工程提高卷', 0, 0, 0, 0, 1);

INSERT INTO `question`(`Qtype`, `Qstem`, `Qanswer`, `Qselect`, `Subno`, `Qreference`, `Qisdeleted`) VALUES ('select', '这是一道数据库单选题()', '{\"A\": \"我是A\", \"B\": \"我是B\", \"C\": \"我是C\". \"D\": \"我是D\"}', 'A', 2, 0, 1);
INSERT INTO `question`(`Qtype`, `Qstem`, `Qanswer`, `Qselect`, `Subno`, `Qreference`, `Qisdeleted`) VALUES ('multi', '这是一道流体力学多选题()', '{\"A\": \"我是A\", \"B\": \"我是B\", \"C\": \"我是C\". \"D\": \"我是D\", \"E\": \"我是E\"}', 'ABC', 1, 0, 0);
INSERT INTO `question`(`Qtype`, `Qstem`, `Qanswer`, `Qselect`, `Subno`, `Qreference`, `Qisdeleted`) VALUES ('fill', '这是一道[填空]填空[填空]', '{\"A\": \"编译原理\", \"B\": \"题\"}', NULL, 3, 0, 0);

INSERT INTO `question_paper`(`Pno`, `Qno`, `QPscore`, `QPposition`) VALUES (1, 1, 2, 1);
INSERT INTO `question_paper`(`Pno`, `Qno`, `QPscore`, `QPposition`) VALUES (1, 2, 10, 3);
INSERT INTO `question_paper`(`Pno`, `Qno`, `QPscore`, `QPposition`) VALUES (1, 3, 5, 2);
INSERT INTO `question_paper`(`Pno`, `Qno`, `QPscore`, `QPposition`) VALUES (3, 2, 4, 1);

INSERT INTO `student_course`(`Cno`, `Sno`) VALUES (1, 'student1');
INSERT INTO `student_course`(`Cno`, `Sno`) VALUES (1, 'student1_en');
INSERT INTO `student_course`(`Cno`, `Sno`) VALUES (4, 'student2');
INSERT INTO `student_course`(`Cno`, `Sno`) VALUES (1, 'student3');
INSERT INTO `student_course`(`Cno`, `Sno`) VALUES (4, 'student3');
INSERT INTO `student_course`(`Cno`, `Sno`) VALUES (3, 'student4_en');

INSERT INTO `test`(`Tname`, `Tdesc`, `Tstart`, `Tend`, `Pno`, `Cno`) VALUES ('数据库期末考试', NULL, '2020-12-15 15:57:42', '2020-12-15 15:57:42', 2, 1);
INSERT INTO `test`(`Tname`, `Tdesc`, `Tstart`, `Tend`, `Pno`, `Cno`) VALUES ('流体力学期中考试', '考试说明测试','2020-12-18 15:00:00', '2020-12-19 15:00:00', 3, 4);

INSERT INTO `student_test`(`Tno`, `Sno`, `STgrade`) VALUES (1, 'student1', NULL);
INSERT INTO `student_test`(`Tno`, `Sno`, `STwrong`, `STblank`, `STgrade`) VALUES (1, 'student1_en', 0, 0, 95);
INSERT INTO `student_test`(`Tno`, `Sno`, `STwrong`, `STblank`, `STgrade`) VALUES (1, 'student3', 1, 1, 78);
INSERT INTO `student_test`(`Tno`, `Sno`, `STgrade`) VALUES (2, 'student2', NULL);
INSERT INTO `student_test`(`Tno`, `Sno`, `STgrade`) VALUES (2, 'student3', NULL);
