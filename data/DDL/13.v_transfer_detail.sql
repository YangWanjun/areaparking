CREATE OR REPLACE VIEW v_transfer_detail AS
select distinct td.id
     , td.reference_no
     , td.settlement_ymd
     , td.reckoning_ymd
     , td.in_out_kbn
     , td.trade_kbn
     , td.amount
     , td.other_amount
     , td.exchange_ymd
     , td.return_ymd
     , td.check_kbn
     , td.check_no
     , td.branch_no
     , td.nominee_code
     , td.nominee_name
     , td.bank_name
     , td.branch_name
     , td.summary
     , td.header_id
	 , td.id as detail_id
     , r.id as request_id
     , r.amount as request_amount
     , (td.amount - ifnull(r.amount, 0)) as deficit
     , c.id as contract_id
     , c.contractor_id
     , c.parking_lot_id
     , c.parking_position_id
     , case
           when r.id is null then '00'
           when td.amount != r.amount and (td.amount - ifnull(r.amount, 0)) <= 2000 and (td.amount - ifnull(r.amount, 0)) >= -2000 then '03'
           when td.amount != r.amount then '01'
           when td.nominee_name != cor.kana then '02'
           when td.amount = r.amount then '11'
           else '99'
	   end as status
	 , case
	       when (select count(1) from ap_contractor_transfer ct where ct.is_deleted = 0 and ct.contractor_id = cor.code) then 1
           else 0
       end as is_committed
  from ap_transfer_detail td
  left join mst_bank_account ba on ba.account_number = SUBSTRING(td.nominee_code, 4)
  left join ap_request r on r.bank_account_id = ba.id
  left join ap_contract c on c.payee_bank_account_id = ba.id
  left join ap_contractor cor on cor.code = c.contractor_id
 where td.is_deleted = 0