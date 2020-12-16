DELIMITER $
CREATE TRIGGER qr_delete AFTER DELETE ON question_paper
FOR EACH ROW
BEGIN
	DECLARE ref_count INT;
	DECLARE hidden TINYINT(1);
	UPDATE question SET Qreference = Qreference - 1 WHERE question.Qno = OLD.Qno;
	SELECT Qreference, Qisdeleted INTO ref_count, hidden FROM question WHERE question.Qno = OLD.Qno;
	IF ref_count = 0 AND hidden = TRUE THEN
		DELETE FROM question WHERE question.Qno = OLD.Qno;
	END IF;
END;$

CREATE TRIGGER qr_insert AFTER INSERT ON question_paper
FOR EACH ROW
BEGIN
	UPDATE question SET Qreference = Qreference + 1 WHERE question.Qno = NEW.Qno;
END;$

-- 由于级联删除并不会激活触发器
-- 所以通过paper上触发器间接触发
CREATE TRIGGER p_delete BEFORE DELETE ON paper
FOR EACH ROW
BEGIN
	DELETE FROM question_paper WHERE Pno = OLD.Pno;
END;$

CREATE TRIGGER t_delete AFTER DELETE ON test
FOR EACH ROW
BEGIN
	DECLARE ref_count INT;
	DECLARE hidden TINYINT(1);
	UPDATE paper SET Preference = Preference - 1 WHERE paper.Pno = OLD.Pno;
	SELECT Preference, Pisdeleted INTO ref_count, hidden FROM paper WHERE paper.Pno = OLD.Pno;
	IF ref_count = 0 AND hidden = TRUE THEN
		DELETE FROM paper WHERE paper.Pno = OLD.Pno;
	END IF;
END;$

CREATE TRIGGER t_insert AFTER INSERT ON test
FOR EACH ROW
BEGIN
	UPDATE paper SET Preference = Preference + 1 WHERE paper.Pno = NEW.Pno;
END;$

DELIMITER ;
