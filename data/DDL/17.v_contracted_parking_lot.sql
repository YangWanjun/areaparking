CREATE OR REPLACE VIEW v_contracted_parking_lot AS
select lot.code
	 , lot.name
     , lot.staff_id
     , lot.category_id
     , post_code
     , CONCAT(lot.pref_name, lot.city_name, ifnull(lot.town_name, ''), ifnull(lot.aza_name, ''), ifnull(lot.other_name, '')) as address
     , lot.owner
     , lot.lender
     , (select count(1) from ap_parking_position pos where pos.parking_lot_id = lot.code and is_deleted = 0) as position_count
     , (select count(1) 
          from ap_contract c
         where c.parking_lot_id = lot.code 
           and c.status = '11' 
           and c.start_date <= current_date()
           and c.end_date >= current_date()
           and c.is_deleted = 0
       ) as contract_count
     , lot.building_management_company_id     	-- 既契約者
     , lot.lease_management_company_id         	-- 新テナント
     , lot.code as parking_lot_id
     , lot_c.id as parking_lot_cancellation_id	-- 物件解約
     , lot_c.is_all as is_all_cancellation		-- 全件解約
  from ap_parking_lot lot
  left join ap_parking_lot_cancellation lot_c on lot_c.parking_lot_id = lot.code
 order by lot.pref_code, lot.city_code, lot.town_name, lot.aza_name, lot.other_name
