-- ----------------------------
-- 含有密码字段的表均加入了两种记录：未加密版本和MD5加密版本
-- 且密码均为123456
-- 用于支持系统开发的不同阶段的测试工作
-- ----------------------------
INSERT INTO `admin`(`Ano`, `Apassword`) VALUES ('admin1', 'e10adc3949ba59abbe56e057f20f883e');
INSERT INTO `admin`(`Ano`, `Apassword`) VALUES ('admin2', 'e10adc3949ba59abbe56e057f20f883e');

INSERT INTO `mentor`(`Mno`, `Mname`, `Mgender`, `Mtitle`, `Mpassword`) VALUES ('76543210', '张三', '男', '副教授', 'e10adc3949ba59abbe56e057f20f883e');
INSERT INTO `mentor`(`Mno`, `Mname`, `Mgender`, `Mtitle`, `Mpassword`) VALUES ('76558523', '李四', '女', '教授', 'e10adc3949ba59abbe56e057f20f883e');
INSERT INTO `mentor`(`Mno`, `Mname`, `Mgender`, `Mtitle`, `Mpassword`) VALUES ('75662223', 'Peter', '男', '讲师', 'e10adc3949ba59abbe56e057f20f883e');

INSERT INTO `student`(`Sno`, `Sname`, `Sgender`, `Smajor`, `Spassword`) VALUES ('120181080223', '李明', '男', '软件工程', 'e10adc3949ba59abbe56e057f20f883e');
INSERT INTO `student`(`Sno`, `Sname`, `Sgender`, `Smajor`, `Spassword`) VALUES ('120181080102', 'Mary', '女', '信息安全', 'e10adc3949ba59abbe56e057f20f883e');
INSERT INTO `student`(`Sno`, `Sname`, `Sgender`, `Smajor`, `Spassword`) VALUES ('120181080116', '王丽', '女', '软件工程', 'e10adc3949ba59abbe56e057f20f883e');
INSERT INTO `student`(`Sno`, `Sname`, `Sgender`, `Smajor`, `Spassword`) VALUES ('120181110111', 'Антон', '男', '核工程', 'e10adc3949ba59abbe56e057f20f883e');

INSERT INTO `subject`(`Subname`) VALUES ('软件工程');
INSERT INTO `subject`(`Subname`) VALUES ('数据库原理');
INSERT INTO `subject`(`Subname`) VALUES ('编译原理');
INSERT INTO `subject`(`Subname`) VALUES ('流体力学');
INSERT INTO `subject`(`Subname`) VALUES ('工程热力学');
INSERT INTO `subject`(`Subname`) VALUES ('C语言程序设计');
INSERT INTO `subject`(`Subname`) VALUES ('Java高级语言程序设计');

INSERT INTO `course`(`Cname`, `Subno`, `Mno`) VALUES ('数据库教学班1', 2, '76543210');
INSERT INTO `course`(`Cname`, `Subno`, `Mno`) VALUES ('数据库教学班2', 2, '76543210');
INSERT INTO `course`(`Cname`, `Subno`, `Mno`) VALUES ('编译原理教学班1', 3, '76543210');
INSERT INTO `course`(`Cname`, `Subno`, `Mno`) VALUES ('Java教学班1', 7, '76543210');
INSERT INTO `course`(`Cname`, `Subno`, `Mno`) VALUES ('流体力学教学班', 4, '76543210');
INSERT INTO `course`(`Cname`, `Subno`, `Mno`) VALUES ('工程热力学教学班', 5, '75662223');

