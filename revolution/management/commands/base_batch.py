# coding: UTF-8
from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from utils.common import get_batch_logger


class BaseBatch(BaseCommand):

    def __init__(self, *args, **kwargs):
        super(BaseBatch, self).__init__(*args, **kwargs)
        self.logger = get_batch_logger()

    def handle(self, *args, **options):
        pass

    def execute(self, *args, **options):
        return super(BaseBatch, self).execute(*args, **options)

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            action='store',
            dest='username',
            default='batch'
        )
