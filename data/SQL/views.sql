USE [areaparking]
GO

IF OBJECT_ID('dbo.v_whiteboard') IS NOT NULL
    DROP VIEW dbo.v_whiteboard
GO

CREATE view v_whiteboard
AS
SELECT RIGHT('0000000000'+ CONVERT(VARCHAR, bk.bk_no), 10) + '|' + hy.hy_no AS id
     , lot.id as parking_lot_id
     , pos.id as parking_position_id
     , bk.bk_no
     , bk.bk_name
	 , (SELECT COUNT(1) FROM [areaparking].[dbo].[ap_parking_position] s1 WHERE s1.parking_lot_id = lot.id AND s1.is_deleted = 0) as position_count
	 , (SELECT COUNT(1) FROM [areaparking].[dbo].[ap_waiting_list] s1 WHERE s1.parking_lot_id = lot.id) as waiting_count
     , hy.hy_no as position_name
	 , CONCAT(bk.add_ken, bk.add_si, bk.add_cyo, bk.add_banti, bk.add_etc) as address
	 , lot.lng
	 , lot.lat
	 , mt.tanto_name							-- 担当者
     , lot.is_existed_contractor_allowed        -- 既契約者
     , lot.is_new_contractor_allowed            -- 新テナント
     , lot.free_end_date                        -- フリーレント終了日
     , lot.comment as lot_comment               -- 駐車場備考
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
     , pos.comment as position_comment          -- 車室の備考
	 /* 契約 */
	 , CASE
	       WHEN ky.ky_no IS NOT NULL THEN 'なし'
		   ELSE '空き'
	   END AS contract_status
  FROM [fk5dtsql].[dbo].[bk_mst] bk
  LEFT JOIN [areaparking].[dbo].[ap_parking_lot] lot ON lot.buken_id = bk.bk_no AND lot.is_deleted = 0
  JOIN [fk5dtsql].[dbo].[hy_mst] hy ON hy.bk_no = bk.bk_no
  LEFT JOIN [areaparking].[dbo].[ap_parking_position] pos ON pos.parking_lot_id = lot.id AND pos.is_deleted = 0 AND pos.name = hy.hy_no
  LEFT JOIN [fk5dtsql].[dbo].[m_tanto] mt ON mt.tanto_no = bk.tanto_no
  LEFT JOIN [fk5dtsql].[dbo].[ky_kosinkai] ky ON ky.bk_no = bk.bk_no AND ky.hy_no = hy.hy_no AND ky.ky_start_ymd <= GETDATE() AND ky.ky_end_ymd >= GETDATE()

GO
