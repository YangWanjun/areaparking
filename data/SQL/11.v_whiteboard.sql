CREATE OR REPLACE VIEW v_whiteboard AS
select pos.id as id
     , lot.code as parking_code
     , lot.code as parking_lot_id
     , lot.name as parking_lot_name
     , lot.staff_id
     , lot.category_id
     , CONCAT(lot.pref_name, lot.city_name, ifnull(lot.town_name, ''), ifnull(lot.aza_name, ''), ifnull(lot.other_name, '')) as address
     , lot.lng
     , lot.lat
     , 0 as position_count
     , 0 as waiting_count
     , plm.is_existed_contractor_allowed        -- 既契約者
     , plm.is_new_contractor_allowed            -- 新テナント
     , plm.free_end_date                        -- フリーレント終了日
     , ptl.id as parking_time_limit_id  		-- 時間制限
     /* 車室情報 */
     , pos.id as parking_position_id
     , '空き' as contract_status
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
  left join ap_parking_lot_type plt on lot.category_id = plt.code
  left join ap_parking_time_limit ptl on ptl.id = lot.time_limit_id
  left join ap_parking_lot_management plm on plm.parking_lot_id = lot.code
										 and plm.start_date <= current_date()
                                         and plm.end_date >= current_date()
  join ap_parking_position pos on lot.code = pos.parking_lot_id
