CREATE OR REPLACE VIEW v_arrears AS
select r.id
     , r.id as request_id
     , r.amount as request_amount
     , DATE_FORMAT(r.limit_date, '%y.%m.%d') as limit_date
     , DATEDIFF(current_date(), r.limit_date) as date_diff
     , case
           when r.id <= 15 then true
           else false
	   end as is_sent
	 , r.payment_kbn
     , cor.code as contractor_id
     , cor.kana
     , cor.tel
     , c.id as contract_id
     , c.parking_lot_id
     , c.parking_position_id
     , DATE_FORMAT(c.start_date, '%y.%m.%d') as contract_start_date
     , IFNULL(td.amount, 0) as transfer_amount
     , (r.amount - IFNULL(td.amount, 0)) as amount
  from ap_request r
  join ap_contract_payment cp on cp.id = r.contract_payment_id and cp.is_deleted = 0
  join ap_contract c on c.id = cp.contract_id
  join ap_contractor cor on cor.code = c.contractor_id
  left join ap_contractor_transfer ct on ct.contractor_id = cor.code
  left join ap_transfer_detail td on td.id = ct.transfer_detail_id
 where r.is_deleted = 0
   and r.amount > IFNULL(td.amount, 0)
