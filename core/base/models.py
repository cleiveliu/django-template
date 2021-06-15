from django.db import models

from core.shortcuts import _
from core.utils import uid_generator

# fmt: off

class ModelBase(models.Model):
    uid = models.CharField(_("uid"), max_length=64, unique=True, default=uid_generator, editable=False)
    create_time = models.DateTimeField(_("create time"), editable=False, auto_now_add=True)
    update_time = models.DateTimeField(_("update time"), editable=False, auto_now=True)

    class Meta:
        abstract = True
