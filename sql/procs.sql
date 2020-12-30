DELIMITER $
/*
 * 存储过程：删除试题，根据是否被引用选择直接删除还是隐藏
 * 输入：target 待删除的试题号
 * 输出：res 若待删除的试题号不存在，返回FALSE，否则返回TRUE
 * ### MySQL中BOOLEAN对应TINYINT(1)
 */
CREATE PROCEDURE delete_question(IN target INTEGER , OUT res BOOLEAN)
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
END;$

/*
 * 存储过程：修改试题，根据是否被引用选择直接修改还是隐藏原题后插入新题
 * 输入：target  待删除的试题号
		 stem    题干
		 answer  题目答案
		 _select 选择题备选项，填空题此字段为NULL
		 subject 题目所属科目
   ### 虽然有可能某些字段并未被修改，但也需要完整地传进来
 * 输出：res 若待更新的试题号不存在，返回FALSE，否则返回TRUE
 * ### MySQL中BOOLEAN对应TINYINT(1)
 */
CREATE PROCEDURE update_question(IN target INTEGER, IN stem VARCHAR(255), IN answer VARCHAR(255),
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
END;$

/*
 * 存储过程：删除试卷，根据是否被引用选择直接删除还是隐藏
 * 输入：target 待删除的试卷号
 * 输出：res 若待删除的试卷号不存在，返回FALSE，否则返回TRUE
 * ### MySQL中BOOLEAN对应TINYINT(1)
 */
CREATE PROCEDURE delete_paper(IN target INTEGER, OUT res BOOLEAN)
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
END;$
DELIMITER ;
