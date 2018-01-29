DELIMITER //

DROP FUNCTION IF EXISTS get_price_raise_limit_date //

/* 車室の契約状態を取得する */
CREATE FUNCTION get_price_raise_limit_date (
) 
RETURNS date
BEGIN

	DECLARE ret_value date;				/* 戻り値 */
    
    SELECT IF(
		date_format(current_date(), '%m%d') > '0331'
	  , str_to_date(concat(extract(year from current_date()) + 1, '0331'), '%Y%m%d')
      , str_to_date(concat(extract(year from current_date()), '0331'), '%Y%m%d')
	) INTO ret_value;
    
    RETURN ret_value;
 
END //

DELIMITER ;