CREATE OR REPLACE VIEW v_bank_account AS
select ba.id
     , ba.branch_no
     , ba.branch_name
     , ba.account_type
     , ba.account_number
     , ba.account_holder
     , ba.bank_id
     , c.id as contract_id
     , c.parking_lot_id
     , c.parking_position_id
     , c.contractor_id
     , c.subscription_id
     , case
	       when c.id is null then '0'
           else '1'
	   end as status
  from mst_bank_account ba
  left join ap_contract c on c.payee_bank_account_id = ba.id
                         and c.start_date <= current_date()
                         and c.end_date >= current_date()
 where ba.is_deleted = 0
