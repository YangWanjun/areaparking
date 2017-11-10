USE areaparking
GO

CREATE TABLE ap_parking_lot (
    [id] int IDENTITY (1, 1) NOT NULL PRIMARY KEY,
    [buken_id] int NOT NULL,
    [is_existed_contractor_allowed] bit NOT NULL,
    [is_new_contractor_allowed] bit NOT NULL,
    [free_end_date] date NULL,
    [comment] varchar(255) NULL,
    [created_date] datetime NOT NULL,
    [updated_date] datetime NOT NULL,
    [is_deleted] bit NOT NULL,
    [deleted_date] datetime NULL
)
