CREATE OR REPLACE VIEW v_contractor_request AS
select cor.code as id
     , cor.code as contractor_id
     , cor.name
     , r.id as request_id
  from ap_contractor cor
  left join ap_request r on r.bank_account_id = cor.payee_bank_account_id