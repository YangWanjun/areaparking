# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import os
import mimetypes
# import pyminizip
import traceback
import subprocess

from email import encoders
from email.header import Header

from django.conf import settings
from django.core.mail import EmailMultiAlternatives, get_connection, SafeMIMEText
from django.core.mail.message import MIMEBase
from django.db import connection
from django.utils.encoding import smart_str

from utils.errors import CustomException
from utils import constants, common


logger = common.get_ap_logger()


class EbMail(object):
    def __init__(self, sender=None, recipient_list=None, cc_list=None, bcc_list=None, attachment_list=None,
                 is_encrypt=True, mail_title=None, mail_body=None, pass_body=None):
        self.sender = sender
        self.recipient_list = EbMail.str_to_list(recipient_list)
        self.cc_list = EbMail.str_to_list(cc_list)
        self.bcc_list = EbMail.str_to_list(bcc_list)
        self.attachment_list = attachment_list
        self.is_encrypt = is_encrypt
        self.mail_title = mail_title
        self.mail_body = mail_body
        self.password = None
        self.pass_body = pass_body
        self.temp_files = []

    def check_recipient(self):
        if not self.recipient_list:
            raise CustomException("宛先はありません。")

    def check_attachment(self):
        if self.attachment_list:
            for attachment in self.attachment_list:
                if not os.path.exists(attachment):
                    raise CustomException("ファイル「%s」が見つかりません。" % attachment)

    def check_mail_title(self):
        if not self.mail_title:
            raise CustomException("メールの題名を設定してください。")

    @classmethod
    def get_mail_connection(cls):
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "select value from mst_config where name = %s "
                    " union all "
                    "select value from mst_config where name = %s "
                    " union all "
                    "select value from mst_config where name = %s "
                    " union all "
                    "select value from mst_config where name = %s ",
                    [constants.CONFIG_EMAIL_SMTP_HOST, constants.CONFIG_EMAIL_SMTP_PORT,
                     constants.CONFIG_EMAIL_ADDRESS, constants.CONFIG_EMAIL_PASSWORD]
                )
                host, port, username, password = cursor.fetchall()
            backend = get_connection()
            backend.host = str(host[0])
            backend.port = int(port[0])
            backend.username = str(username[0])
            backend.password = str(password[0])
            return backend
        except Exception as ex:
            logger.error(str(ex))
            logger.error(traceback.format_exc())
            raise CustomException(str(ex))

    @classmethod
    def str_to_list(cls, s):
        if isinstance(s, str):
            return [i.strip() for i in s.split(',') if i]
        else:
            return s

    # def zip_attachments(self):
    #     if self.attachment_list:
    #         temp_path = common.get_temp_path()
    #         temp_zip = os.path.join(temp_path, datetime.datetime.now().strftime('%Y%m%d%H%M%S%f.zip'))
    #         self.temp_files.append(temp_zip)
    #         # TODO: エンコードが不一致しているので、暫定対策はＯＳごとに処理する。
    #         file_list = []
    #         # if sys.platform == 'linux2':
    #         for f in self.attachment_list:
    #             new_path = os.path.join(temp_path, self.escape(os.path.basename(f)).encode('shift-jis'))
    #             shutil.copy(f, new_path)
    #             # ファイル名をshift-jisの名前に変更する、Windowsで開く時の文字化け防止
    #             # cmd = ['/usr/local/convmv-2.03/convmv', '--r', '--notest', '-f', 'utf8', '-t', 'cp932', new_path]
    #             # subprocess.check_output(cmd, shell=False)
    #             # new_path = new_path.encode('shift-jis')
    #             file_list.append(new_path)
    #             self.temp_files.append(new_path)
    #         # else:
    #         #     file_list = [f.encode('shift-jis') for f in self.attachment_list]
    #         password = self.generate_password()
    #         pyminizip.compress_multiple(file_list, temp_zip, password, 1)
    #         bytes = open(temp_zip, b'rb',).read()
    #         return bytes
    #     else:
    #         return None
    #
    # def escape(self, name):
    #     """Shift_JISのダメ文字対策
    #
    #     2バイト目に「5C」のコードが使われている文字は、次のようなものがあります。
    #     ―ソЫⅨ噂浬欺圭構蚕十申曾箪貼能表暴予禄兔喀媾彌拿杤歃濬畚秉綵臀藹觸軆鐔饅鷭偆砡
    #
    #     :param name:
    #     :return:
    #     """
    #     chars = u"ソЫⅨ噂浬欺圭構蚕十申曾箪貼能表暴予禄兔喀媾彌拿杤歃濬畚秉綵臀藹觸軆鐔饅鷭偆砡"
    #     s = name
    #     for c in chars:
    #         if c in s:
    #             s = s.replace(c, u"＿")
    #     return s
    #
    # def generate_password(self, length=8):
    #     self.password = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))
    #     return self.password

    def send_email(self, user=None):
        try:
            self.check_recipient()
            self.check_attachment()
            self.check_mail_title()

            mail_connection = self.get_mail_connection()
            if not self.sender:
                self.sender = mail_connection.username

            email = EmailMultiAlternativesWithEncoding(
                subject=self.mail_title,
                body=self.mail_body,
                from_email=self.sender,
                to=self.recipient_list,
                cc=self.cc_list,
                connection=mail_connection
            )
            email.attach_alternative(self.mail_body, constants.MIME_TYPE_HTML)
            # attachments = self.zip_attachments()
            # if attachments:
            #     email.attach('%s.zip' % self.mail_title, attachments, constants.MIME_TYPE_ZIP)
            email.send()
            # パスワードを送信する。
            self.send_password(mail_connection)
            log_format = u"題名: %s; TO: %s; CC: %s; 送信完了。"
            logger.info(log_format % (
                self.mail_title,
                ','.join(self.recipient_list) if self.recipient_list else '',
                ','.join(self.cc_list) if self.cc_list else ''
            ))

            if user:
                # 送信ログ
                from master.models import EMailLogEntry
                EMailLogEntry.objects.create(
                    user=user,
                    sender=self.sender,
                    recipient=",".join(self.recipient_list),
                    cc=",".join(self.cc_list) if self.cc_list else None,
                    bcc=",".join(self.bcc_list) if self.bcc_list else None,
                    title=self.mail_title,
                    body=self.mail_body,
                    attachment=",".join(self.attachment_list) if self.attachment_list else None
                )
        except subprocess.CalledProcessError as e:
            logger.error(e.output)
        finally:
            # 一時ファイルを削除
            for path in self.temp_files:
                if os.path.exists(path):
                    os.remove(path)

    def send_password(self, conn):
        if self.attachment_list and self.is_encrypt:
            # TODO: パスワードの送信もメールテンプレートに管理する。
            try:
                body = self.pass_body.format(password=self.password)
            except Exception:
                body = "PW: %s" % self.password
            email = EmailMultiAlternativesWithEncoding(
                subject=self.mail_title,
                body=body,
                from_email=self.sender,
                to=self.recipient_list,
                cc=self.cc_list,
                connection=conn
            )
            email.send()
            logger.info("%sのパスワードは送信しました。" % self.mail_title)


class EmailMultiAlternativesWithEncoding(EmailMultiAlternatives):
    def _create_attachment(self, filename, content, mimetype=None):
        """
        Converts the filename, content, mimetype triple into a MIME attachment
        object. Use self.encoding when handling text attachments.
        """
        if mimetype is None:
            mimetype, _ = mimetypes.guess_type(filename)
            # if mimetype is None:
            #     mimetype = constants.MIME_TYPE_EXCEL
        basetype, subtype = mimetype.split('/', 1)
        if basetype == 'text':
            encoding = self.encoding or settings.DEFAULT_CHARSET
            attachment = SafeMIMEText(smart_str(content, settings.DEFAULT_CHARSET), subtype, encoding)
        else:
            # Encode non-text attachments with base64.
            attachment = MIMEBase(basetype, subtype)
            attachment.set_payload(content)
            encoders.encode_base64(attachment)
        if filename:
            try:
                filename = filename.encode('ascii')
            except UnicodeEncodeError:
                filename = Header(filename, 'utf-8').encode()
            attachment.add_header('Content-Disposition', 'attachment', filename=filename)
        return attachment
