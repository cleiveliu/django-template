from core.shortcuts import CustomSer

from authentication.models import User


class UserSer(CustomSer):
    class Meta:
        model = User
        fields = "__all__"
