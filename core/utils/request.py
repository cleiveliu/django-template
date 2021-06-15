from rest_framework.request import Request
from rest_framework.request import QueryDict


def current_user(request: Request):
    """返回当前请求的用户, 若未登录, 则返回None"""
    return request.user if request.user.is_active else None


def get_pure_query_params(query_params: QueryDict):
    return {k: v for k, v in query_params.items()}
