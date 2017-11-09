USE [areaparking]
GO

IF OBJECT_ID('dbo.bk_mst') IS NOT NULL
	DROP SYNONYM [dbo].[bk_mst]
GO

CREATE SYNONYM [dbo].[bk_mst] FOR [fk5dtsql].[dbo].[bk_mst]
GO


