CREATE OR REPLACE VIEW v_map_board AS
select lot.code as id
     , lot.code as parking_lot_id
     , lot.name as parking_lot_name
     , lot.staff_id
     , concat(m.first_name, ' ', m.last_name) as staff_name
     , CONCAT(lot.pref_name, lot.city_name, ifnull(lot.town_name, ''), ifnull(lot.aza_name, ''), ifnull(lot.other_name, '')) as address
     , lot.lng
     , lot.lat
     , (select count(1) 
          from ap_parking_position pos1 
		 where pos1.parking_lot_id = lot.code
           and pos1.is_deleted = 0
       ) as position_count
     , 0 as waiting_count
     , (select count(1)
          from ap_contract c1
		 where c1.parking_lot_id = lot.code
           and c1.is_deleted = 0
		   and c1.start_date <= current_date()
		   and c1.end_date >= current_date()
       ) as contract_count
     , (select count(1)
          from ap_temp_contract c1
		 where c1.parking_lot_id = lot.code
           and c1.is_deleted = 0
       ) as temp_contract_count
     , plm.is_existed_contractor_allowed        -- 既契約者
     , plm.is_new_contractor_allowed            -- 新テナント
     , plm.free_end_date                        -- フリーレント終了日
     , ptl.id as parking_time_limit_id  		-- 時間制限
     , lot.created_date
     , lot.updated_date
     , lot.is_deleted
     , lot.deleted_date
  from ap_parking_lot lot
  left join ap_parking_lot_type plt on lot.category_id = plt.code and plt.is_deleted = 0
  left join ap_parking_time_limit ptl on ptl.id = lot.time_limit_id and ptl.is_deleted = 0
  left join ap_parking_lot_management plm on plm.parking_lot_id = lot.code
										 and plm.start_date <= current_date()
                                         and plm.end_date >= current_date()
                                         and plm.is_deleted = 0
  left join ap_member m on m.id = lot.staff_id
 where lot.is_deleted = 0
