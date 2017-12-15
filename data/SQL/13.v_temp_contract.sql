CREATE OR REPLACE VIEW v_temp_contract AS
select c.id
     , c.id as temp_contract_id
     , c.parking_lot_id
     , cor.id as contractor_id
     , c.created_date
     , c.updated_date
     , c.is_deleted
     , c.deleted_date
  from ap_temp_contract c
  join ap_temp_contractor cor on c.contractor_id = cor.id
  left join ap_parking_lot lot on c.parking_lot_id = lot.code