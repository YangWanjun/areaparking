# coding: UTF-8
from __future__ import unicode_literals

from base_batch import BaseBatch
from revolution.batch import sync_buken


class Command(BaseBatch):

    def handle(self, *args, **options):
        self.logger.info("賃貸革命から物件同期開始>>>>")
        # username = options.get('username')
        buken_count, room_count = sync_buken()
        self.logger.info("{0}の物件が同期されました、{1}の車室が同期されました。".format(buken_count, room_count))
        self.logger.info("賃貸革命から物件同期終了<<<<")
