CREATE OR REPLACE VIEW v_whiteboard AS
select pos.id as id
     , lot.code as parking_lot_id
     , lot.name as parking_lot_name
     , lt.name as segment
     , CONCAT(lot.pref_name, lot.city_name, ifnull(lot.town_name, ''), ifnull(lot.aza_name, ''), ifnull(lot.other_name, '')) as address
     , lot.lng
     , lot.lat
     , pos.id as parking_position_id
     , pos.name as parking_position_name
     , lot.is_existed_contractor_allowed        -- 既契約者
     , lot.is_new_contractor_allowed            -- 新テナント
     , lot.free_end_date                        -- フリーレント終了日
     , tl.name as time_limit  					-- 時間制限
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
  left join ap_parking_lot_type lt on lot.segment_id = lt.code
  left join ap_parking_time_limit tl on tl.id = lot.time_limit_id
  join ap_parking_position pos on lot.code = pos.parking_lot_id
