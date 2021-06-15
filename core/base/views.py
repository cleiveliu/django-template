from rest_framework.views import APIView as _APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.settings import api_settings


from core.utils.response import standard_response_format
from core import settings


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class APIView(_APIView):

    # 如果 DEBUG为True, 则关闭csrf校验, 方便 postman 等工具测试
    # 参考: https://stackoverflow.com/questions/30871033/django-rest-framework-remove-csrf
    authentication_classes = (
        (CsrfExemptSessionAuthentication, BasicAuthentication)
        if settings.DEBUG == True
        else api_settings.DEFAULT_AUTHENTICATION_CLASSES
    )

    # Note: Views are made CSRF exempt from within `as_view` as to prevent
    # accidental removal of this exemption in cases where `dispatch` needs to
    # be overridden.
    def dispatch(self, request, *args, **kwargs):
        """
        `.dispatch()` is pretty much the same as Django's regular dispatch,
        but with extra hooks for startup, finalize, and exception handling.
        """
        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers  # deprecate?

        try:
            self.initial(request, *args, **kwargs)

            # Get the appropriate handler method
            if request.method.lower() in self.http_method_names:
                handler = getattr(
                    self, request.method.lower(), self.http_method_not_allowed
                )
            else:
                handler = self.http_method_not_allowed

            response = handler(request, *args, **kwargs)

        except Exception as exc:
            response = self.handle_exception(exc)

        # 对视图函数返回格式为 (code, body, msg) 的数据
        # 自动转成 Respons({"code": code, "body": body, "message": msg)
        # 不用每个试图函数写 `return standard_response_format(code, body, msg)``
        if isinstance(response, (tuple, list)):
            try:
                response = standard_response_format(*response)
            except Exception as e:
                response = self.handle_exception(e)

        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response


"""
from rest_framework.request import Request
from pydantic import BaseModel
from core.conf.http import get_request_method, post_request_method
from core.utils.request import current_user, get_pure_query_params
handle_func = None
    http_method = post_request_method
    schema_model: BaseModel = None

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        schema_model = self._get_handle_func_schema_model()
        if schema_model is None:
            return
        if not issubclass(schema_model, BaseModel):
            raise ValueError("not surpported schema:", schema)
        self.schema_model = schema_model
        if self.http_method == get_request_method:
            setattr(self, "get", self.__get)
        elif self.http_method == post_request_method:
            setattr(self, "post", self.__post)
        else:
            raise ValueError("not sourpported method:", self.http_method)

    def _get_handle_func_schema_model(self):
        if self.handle_func is None:
            return None
        return self.handle_func.__annotations__["data"]

    def __get(self, request: Request):
        d = get_pure_query_params(request.query_params)
        data = self.schema_model(**d)
        user = current_user(request)
        return self.handle_func(request, user, data)

    def __post(self, request: Request):
        data = self.schema_model(**request.data)
        user = current_user(request)
        return self.handle_func(request, user, data)
    
"""
