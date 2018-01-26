#!/bin/sh

mysql -h 127.0.0.1 -u root -proot areaparking < 01.get_process_percent.sql
mysql -h 127.0.0.1 -u root -proot areaparking < 02.get_position_status.sql
mysql -h 127.0.0.1 -u root -proot areaparking < 03.get_price_raise_limit_date.sql
mysql -h 127.0.0.1 -u root -proot areaparking < 11.v_whiteboard.sql
mysql -h 127.0.0.1 -u root -proot areaparking < 12.v_whiteboard_position.sql
mysql -h 127.0.0.1 -u root -proot areaparking < 13.v_transfer_detail.sql
mysql -h 127.0.0.1 -u root -proot areaparking < 14.v_contractor_request.sql
mysql -h 127.0.0.1 -u root -proot areaparking < 15.v_arrears.sql
mysql -h 127.0.0.1 -u root -proot areaparking < 16.v_price_raise.sql