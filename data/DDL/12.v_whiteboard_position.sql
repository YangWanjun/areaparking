CREATE OR REPLACE VIEW v_whiteboard_position AS
select pos.id
     , lot.code as whiteboard_id
     /* 車室情報 */
     , pos.id as parking_position_id
     , CONCAT(lot.pref_name, lot.city_name, ifnull(lot.town_name, ''), ifnull(lot.aza_name, ''), ifnull(lot.other_name, '')) as address
     , CASE
           WHEN c.id is not null THEN '03' 		-- 空き無
           WHEN tc.id is not null THEN '02'     -- 手続き中
           ELSE '01'							-- 空き
       END as position_status
	 , c.end_date as contract_end_date			-- 契約終了日
     /* 賃料 */
     , pos.price_recruitment
     , pos.price_recruitment_no_tax
     , pos.price_homepage
     , pos.price_homepage_no_tax
     , pos.price_handbill
     , pos.price_handbill_no_tax
     /* サイズ */
     , pos.length
     , pos.width
     , pos.height
     , pos.weight
     , pos.tyre_width
     , pos.tyre_width_ap
     , pos.min_height
     , pos.min_height_ap
     , pos.f_value
     , pos.r_value
     , pos.comment as position_comment          -- 車室の備考
  from ap_parking_lot lot
  join ap_parking_position pos on pos.parking_lot_id = lot.code
  left join ap_contract c on c.parking_position_id = pos.id
                         and c.status = '11' 	-- 本契約
                         and c.start_date <= current_date()
                         and c.end_date >= current_date()
                         and c.is_deleted = 0
  left join ap_contract tc on tc.parking_position_id = pos.id
                          and tc.is_deleted = 0
                          and tc.status = '01' 	-- 仮契約
 where lot.is_deleted = 0
   and pos.is_deleted = 0