INSERT INTO `question`(`Qtype`, `Qstem`, `Qanswer`, `Qselect`, `Subno`, `Qreference`, `Qisdeleted`) VALUES ('fill', '这是一道[填空]编译原理填空1[填空]', '[\"正确答案1\", \"正确答案2\"]', NULL, 3, 0, 0);
INSERT INTO `question`(`Qtype`, `Qstem`, `Qanswer`, `Qselect`, `Subno`, `Qreference`, `Qisdeleted`) VALUES ('fill', '这是一道[填空]编译原理填空2[填空]', '[\"正确答案1\", \"正确答案2\"]', NULL, 3, 0, 0);
INSERT INTO `question`(`Qtype`, `Qstem`, `Qanswer`, `Qselect`, `Subno`, `Qreference`, `Qisdeleted`) VALUES ('fill', '这是一道[填空]编译原理填空3[填空]', '[\"正确答案1\", \"正确答案2\"]', NULL, 3, 0, 0);
INSERT INTO `question`(`Qtype`, `Qstem`, `Qanswer`, `Qselect`, `Subno`, `Qreference`, `Qisdeleted`) VALUES ('fill', '这是一道[填空]编译原理填空4[填空]', '[\"正确答案1\", \"正确答案2\"]', NULL, 3, 0, 0);
INSERT INTO `question`(`Qtype`, `Qstem`, `Qanswer`, `Qselect`, `Subno`, `Qreference`, `Qisdeleted`) VALUES ('fill', '这是一道[填空]编译原理填空6[填空]', '[\"正确答案1\", \"正确答案2\"]', NULL, 3, 0, 0);
INSERT INTO `question`(`Qtype`, `Qstem`, `Qanswer`, `Qselect`, `Subno`, `Qreference`, `Qisdeleted`) VALUES ('fill', '这是一道[填空]编译原理填空7[填空]', '[\"正确答案1\", \"正确答案2\"]', NULL, 3, 0, 0);
INSERT INTO `question`(`Qtype`, `Qstem`, `Qanswer`, `Qselect`, `Subno`, `Qreference`, `Qisdeleted`) VALUES ('multi', '这是一道流体力学多选题1(   )', '[\"我是A\", \"我是B\", \"我是C\", \"我是D\", \"我是E\"]', '[\"A\", \"C\", \"E\"]', 4, 0, 0);
INSERT INTO `question`(`Qtype`, `Qstem`, `Qanswer`, `Qselect`, `Subno`, `Qreference`, `Qisdeleted`) VALUES ('multi', '这是一道流体力学多选题2(   )', '[\"我是A\", \"我是B\", \"我是C\", \"我是D\", \"我是E\"]', '[\"A\", \"C\", \"E\"]', 4, 0, 0);
INSERT INTO `question`(`Qtype`, `Qstem`, `Qanswer`, `Qselect`, `Subno`, `Qreference`, `Qisdeleted`) VALUES ('multi', '这是一道流体力学多选题3(   )', '[\"我是A\", \"我是B\", \"我是C\", \"我是D\", \"我是E\"]', '[\"A\", \"C\", \"E\"]', 4, 0, 0);
INSERT INTO `question`(`Qtype`, `Qstem`, `Qanswer`, `Qselect`, `Subno`, `Qreference`, `Qisdeleted`) VALUES ('multi', '这是一道流体力学多选题4(   )', '[\"我是A\", \"我是B\", \"我是C\", \"我是D\", \"我是E\"]', '[\"A\", \"C\", \"E\"]', 4, 0, 0);
INSERT INTO `question`(`Qtype`, `Qstem`, `Qanswer`, `Qselect`, `Subno`, `Qreference`, `Qisdeleted`) VALUES ('select', '根据应用需求建立索引是在下列哪个阶段完成1(    )。', '[\"数据库概念结构设计\", \"数据库逻辑结构设计\", \"数据库物理设计\", \"数据库实施与维护\"]', '[\"A\"]', 2, 0, 0);
INSERT INTO `question`(`Qtype`, `Qstem`, `Qanswer`, `Qselect`, `Subno`, `Qreference`, `Qisdeleted`) VALUES ('select', '以下哪一条属于关系数据库的规范化理论要解决的问题?1(   )。', '[\"如何构造合适的数据库逻辑结构\", \"如果构造合适的数据库物理结构\", \"如何构造合适的应用程序界面\", \"如何控制不同用户的数据操作权限\"]', '[\"A\"]', 2, 0, 0);
INSERT INTO `question`(`Qtype`, `Qstem`, `Qanswer`, `Qselect`, `Subno`, `Qreference`, `Qisdeleted`) VALUES ('select', '以下哪一条属于关系数据库的规范化理论要解决的问题?1(   )。', '[\"如何构造合适的数据库逻辑结构\", \"如果构造合适的数据库物理结构\", \"如何构造合适的应用程序界面\", \"如何控制不同用户的数据操作权限\"]', '[\"A\"]', 2, 0, 0);
INSERT INTO `question`(`Qtype`, `Qstem`, `Qanswer`, `Qselect`, `Subno`, `Qreference`, `Qisdeleted`) VALUES ('select', '以下哪一条属于关系数据库的规范化理论要解决的问题?1(   )。', '[\"如何构造合适的数据库逻辑结构\", \"如果构造合适的数据库物理结构\", \"如何构造合适的应用程序界面\", \"如何控制不同用户的数据操作权限\"]', '[\"A\"]', 2, 0, 0);
INSERT INTO `question`(`Qtype`, `Qstem`, `Qanswer`, `Qselect`, `Subno`, `Qreference`, `Qisdeleted`) VALUES ('select', '以下哪一条属于关系数据库的规范化理论要解决的问题?1(   )。', '[\"如何构造合适的数据库逻辑结构\", \"如果构造合适的数据库物理结构\", \"如何构造合适的应用程序界面\", \"如何控制不同用户的数据操作权限\"]', '[\"A\"]', 2, 0, 0);
INSERT INTO `question`(`Qtype`, `Qstem`, `Qanswer`, `Qselect`, `Subno`, `Qreference`, `Qisdeleted`) VALUES ('select', '根据应用需求建立索引是在下列哪个阶段完成2(    )。', '[\"数据库概念结构设计\", \"数据库逻辑结构设计\", \"数据库物理设计\", \"数据库实施与维护\"]', '[\"A\"]', 2, 0, 0);
INSERT INTO `question`(`Qtype`, `Qstem`, `Qanswer`, `Qselect`, `Subno`, `Qreference`, `Qisdeleted`) VALUES ('select', '根据应用需求建立索引是在下列哪个阶段完成3(    )。', '[\"数据库概念结构设计\", \"数据库逻辑结构设计\", \"数据库物理设计\", \"数据库实施与维护\"]', '[\"A\"]', 2, 0, 0);
INSERT INTO `question`(`Qtype`, `Qstem`, `Qanswer`, `Qselect`, `Subno`, `Qreference`, `Qisdeleted`) VALUES ('select', '根据应用需求建立索引是在下列哪个阶段完成4(    )。', '[\"数据库概念结构设计\", \"数据库逻辑结构设计\", \"数据库物理设计\", \"数据库实施与维护\"]', '[\"A\"]', 2, 0, 0);
INSERT INTO `question`(`Qtype`, `Qstem`, `Qanswer`, `Qselect`, `Subno`, `Qreference`, `Qisdeleted`) VALUES ('select', '以下哪一条属于关系数据库的规范化理论要解决的问题?5(   )。', '[\"如何构造合适的数据库逻辑结构\", \"如果构造合适的数据库物理结构\", \"如何构造合适的应用程序界面\", \"如何控制不同用户的数据操作权限\"]', '[\"A\"]', 2, 0, 0);

