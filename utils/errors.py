# coding: UTF-8


class MyBaseException(Exception):
    def __init__(self, message):
        self.message = message


class FileNotExistException(MyBaseException):
    def __init__(self, message=""):
        MyBaseException.__init__(self, message)


class CustomException(MyBaseException):
    def __init__(self, message=""):
        MyBaseException.__init__(self, message)
