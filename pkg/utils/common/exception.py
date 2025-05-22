class ExitException(BaseException):  # 退出报错
    def __init__(self, msg=""):
        self.msg = msg

    def __str__(self):
        return self.msg

class ExitLoopException(BaseException):  # 退出循环
    def __init__(self, msg=""):
        self.msg = msg

    def __str__(self):
        return self.msg

class CaptchaExitException(BaseException):  # 出验证码退出循环
    def __init__(self, msg=""):
        self.msg = msg

    def __str__(self):
        return self.msg

class ExceedLimitException(BaseException):  # 超出限制
    def __init__(self, msg=""):
        self.msg = msg

    def __str__(self):
        return self.msg


class ProxyErrorExitException(BaseException):  # 代理错误退出报错
    def __init__(self, msg=""):
        self.msg = msg

    def __str__(self):
        return self.msg


class CaptchaExitException(BaseException):  # 验证码退出报错
    def __init__(self, msg=""):
        self.msg = msg

    def __str__(self):
        return self.msg


class LoginExitException(ExitException):  # 登录退出报错
    def __init__(self, msg=""):
        self.msg = msg

    def __str__(self):
        return self.msg


class ParseException(BaseException):  # 解析报错
    def __init__(self, msg=""):
        self.msg = msg

    def __str__(self):
        return self.msg


class LoginException(BaseException):  # 登陆报错
    def __init__(self, msg=""):
        self.msg = msg

    def __str__(self):
        return self.msg


class RiskException(BaseException):  # 风控报错
    def __init__(self, msg=""):
        self.msg = msg

    def __str__(self):
        return self.msg


class GoodsParseException(BaseException):  # 商品解析报错
    def __init__(self, msg=""):
        self.msg = msg

    def __str__(self):
        return self.msg