INSERT INTO `paper`(`Pname`, `Subno`, `Pnum`, `Pscore`, `Preference`, `Pisdeleted`) VALUES ('数据库基础卷', 2, 10, 100, 0, 0);
INSERT INTO `paper`(`Pname`, `Subno`, `Pnum`, `Pscore`, `Preference`, `Pisdeleted`) VALUES ('数据库提高卷', 2, 1, 100, 0, 0);
INSERT INTO `paper`(`Pname`, `Subno`, `Pnum`, `Pscore`, `Preference`, `Pisdeleted`) VALUES ('流体力学基础卷', 4, 5, 100, 0, 0);
INSERT INTO `paper`(`Pname`, `Subno`, `Pnum`, `Pscore`, `Preference`, `Pisdeleted`) VALUES ('软件工程提高卷', 1, 1, 100, 0, 0);

INSERT INTO `question_paper`(`Pno`, `Qno`, `QPscore`) VALUES (1, 11, 10);
INSERT INTO `question_paper`(`Pno`, `Qno`, `QPscore`) VALUES (1, 12, 10);
INSERT INTO `question_paper`(`Pno`, `Qno`, `QPscore`) VALUES (1, 13, 10);
INSERT INTO `question_paper`(`Pno`, `Qno`, `QPscore`) VALUES (1, 6, 10);
INSERT INTO `question_paper`(`Pno`, `Qno`, `QPscore`) VALUES (1, 9, 10);
INSERT INTO `question_paper`(`Pno`, `Qno`, `QPscore`) VALUES (1, 3, 10);
INSERT INTO `question_paper`(`Pno`, `Qno`, `QPscore`) VALUES (1, 19, 10);
INSERT INTO `question_paper`(`Pno`, `Qno`, `QPscore`) VALUES (1, 7, 10);
INSERT INTO `question_paper`(`Pno`, `Qno`, `QPscore`) VALUES (1, 18, 10);
INSERT INTO `question_paper`(`Pno`, `Qno`, `QPscore`) VALUES (1, 5, 10);
INSERT INTO `question_paper`(`Pno`, `Qno`, `QPscore`) VALUES (3, 13, 20);
INSERT INTO `question_paper`(`Pno`, `Qno`, `QPscore`) VALUES (3, 11, 20);
INSERT INTO `question_paper`(`Pno`, `Qno`, `QPscore`) VALUES (3, 12, 20);
INSERT INTO `question_paper`(`Pno`, `Qno`, `QPscore`) VALUES (3, 10, 20);
INSERT INTO `question_paper`(`Pno`, `Qno`, `QPscore`) VALUES (3, 6, 20);
INSERT INTO `question_paper`(`Pno`, `Qno`, `QPscore`) VALUES (4, 11, 100);
INSERT INTO `question_paper`(`Pno`, `Qno`, `QPscore`) VALUES (2, 13, 100);

