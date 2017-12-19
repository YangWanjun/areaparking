DELIMITER //

DROP FUNCTION IF EXISTS get_process_percent //

/* 残業時間を取得する */
CREATE FUNCTION get_process_percent (
	in_process_id integer
) 
RETURNS DECIMAL(4, 1)
BEGIN

	DECLARE ret_value float;			/* 戻り値 */
    DECLARE total_task float; 	 			/* タスク数 */
    DECLARE finished_task float; 	 			/* 処理済みタスク数 */
    
    SELECT COUNT(1) into total_task FROM ap_task where process_id = in_process_id and is_deleted = 0;
    
    IF total_task > 0 THEN
		SELECT COUNT(1) into finished_task FROM ap_task where process_id = in_process_id and is_deleted = 0 and status in ('10', '99');
        SET ret_value = finished_task / total_task;
	ELSE
		SET ret_value = 0;
	END IF;
    
    RETURN ret_value * 100;
 
END //

DELIMITER ;