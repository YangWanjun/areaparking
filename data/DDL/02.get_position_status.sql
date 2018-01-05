DELIMITER //

DROP FUNCTION IF EXISTS get_position_status //

/* 車室の契約状態を取得する */
CREATE FUNCTION get_position_status (
	in_position_id integer
) 
RETURNS char(2)
BEGIN

	DECLARE ret_value char(2);				/* 戻り値 */
    
    IF (SELECT COUNT(1) 
          FROM ap_contract 
		 WHERE parking_position_id = in_position_id 
           AND status = '11' 					/* 本契約 */
           -- AND start_date <= current_date()	/* 来月からの契約の場合があるので、開始日は除外する */
           AND end_date >= current_date()
           AND is_deleted = 0) > 0 THEN
		-- 契約済み 空無
        SET ret_value = '03';
	ELSEIF (SELECT COUNT(1)
              FROM ap_contract
			 WHERE parking_position_id = in_position_id
               AND status = '01'
               AND is_deleted = 0) > 0 THEN
		-- 仮契約中 手続中
		SET ret_value = '02';
	ELSE
		-- 空き
		SET ret_value = '01';
	END IF;
    
    RETURN ret_value;
 
END //

DELIMITER ;