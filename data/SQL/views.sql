USE [areaparking]
GO

IF OBJECT_ID('dbo.v_whiteboard') IS NOT NULL
	DROP VIEW dbo.v_whiteboard
GO

CREATE view v_whiteboard
AS
SELECT lot.id as parking_lot_id
     , pos.id as parking_position_id
	 , bk.bk_no
	 , br.naibu_no
	 , br.hy_no as position_name
	 , lot.is_existed_contractor_allowed		-- 既契約者
	 , lot.is_new_contractor_allowed			-- 新テナント
	 , lot.free_end_date						-- フリーレント終了日
	 , lot.comment as lot_comment				-- 駐車場備考
	 /* 賃料 */
	 , pos.price_recruitment
	 , pos.price_recruitment_no_tax
	 , pos.price_homepage
	 , pos.price_homepage_no_tax
	 , pos.price_handbill
	 , pos.price_handbill_no_tax
	 /* サイズ */
	 , pos.length
	 , pos.width
	 , pos.height
	 , pos.weight
	 , pos.tyre_width
	 , pos.tyre_width_ap
	 , pos.min_height
	 , pos.min_height_ap
	 , pos.f_value
	 , pos.r_value

	 , pos.time_limit_id
	 , pos.comment as position_comment			-- 車室の備考
  FROM [fk5dtsql].[dbo].[bk_mst] bk
  LEFT JOIN [areaparking].[dbo].[ap_parking_lot] lot ON lot.buken_id = bk.bk_no AND lot.is_deleted = 0
  JOIN [fk5dtsql].[dbo].[bai_rooms] br ON br.bk_no = bk.bk_no
  LEFT JOIN [areaparking].[dbo].[ap_parking_position] pos ON pos.parking_lot_id = lot.id AND pos.is_deleted = 0 AND pos.seq_no = br.naibu_no

GO
