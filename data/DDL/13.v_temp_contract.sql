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
     , c.car_id
  from ap_contract c
  join django_content_type ct on ct.app_label = 'contract' and ct.model = 'contract'
  left join ap_process p on p.content_type_id = ct.id and p.object_id = c.id
 where c.is_deleted = 0
   and c.status = '01'		-- 仮契約
