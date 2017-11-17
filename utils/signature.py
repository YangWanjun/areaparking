# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os

from django.conf import settings

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random


SECRET_KEY = settings.SECRET_KEY
PATH_KEY_DIR = os.path.join(settings.MEDIA_ROOT, 'keys')


def sign(in_file):
    """電子署名を行う

    :param in_file:
    :return:
    """
    generate_keys()
    with open(get_private_key_path(), b'r') as f:
        rsa = RSA.importKey(f.read(), SECRET_KEY)
        digest = get_file_checksum(in_file)
        signature = rsa.sign(digest, '')[0]
    return str(signature)


def verify(in_file, signature):
    """ファイルを検証する、署名にあっているかどうかをチェックする。

    :param in_file:
    :param signature:
    :return:
    """
    with open(get_public_key_path(), b'r') as f:
        rsa = RSA.importKey(f.read(), SECRET_KEY)
        digest = get_file_checksum(in_file)
        is_verify = rsa.verify(digest, (long(signature),))
    return is_verify


def get_file_checksum(filename):
    """電子署名用のダイジェスト情報を取得する

    :param filename:
    :return:
    """
    h = SHA256.new()
    chunk_size = 8192
    with open(filename, b'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if len(chunk) == 0:
                break
            h.update(chunk)
    return h.digest()


def get_private_key_path():
    """秘密鍵の格納場所を取得する。

    :return:
    """
    if not os.path.exists(PATH_KEY_DIR):
        os.mkdir(PATH_KEY_DIR)
    return os.path.join(PATH_KEY_DIR, 'signature_private.pem')


def get_public_key_path():
    """公開鍵の格納場所を取得する。

    :return:
    """
    if not os.path.exists(PATH_KEY_DIR):
        os.mkdir(PATH_KEY_DIR)
    return os.path.join(PATH_KEY_DIR, 'signature_public.pem')


def generate_keys():
    path_private = get_private_key_path()
    path_public = get_public_key_path()
    # 既に作成済みの場合、再作成不要
    if os.path.exists(path_private) and os.path.exists(path_public):
        return
    random_generator = Random.new().read
    rsa = RSA.generate(1024, random_generator)
    # 秘密鍵作成
    private_pem = rsa.exportKey(format='PEM', passphrase=SECRET_KEY)
    with open(path_private, b'w') as f:
        f.write(private_pem)
    # 公開鍵作成
    public_pem = rsa.publickey().exportKey()
    with open(path_public, b'w') as f:
        f.write(public_pem)
