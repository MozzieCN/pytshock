class TShockException(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message


class NoPermissionException(TShockException):
    def __init__(self , message):
        super().__init__(401,message)


class ParamException(TShockException):
    def __init__(self):
        super().__init__(403, '参数错误')


class ServerException(TShockException):
    def __init__(self):
        super().__init__(500, '访问服务器错误')
