/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 80021
Source Host           : 127.0.0.1:3306
Source Database       : exam

Target Server Type    : MYSQL
Target Server Version : 80021
File Encoding         : 65001

Date: 2020-12-29 20:35:34
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for admin
-- ----------------------------
DROP TABLE IF EXISTS `admin`;
CREATE TABLE `admin` (
  `Ano` varchar(20) COLLATE utf8mb4_general_ci NOT NULL COMMENT '管理员账号',
  `Apassword` varchar(32) COLLATE utf8mb4_general_ci NOT NULL COMMENT '管理员密码',
  PRIMARY KEY (`Ano`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Table structure for course
-- ----------------------------
DROP TABLE IF EXISTS `course`;
CREATE TABLE `course` (
  `Cno` int NOT NULL AUTO_INCREMENT COMMENT '课程编号',
  `Cname` varchar(20) COLLATE utf8mb4_general_ci NOT NULL COMMENT '课程名称',
  `Subno` int DEFAULT NULL COMMENT '课程所属科目',
  `Mno` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '教授该课程教师号',
  PRIMARY KEY (`Cno`),
  KEY `Mno` (`Mno`),
  KEY `Subno` (`Subno`),
  CONSTRAINT `course_ibfk_1` FOREIGN KEY (`Mno`) REFERENCES `mentor` (`Mno`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `course_ibfk_2` FOREIGN KEY (`Subno`) REFERENCES `subject` (`Subno`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Table structure for mentor
-- ----------------------------
DROP TABLE IF EXISTS `mentor`;
CREATE TABLE `mentor` (
  `Mno` varchar(20) COLLATE utf8mb4_general_ci NOT NULL COMMENT '教师编号',
  `Mname` varchar(10) COLLATE utf8mb4_general_ci NOT NULL COMMENT '教师姓名',
  `Mgender` char(1) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '教师性别',
  `Mtitle` varchar(10) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '教师职称',
  `Mpassword` varchar(32) COLLATE utf8mb4_general_ci NOT NULL COMMENT '教师登陆密码',
  PRIMARY KEY (`Mno`),
  KEY `Mname` (`Mname`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Table structure for paper
-- ----------------------------
DROP TABLE IF EXISTS `paper`;
CREATE TABLE `paper` (
  `Pno` int NOT NULL AUTO_INCREMENT COMMENT '试卷的编号',
  `Pname` varchar(30) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '试卷名',
  `Subno` int DEFAULT NULL COMMENT '科目编号',
  `Pnum` int NOT NULL COMMENT '试卷包含的题目数量',
  `Pscore` int NOT NULL COMMENT '试卷总分',
  `Preference` int DEFAULT '0' COMMENT '试卷被引用的次数',
  `Pisdeleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '真：隐藏 假：显示',
  PRIMARY KEY (`Pno`),
  KEY `Subno` (`Subno`),
  KEY `Pname` (`Pname`),
  CONSTRAINT `paper_ibfk_1` FOREIGN KEY (`Subno`) REFERENCES `subject` (`Subno`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Table structure for question
-- ----------------------------
DROP TABLE IF EXISTS `question`;
CREATE TABLE `question` (
  `Qno` int NOT NULL AUTO_INCREMENT COMMENT '题库中的编号',
  `Qtype` enum('select','multi','fill') COLLATE utf8mb4_general_ci NOT NULL COMMENT '题目类型 select-单选 multi-多选 fill-填空',
  `Qstem` varchar(255) COLLATE utf8mb4_general_ci NOT NULL COMMENT '题目的内容',
  `Qanswer` varchar(255) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'JSON列表，题目的答案',
  `Qselect` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'JSON列表，选择题的备选项',
  `Subno` int DEFAULT NULL COMMENT '题目所属的科目',
  `Qreference` int unsigned NOT NULL DEFAULT '0' COMMENT '题目被引用的次数',
  `Qisdeleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '真：隐藏 假：显示',
  PRIMARY KEY (`Qno`),
  KEY `Subno` (`Subno`),
  KEY `Qquery` (`Qno`,`Qtype`,`Qstem`,`Qanswer`) USING BTREE,
  CONSTRAINT `question_ibfk_1` FOREIGN KEY (`Subno`) REFERENCES `subject` (`Subno`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Table structure for question_paper
-- ----------------------------
DROP TABLE IF EXISTS `question_paper`;
CREATE TABLE `question_paper` (
  `Pno` int NOT NULL COMMENT '题库中的编号',
  `Qno` int NOT NULL COMMENT '试卷的编号',
  `QPscore` int DEFAULT '0' COMMENT '试题的分值',
  PRIMARY KEY (`Pno`,`Qno`),
  KEY `Qno` (`Qno`),
  CONSTRAINT `question_paper_ibfk_1` FOREIGN KEY (`Pno`) REFERENCES `paper` (`Pno`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `question_paper_ibfk_2` FOREIGN KEY (`Qno`) REFERENCES `question` (`Qno`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Table structure for student
-- ----------------------------
DROP TABLE IF EXISTS `student`;
CREATE TABLE `student` (
  `Sno` varchar(20) COLLATE utf8mb4_general_ci NOT NULL COMMENT '学生编号',
  `Sname` varchar(10) COLLATE utf8mb4_general_ci NOT NULL COMMENT '学生姓名',
  `Sgender` enum('男','女') COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '学生性别',
  `Smajor` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '学生专业',
  `Spassword` varchar(32) COLLATE utf8mb4_general_ci NOT NULL COMMENT '学生登陆密码',
  PRIMARY KEY (`Sno`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Table structure for student_course
-- ----------------------------
DROP TABLE IF EXISTS `student_course`;
CREATE TABLE `student_course` (
  `Cno` int NOT NULL COMMENT '课程编号',
  `Sno` varchar(20) COLLATE utf8mb4_general_ci NOT NULL COMMENT '学生编号',
  PRIMARY KEY (`Cno`,`Sno`),
  KEY `student_course_ibfk_2` (`Sno`),
  CONSTRAINT `student_course_ibfk_1` FOREIGN KEY (`Cno`) REFERENCES `course` (`Cno`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `student_course_ibfk_2` FOREIGN KEY (`Sno`) REFERENCES `student` (`Sno`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Table structure for student_test
-- ----------------------------
DROP TABLE IF EXISTS `student_test`;
CREATE TABLE `student_test` (
  `Tno` int NOT NULL COMMENT '考试编号',
  `Sno` varchar(20) COLLATE utf8mb4_general_ci NOT NULL COMMENT '学生编号',
  `STwrong` int DEFAULT NULL COMMENT '错题数量',
  `STblank` int DEFAULT NULL COMMENT '未作答题数',
  `STgrade` int DEFAULT NULL COMMENT '学生考试成绩',
  PRIMARY KEY (`Tno`,`Sno`),
  KEY `Sno` (`Sno`),
  CONSTRAINT `student_test_ibfk_1` FOREIGN KEY (`Sno`) REFERENCES `student` (`Sno`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `student_test_ibfk_2` FOREIGN KEY (`Tno`) REFERENCES `test` (`Tno`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Table structure for subject
-- ----------------------------
DROP TABLE IF EXISTS `subject`;
CREATE TABLE `subject` (
  `Subno` int NOT NULL AUTO_INCREMENT COMMENT '科目编号',
  `Subname` varchar(25) COLLATE utf8mb4_general_ci NOT NULL COMMENT '科目名称',
  PRIMARY KEY (`Subno`),
  KEY `Subname` (`Subname`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Table structure for test
-- ----------------------------
DROP TABLE IF EXISTS `test`;
CREATE TABLE `test` (
  `Tno` int NOT NULL AUTO_INCREMENT COMMENT '考试的编号',
  `Tname` varchar(20) COLLATE utf8mb4_general_ci NOT NULL COMMENT '考试的名称',
  `Tdesc` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '考试说明',
  `Tstart` timestamp NOT NULL COMMENT '考试开始时间',
  `Tend` timestamp NULL DEFAULT NULL COMMENT '考试结束时间',
  `Pno` int NOT NULL COMMENT '引用的试卷编号',
  `Cno` int NOT NULL COMMENT '所属的课程编号',
  PRIMARY KEY (`Tno`),
  KEY `Pno` (`Pno`),
  KEY `Cno` (`Cno`),
  CONSTRAINT `test_ibfk_1` FOREIGN KEY (`Pno`) REFERENCES `paper` (`Pno`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `test_ibfk_2` FOREIGN KEY (`Cno`) REFERENCES `course` (`Cno`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Procedure structure for delete_paper
-- ----------------------------
DROP PROCEDURE IF EXISTS `delete_paper`;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `delete_paper`(IN target VARCHAR(20), OUT res BOOLEAN)
BEGIN
	DECLARE ref_count INT;
	SELECT Preference INTO ref_count FROM paper WHERE Pno = target;
	IF ref_count IS NULL THEN
		SET res = FALSE;
	ELSE
		IF ref_count > 0 THEN
			UPDATE paper SET Pisdeleted = TRUE WHERE Pno = target;
		ELSE
			DELETE FROM paper WHERE Pno = target;
		END IF;
		SET res = TRUE;
	END IF;
END
;;
DELIMITER ;

-- ----------------------------
-- Procedure structure for delete_question
-- ----------------------------
DROP PROCEDURE IF EXISTS `delete_question`;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `delete_question`(IN target VARCHAR(20), OUT res BOOLEAN)
BEGIN
	DECLARE ref_count INT;
	SELECT Qreference INTO ref_count FROM question WHERE Qno = target;
	IF ref_count IS NULL THEN
		SET res = FALSE;
	ELSE
		IF ref_count > 0 THEN
			UPDATE question SET Qisdeleted = TRUE WHERE Qno = target;
		ELSE
			DELETE FROM question WHERE Qno = target;
		END IF;
		SET res = TRUE;
	END IF;
END
;;
DELIMITER ;

-- ----------------------------
-- Procedure structure for update_question
-- ----------------------------
DROP PROCEDURE IF EXISTS `update_question`;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `update_question`(IN target VARCHAR(20), IN stem VARCHAR(255), IN answer VARCHAR(255),
	IN _select VARCHAR(255), IN subject VARCHAR(5), OUT res BOOLEAN)
BEGIN
	DECLARE ref_count INT;
	DECLARE type ENUM('select', 'multi', 'fill');

	SELECT Qreference INTO ref_count FROM question WHERE Qno = target;
	-- ref_count为NULL说明查不到此条记录
	IF ref_count IS NULL THEN
		SET res = FALSE;
	ELSE
		IF ref_count > 0 THEN
			-- 被引用了，隐藏原题创建一个新题
			SELECT Qtype INTO type FROM question WHERE Qno = target;
			UPDATE question SET Qisdeleted = TRUE WHERE Qno = target;
			INSERT INTO `question`(`Qtype`, `Qstem`, `Qanswer`, `Qselect`, `Subno`)
				VALUES (type, stem, answer, _select, subject);
		ELSE
			UPDATE question SET Qstem = stem, Qanswer = answer, Qselect = _select, Qsubject = subject
				WHERE Qno = target;
		END IF;
		SET res = TRUE;
	END IF;
END
;;
DELIMITER ;
DROP TRIGGER IF EXISTS `p_delete`;
DELIMITER ;;
CREATE TRIGGER `p_delete` BEFORE DELETE ON `paper` FOR EACH ROW BEGIN
	DELETE FROM question_paper WHERE Pno = OLD.Pno;
END
;;
DELIMITER ;
DROP TRIGGER IF EXISTS `qr_insert`;
DELIMITER ;;
CREATE TRIGGER `qr_insert` AFTER INSERT ON `question_paper` FOR EACH ROW BEGIN
	UPDATE question SET Qreference = Qreference + 1 WHERE question.Qno = NEW.Qno;
END
;;
DELIMITER ;
DROP TRIGGER IF EXISTS `qr_delete`;
DELIMITER ;;
CREATE TRIGGER `qr_delete` AFTER DELETE ON `question_paper` FOR EACH ROW BEGIN
	DECLARE ref_count INT;
	DECLARE hidden TINYINT(1);
	UPDATE question SET Qreference = Qreference - 1 WHERE question.Qno = OLD.Qno;
	SELECT Qreference, Qisdeleted INTO ref_count, hidden FROM question WHERE question.Qno = OLD.Qno;
	IF ref_count = 0 AND hidden = TRUE THEN
		DELETE FROM question WHERE question.Qno = OLD.Qno;
	END IF;
END
;;
DELIMITER ;
DROP TRIGGER IF EXISTS `t_insert`;
DELIMITER ;;
CREATE TRIGGER `t_insert` AFTER INSERT ON `test` FOR EACH ROW BEGIN
	UPDATE paper SET Preference = Preference + 1 WHERE paper.Pno = NEW.Pno;
END
;;
DELIMITER ;
DROP TRIGGER IF EXISTS `t_delete`;
DELIMITER ;;
CREATE TRIGGER `t_delete` AFTER DELETE ON `test` FOR EACH ROW BEGIN
	DECLARE ref_count INT;
	DECLARE hidden TINYINT(1);
	UPDATE paper SET Preference = Preference - 1 WHERE paper.Pno = OLD.Pno;
	SELECT Preference, Pisdeleted INTO ref_count, hidden FROM paper WHERE paper.Pno = OLD.Pno;
	IF ref_count = 0 AND hidden = TRUE THEN
		DELETE FROM paper WHERE paper.Pno = OLD.Pno;
	END IF;
END
;;
DELIMITER ;
