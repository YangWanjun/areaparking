USE [areaparking]
GO

IF OBJECT_ID('dbo.v_parking_lot') IS NOT NULL
	DROP VIEW dbo.v_parking_lot
GO

CREATE view v_parking_lot
AS
SELECT *, 0 as is_deleted FROM [fk5dtsql].[dbo].[bk_mst]

GO

IF OBJECT_ID('dbo.v_m_brui') IS NOT NULL
	DROP VIEW dbo.v_m_brui
GO

CREATE view v_m_brui
AS
SELECT *, 0 as is_deleted FROM [fk5dtsql].[dbo].[m_brui]
