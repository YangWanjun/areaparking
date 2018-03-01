# coding: UTF-8


class MyBaseException(Exception):
    def __init__(self, message):
        self.message = message


class FileNotExistException(MyBaseException):
    def __init__(self, message=""):
        MyBaseException.__init__(self, message)


class SettingException(MyBaseException):
    """
    設定はしてない場合、または設定間違った場合発生する例外
    """
    def __init__(self, message=""):
        MyBaseException.__init__(self, message)


class CustomException(MyBaseException):

    def __init__(self, message=""):
        MyBaseException.__init__(self, message)


class OperationFinishedException(MyBaseException):

    def __init__(self, message=""):
        MyBaseException.__init__(self, message)
