CREATE OR REPLACE VIEW v_whiteboard AS
select lot.code as code
     , lot.code as parking_lot_id
     , lot.name
     , lot.staff_id
     , lot.category_id
     , CONCAT(lot.pref_name, lot.city_name, ifnull(lot.town_name, ''), ifnull(lot.aza_name, ''), ifnull(lot.other_name, '')) as address
     , lot.lng
     , lot.lat
     , (select count(1) from ap_parking_position pos where pos.parking_lot_id = lot.code and is_deleted = 0) as position_count
     , (select count(1) 
          from ap_contract c
         where c.parking_lot_id = lot.code 
           and c.status = '11' 
           and c.start_date <= current_date()
           and c.end_date >= current_date()
           and c.is_deleted = 0
       ) as contract_count
     , (select count(1) from ap_subscription s where s.parking_lot_id = lot.code and s.status < '11' and s.is_deleted = 0) as temp_contract_count
     , 0 as waiting_count
     , lot.is_existed_contractor_allowed        -- 既契約者
     , lot.is_new_contractor_allowed            -- 新テナント
     , lot.free_end_date                        -- フリーレント終了日
  from ap_parking_lot lot
 where lot.is_deleted = 0