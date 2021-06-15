from core.utils.request import current_user
from authentication.serializers import UserSer
from django.contrib.auth import login, authenticate

from core.shortcuts import APIView, Request, RespCode, AllowAny

from authentication.schemas import SchemaLogin


def password_login(request, data: SchemaLogin):
    user = authenticate(request, username=data.username, password=data.password)
    if user:
        login(request, user, backend="django.contrib.auth.backends.ModelBackend")
        return RespCode.Succeed, {}, ""
    else:
        return RespCode.WrongPassword, {}, "username or password is not correct"


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request):
        data = SchemaLogin(**request.data)
        return password_login(request, data)


def get_user_info(user):
    if not user:
        return RespCode.NotLogin, {}, ""
    return RespCode.Succeed, UserSer(user, exclude=["password"]).data, ""


class UserInfoView(APIView):
    def get(self, request: Request):
        user = current_user(request)
        return get_user_info(user)
