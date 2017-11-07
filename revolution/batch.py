# coding: UTF-8
from __future__ import unicode_literals

from django.db import connection


def sync_buken():
    with connection.cursor() as cursor:
        cursor.execute(
            " INSERT INTO areaparking.dbo.ap_parking_lot (buken_id, is_existed_contractor_allowed, is_new_contractor_allowed, created_date, updated_date, is_deleted)"
            " SELECT bk_no, 0, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 0"
            "   FROM fk5dtsql.dbo.bk_mst"
            "  WHERE NOT EXISTS (SELECT 1 FROM areaparking.dbo.ap_parking_lot WHERE ap_parking_lot.buken_id = bk_mst.bk_no)"
        )
        buken_count = cursor.rowcount
        cursor.execute(
            " INSERT INTO areaparking.dbo.ap_parking_position (parking_lot_id, seq_no, name, created_date, updated_date, is_deleted)"
            " SELECT (SELECT id FROM areaparking.dbo.ap_parking_lot WHERE ap_parking_lot.buken_id=bai_rooms.bk_no) as bk_no"
            "      , naibu_no, hy_no"
            "      , CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 0 as is_deleted"
            "   FROM fk5dtsql.dbo.bai_rooms"
            "  WHERE NOT EXISTS ("
            "            SELECT 1 FROM areaparking.dbo.ap_parking_lot t1 "
            " 		       JOIN areaparking.dbo.ap_parking_position t2 ON t1.id = t2.parking_lot_id"
            "             WHERE t1.buken_id = bai_rooms.bk_no"
            "               AND t2.seq_no = bai_rooms.naibu_no"
            "        )"
        )
        room_count = cursor.rowcount
    return buken_count, room_count