INSERT INTO `student_course`(`Cno`, `Sno`) VALUES (1, '120181080102');
INSERT INTO `student_course`(`Cno`, `Sno`) VALUES (1, '120181080116');
INSERT INTO `student_course`(`Cno`, `Sno`) VALUES (1, '120181080223');
INSERT INTO `student_course`(`Cno`, `Sno`) VALUES (1, '120181110111');
INSERT INTO `student_course`(`Cno`, `Sno`) VALUES (2, '120181080116');
INSERT INTO `student_course`(`Cno`, `Sno`) VALUES (5, '120181080116');
INSERT INTO `student_course`(`Cno`, `Sno`) VALUES (5, '120181110111');

INSERT INTO `test`(`Tname`, `Tdesc`, `Tstart`, `Tend`, `Pno`, `Cno`) VALUES ('数据库期末考试', NULL, '2020-12-15 15:57:42', '2020-12-15 15:57:42', 1, 1);
INSERT INTO `test`(`Tname`, `Tdesc`, `Tstart`, `Tend`, `Pno`, `Cno`) VALUES ('流体力学期中考试', '考试说明测试', '2020-12-18 15:00:00', '2020-12-19 15:00:00', 3, 1);

INSERT INTO `student_test`(`Tno`, `Sno`, `STwrong`, `STblank`, `STgrade`) VALUES (1, '120181080102', 0, 0, 100);
INSERT INTO `student_test`(`Tno`, `Sno`) VALUES (1, '120181080116');
INSERT INTO `student_test`(`Tno`, `Sno`, `STwrong`, `STblank`, `STgrade`) VALUES (1, '120181080223', 2, 3, 80);
INSERT INTO `student_test`(`Tno`, `Sno`) VALUES (1, '120181110111');
INSERT INTO `student_test`(`Tno`, `Sno`, `STwrong`, `STblank`, `STgrade`) VALUES (2, '120181080102', 1, 0, 95);
INSERT INTO `student_test`(`Tno`, `Sno`, `STwrong`, `STblank`, `STgrade`) VALUES (2, '120181080116', 2, 3, 80);
INSERT INTO `student_test`(`Tno`, `Sno`) VALUES (2, '120181080223');
INSERT INTO `student_test`(`Tno`, `Sno`) VALUES (2, '120181110111');
