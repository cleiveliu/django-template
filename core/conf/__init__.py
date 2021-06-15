from core.base.enum import IntEnum


class RespCode(IntEnum):
    # common
    Succeed = 200  # 成功
    Fail = -1  # 失败
    NotFound = 404  # 未找到

    # auth 400-449
    NotLogin = 400  # 未登录
    WrongPassword = 401  # 密码错误
    WrongVerifyCode = 402  # 验证码错误
    NoPermission = 403  # 没有权限
    Banned = 444  # 被拉黑了

    # param 450-499
    InvalidParam = 450  # 参数格式不正确, 类型不匹配或缺失必需参数; 参数逻辑错误, 如年龄小于0
    ParamsLogicWrong = 451

    # business
    NotEnoughBalance = -2  # 余额不足

    # server error
    Exception = 500  # 服务器内部错误
