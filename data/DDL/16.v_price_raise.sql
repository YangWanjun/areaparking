CREATE OR REPLACE VIEW v_price_raise AS
select c.id
     , c.id as contract_id
     , c.contractor_id
     , c.parking_lot_id
     , c.parking_position_id
     , c.car_id
     , c.staff_id
     , c.start_date
     , c.end_date
     , DATE_FORMAT(date_add(c.end_date, INTERVAL 1 MONTH), '%Y') as year
     , DATE_FORMAT(date_add(c.end_date, INTERVAL 1 MONTH), '%m') as month
     , cp.amount
     , (cp.amount + cp.consumption_tax) as amount_with_tax
     , prev_cp.amount as prev_amount
     , (prev_cp.amount + prev_cp.consumption_tax) as prev_amount_with_tax
     , case
           when c.contractor_id > 110 and c.contractor_id < 115 then true
           else false
	   end as is_defect								-- 不具合中
	 , case 
           when c.contractor_id < 105 then 20800
           else 24000
	   end as around_price							-- 周辺相場
     , case
           when prev_c.id is null then false
           -- 駐車場設備不具合
           when c.contractor_id > 110 and c.contractor_id < 115 then false
           -- 周辺相場が低め（APより安い駐車場がある）
           when c.contractor_id < 105 then false
           -- 昨年度の値上げの有無
           when (cp.amount + cp.consumption_tax) = (prev_cp.amount + prev_cp.consumption_tax) then true
           else false
	   end as is_raise
  from ap_contract c
  join ap_contractor cor on cor.code = c.contractor_id and cor.is_deleted = 0
  left join ap_contract_payment cp on cp.contract_id = c.id 
								  and cp.is_deleted = 0 
                                  and cp.timing = '30'
  left join ap_contract prev_c on prev_c.contractor_id = c.contractor_id 
                              and prev_c.is_deleted = 0 
                              and prev_c.end_date = DATE_SUB(c.start_date, INTERVAL 1 day)
  left join ap_contract_payment prev_cp on prev_cp.contract_id = prev_c.id 
							  and prev_cp.is_deleted = 0 
                              and prev_cp.timing = '30'
 where c.is_deleted = 0
   and c.end_date >= DATE_SUB(get_price_raise_limit_date(), INTERVAL 1 year)
   and c.end_date <= get_price_raise_limit_date()
   and exists (
	       select 1
             from ap_contract c1
			where c1.contractor_id = c.contractor_id
              and c1.is_deleted = 0
              and c1.start_date = DATE_ADD(c.end_date, INTERVAL 1 day)
	   )
   and not exists (
           select 1
             from ap_price_raising pr
			where pr.contract_id = c.id
              and pr.is_deleted = 0
       )
 order by c.end_date
