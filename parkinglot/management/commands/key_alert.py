from parkinglot.biz import get_lacking_keys
from master.models import BatchManage, MailGroup, MailTemplate
from utils.django_base import BaseBatch
from utils.app_base import push_notification


class Command(BaseBatch):
    BATCH_NAME = 'key_alert'
    BATCH_TITLE = '鍵残件数アラートバッチ'

    def handle(self, *args, **options):
        lacking_keys = get_lacking_keys()
        for parking_lot, category, name, count in lacking_keys:
            self.logger.debug('駐車場：{0:50}鍵分類：{1:10}足りない本数：{2:>5}'.format(
                str(parking_lot), name, str(count)
            ))
        if lacking_keys:
            # メール通知
            group = MailGroup.get_batch_key_alert_group()
            context = {'lacking_keys': lacking_keys}
            group.send_main('yangwanjun@e-business.co.jp', context)
            # プッシュ通知
            push_notification(self.BATCH_TITLE, "鍵が足りない")

    def get_batch_manager(self):
        """指定名称のバッチを取得する。

        :param name:
        :return:
        """
        return BatchManage.get_batch_by_name(self.BATCH_NAME)
