/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 80021
Source Host           : 127.0.0.1:3306
Source Database       : exam

Target Server Type    : MYSQL
Target Server Version : 80021
File Encoding         : 65001

Date: 2020-12-15 10:59:31
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for admin
-- ----------------------------
DROP TABLE IF EXISTS `admin`;
CREATE TABLE `admin` (
  `Ano` varchar(20) NOT NULL COMMENT '管理员账号',
  `Apassword` varchar(32) NOT NULL COMMENT '管理员密码',
  PRIMARY KEY (`Ano`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_general_ci;

-- ----------------------------
-- Table structure for course
-- ----------------------------
DROP TABLE IF EXISTS `course`;
CREATE TABLE `course` (
  `Cno` varchar(20) NOT NULL COMMENT '课程编号',
  `Cname` varchar(20) NOT NULL COMMENT '课程名称',
  `Subno` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '课程所属科目',
  `Mno` varchar(20) DEFAULT NULL COMMENT '教授该课程教师号',
  PRIMARY KEY (`Cno`),
  KEY `Mno` (`Mno`),
  KEY `Subno` (`Subno`),
  CONSTRAINT `course_ibfk_1` FOREIGN KEY (`Mno`) REFERENCES `mentor` (`Mno`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `course_ibfk_2` FOREIGN KEY (`Subno`) REFERENCES `subject` (`Subno`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_general_ci;

-- ----------------------------
-- Table structure for mentor
-- ----------------------------
DROP TABLE IF EXISTS `mentor`;
CREATE TABLE `mentor` (
  `Mno` varchar(20) NOT NULL COMMENT '教师编号',
  `Mname` varchar(10) NOT NULL COMMENT '教师姓名',
  `Mgender` varchar(3) DEFAULT NULL COMMENT '教师性别',
  `Mtitle` varchar(10) DEFAULT NULL COMMENT '教师职称',
  `Mpassword` varchar(32) NOT NULL COMMENT '教师登陆密码',
  PRIMARY KEY (`Mno`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_general_ci;

-- ----------------------------
-- Table structure for paper
-- ----------------------------
DROP TABLE IF EXISTS `paper`;
CREATE TABLE `paper` (
  `Pno` varchar(20) NOT NULL COMMENT '试卷的编号',
  `Pname` varchar(30) DEFAULT NULL COMMENT '试卷名',
  `Subno` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '科目编号',
  `Preference` int DEFAULT '0' COMMENT '试卷被引用的次数',
  `Pisdeleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '真：隐藏 假：显示',
  PRIMARY KEY (`Pno`),
  KEY `Subno` (`Subno`),
  CONSTRAINT `paper_ibfk_1` FOREIGN KEY (`Subno`) REFERENCES `subject` (`Subno`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_general_ci;

-- ----------------------------
-- Table structure for question
-- ----------------------------
DROP TABLE IF EXISTS `question`;
CREATE TABLE `question` (
  `Qno` varchar(20) NOT NULL COMMENT '题库中的编号',
  `Qtype` enum('select', 'multi', 'fill') NOT NULL COMMENT '题目类型 select-单选 multi-多选 fill-填空',
  `Qstem` varchar(255) NOT NULL COMMENT '题目的内容',
  `Qanswer` varchar(255) NOT NULL COMMENT 'JSON格式的题目的答案，选择题的备选项，填空题的答案',
  `Qselect` varchar(10) DEFAULT NULL COMMENT '选择题的正确选项',
  `Subno` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '题目所属的科目',
  `Qreference` int unsigned NOT NULL DEFAULT '0' COMMENT '题目被引用的次数',
  `Qisdeleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '真：隐藏 假：显示',
  PRIMARY KEY (`Qno`),
  KEY `Subno` (`Subno`),
  CONSTRAINT `question_ibfk_1` FOREIGN KEY (`Subno`) REFERENCES `subject` (`Subno`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_general_ci;

-- ----------------------------
-- Table structure for question_paper
-- ----------------------------
DROP TABLE IF EXISTS `question_paper`;
CREATE TABLE `question_paper` (
  `Pno` varchar(20) NOT NULL COMMENT '题库中的编号',
  `Qno` varchar(20) NOT NULL COMMENT '试卷的编号',
  `QPscore` int DEFAULT '0' COMMENT '试题的分值',
  `QPposition` int DEFAULT NULL COMMENT '题目在试卷中的位置',
  PRIMARY KEY (`Pno`,`Qno`),
  KEY `Qno` (`Qno`),
  CONSTRAINT `question_paper_ibfk_1` FOREIGN KEY (`Pno`) REFERENCES `paper` (`Pno`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `question_paper_ibfk_2` FOREIGN KEY (`Qno`) REFERENCES `question` (`Qno`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_general_ci;

-- ----------------------------
-- Table structure for student
-- ----------------------------
DROP TABLE IF EXISTS `student`;
CREATE TABLE `student` (
  `Sno` varchar(20) NOT NULL COMMENT '学生编号',
  `Sname` varchar(10) NOT NULL COMMENT '学生姓名',
  `Sgender` enum('男','女') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '学生性别',
  `Smajor` varchar(20) DEFAULT NULL COMMENT '学生专业',
  `Spassword` varchar(32) NOT NULL COMMENT '学生登陆密码',
  PRIMARY KEY (`Sno`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_general_ci;

-- ----------------------------
-- Table structure for student_course
-- ----------------------------
DROP TABLE IF EXISTS `student_course`;
CREATE TABLE `student_course` (
  `Cno` varchar(20) NOT NULL COMMENT '课程编号',
  `Sno` varchar(20) NOT NULL COMMENT '学生编号',
  PRIMARY KEY (`Cno`,`Sno`),
  KEY `student_course_ibfk_2` (`Sno`),
  CONSTRAINT `student_course_ibfk_1` FOREIGN KEY (`Cno`) REFERENCES `course` (`Cno`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `student_course_ibfk_2` FOREIGN KEY (`Sno`) REFERENCES `student` (`Sno`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_general_ci;

-- ----------------------------
-- Table structure for student_test
-- ----------------------------
DROP TABLE IF EXISTS `student_test`;
CREATE TABLE `student_test` (
  `Tno` varchar(20) NOT NULL COMMENT '考试编号',
  `Sno` varchar(20) NOT NULL COMMENT '学生编号',
  `STgrade` int DEFAULT NULL COMMENT '学生考试成绩',
  PRIMARY KEY (`Tno`,`Sno`),
  KEY `Sno` (`Sno`),
  CONSTRAINT `student_test_ibfk_1` FOREIGN KEY (`Tno`) REFERENCES `test` (`Tno`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `student_test_ibfk_2` FOREIGN KEY (`Sno`) REFERENCES `student` (`Sno`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_general_ci;

-- ----------------------------
-- Table structure for subject
-- ----------------------------
DROP TABLE IF EXISTS `subject`;
CREATE TABLE `subject` (
  `Subno` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '科目编号',
  `Subname` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '科目名称',
  PRIMARY KEY (`Subno`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_general_ci;

-- ----------------------------
-- Table structure for test
-- ----------------------------
DROP TABLE IF EXISTS `test`;
CREATE TABLE `test` (
  `Tno` char(20) NOT NULL COMMENT '考试的编号',
  `Tname` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '考试的名称',
  `Tstart` timestamp NOT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '考试开始时间',
  `Tend` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '考试结束时间',
  `Pno` varchar(20) NOT NULL COMMENT '引用的试卷编号',
  `Cno` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '所属的课程编号',
  PRIMARY KEY (`Tno`),
  KEY `Pno` (`Pno`),
  KEY `Cno` (`Cno`),
  CONSTRAINT `test_ibfk_1` FOREIGN KEY (`Pno`) REFERENCES `paper` (`Pno`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `test_ibfk_2` FOREIGN KEY (`Cno`) REFERENCES `course` (`Cno`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_general_ci;
