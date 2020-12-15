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

INSERT INTO `subject`(`Subno`, `Subname`) VALUES ('s0001', '软件工程');
INSERT INTO `subject`(`Subno`, `Subname`) VALUES ('s0002', '数据库原理');
INSERT INTO `subject`(`Subno`, `Subname`) VALUES ('s0003', '编译原理');
INSERT INTO `subject`(`Subno`, `Subname`) VALUES ('s0004', '流体力学');
INSERT INTO `subject`(`Subno`, `Subname`) VALUES ('s0005', '工程热力学');
INSERT INTO `subject`(`Subno`, `Subname`) VALUES ('s0006', 'C语言程序设计');
INSERT INTO `subject`(`Subno`, `Subname`) VALUES ('s0007', 'Java高级语言程序设计');

INSERT INTO `course`(`Cno`, `Cname`, `Subno`, `Mno`) VALUES ('c0001', '数据库教学班1', 's0002', 'teacher1');
INSERT INTO `course`(`Cno`, `Cname`, `Subno`, `Mno`) VALUES ('c0002', '数据库教学班2', 's0002', 'teacher1');
INSERT INTO `course`(`Cno`, `Cname`, `Subno`, `Mno`) VALUES ('c0003', '数据库教学班3', 's0002', 'teacher1_en');
INSERT INTO `course`(`Cno`, `Cname`, `Subno`, `Mno`) VALUES ('c0004', '流体力学1', 's0004', 'teacher2');
INSERT INTO `course`(`Cno`, `Cname`, `Subno`, `Mno`) VALUES ('c0005', '流体力学2', 's0004', 'teacher2_en');

INSERT INTO `paper`(`Pno`, `Pname`, `Preference`, `Pisdeleted`, `Subno`) VALUES ('p0001', '数据库基础卷', 0, 0, 's0002');
INSERT INTO `paper`(`Pno`, `Pname`, `Preference`, `Pisdeleted`, `Subno`) VALUES ('p0002', '数据库提高卷', 0, 0, 's0002');
INSERT INTO `paper`(`Pno`, `Pname`, `Preference`, `Pisdeleted`, `Subno`) VALUES ('p0003', '流体力学基础卷', 0, 1, 's0004');
INSERT INTO `paper`(`Pno`, `Pname`, `Preference`, `Pisdeleted`, `Subno`) VALUES ('p0004', '软件工程提高卷', 0, 0, 's0001');

INSERT INTO `question`(`Qno`, `Qtype`, `Qstem`, `Qanswer`, `Qselect`, `Subno`, `Qreference`, `Qisdeleted`) VALUES ('q00001', 'select', '这是一道数据库单选题()', '{\"A\": \"我是A\", \"B\": \"我是B\", \"C\": \"我是C\". \"D\": \"我是D\"}', 'A', 's0002', 0, 1);
INSERT INTO `question`(`Qno`, `Qtype`, `Qstem`, `Qanswer`, `Qselect`, `Subno`, `Qreference`, `Qisdeleted`) VALUES ('q00002', 'multi', '这是一道流体力学多选题()', '{\"A\": \"我是A\", \"B\": \"我是B\", \"C\": \"我是C\". \"D\": \"我是D\", \"E\": \"我是E\"}', 'ABC', 's0001', 0, 0);
INSERT INTO `question`(`Qno`, `Qtype`, `Qstem`, `Qanswer`, `Qselect`, `Subno`, `Qreference`, `Qisdeleted`) VALUES ('q00003', 'fill', '这是一道[填空]填空[填空]', '{\"A\": \"编译原理\", \"B\": \"题\"}', NULL, 's0003', 0, 0);

INSERT INTO `question_paper`(`Pno`, `Qno`, `QPscore`, `QPposition`) VALUES ('p0001', 'q00001', 2, 1);
INSERT INTO `question_paper`(`Pno`, `Qno`, `QPscore`, `QPposition`) VALUES ('p0001', 'q00002', 10, 3);
INSERT INTO `question_paper`(`Pno`, `Qno`, `QPscore`, `QPposition`) VALUES ('p0001', 'q00003', 5, 2);
INSERT INTO `question_paper`(`Pno`, `Qno`, `QPscore`, `QPposition`) VALUES ('p0003', 'q00002', 4, 1);

INSERT INTO `student_course`(`Cno`, `Sno`) VALUES ('c0001', 'student1');
INSERT INTO `student_course`(`Cno`, `Sno`) VALUES ('c0001', 'student1_en');
INSERT INTO `student_course`(`Cno`, `Sno`) VALUES ('c0004', 'student2');
INSERT INTO `student_course`(`Cno`, `Sno`) VALUES ('c0001', 'student3');
INSERT INTO `student_course`(`Cno`, `Sno`) VALUES ('c0004', 'student3');
INSERT INTO `student_course`(`Cno`, `Sno`) VALUES ('c0003', 'student4_en');

INSERT INTO `test`(`Tno`, `Tname`, `Tstart`, `Tend`, `Pno`, `Cno`) VALUES ('t0001', '数据库期末考试', '2020-12-15 15:57:42', '2020-12-15 15:57:42', 'p0002', 'c0001');
INSERT INTO `test`(`Tno`, `Tname`, `Tstart`, `Tend`, `Pno`, `Cno`) VALUES ('t0003', '流体力学期中考试', '2020-12-18 15:00:00', '2020-12-19 15:00:00', 'p0003', 'c0004');

INSERT INTO `student_test`(`Tno`, `Sno`, `STgrade`) VALUES ('t0001', 'student1', NULL);
INSERT INTO `student_test`(`Tno`, `Sno`, `STgrade`) VALUES ('t0001', 'student1_en', 95);
INSERT INTO `student_test`(`Tno`, `Sno`, `STgrade`) VALUES ('t0001', 'student3', 78);
INSERT INTO `student_test`(`Tno`, `Sno`, `STgrade`) VALUES ('t0003', 'student2', NULL);
INSERT INTO `student_test`(`Tno`, `Sno`, `STgrade`) VALUES ('t0003', 'student3', NULL);
