CREATE OR REPLACE VIEW v_temp_contract AS
select c.id
	 , c.id as contract_id
     , c.parking_lot_id
     , c.parking_position_id
     , get_process_percent(p.id) as percent		-- 完成度
     , c.contractor_id
     , c.contract_date
     , c.start_date
     , c.end_date
     , c.staff_id
     , c.mediation_id
     , c.staff_assistant1_id
     , c.staff_assistant2_id
     , c.staff_assistant3_id
     , c.payee_bank_account_id
     , c.car_maker_id
     , c.car_model
     , c.car_color
     , c.car_no_plate
     , c.car_comment
  from ap_contract c
  left join ap_process p on p.contract_id = c.id
 where c.is_deleted = 0
   and c.status = '01'		-- 仮契約
