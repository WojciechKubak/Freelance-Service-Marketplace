from apps.common.models import BaseModel
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager as BUM
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from typing import Self
import uuid


class BaseUserManager(BUM):

    def create_user(
        self,
        email: str,
        password: str | None = None,
        is_admin: bool = False,
    ) -> Self:
        user = self.model(email=self.normalize_email(email.lower()), is_admin=is_admin)
        user.set_password(password)

        user.full_clean()
        user.save(using=self._db)

        return user

    def create_superuser(
        self,
        email: str,
        password: str | None = None,
    ) -> Self:
        user = self.create_user(email, password, is_admin=True)
        user.is_superuser = True

        user.save(using=self._db)

        return user


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )

    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = BaseUserManager()

    USERNAME_FIELD = "email"

    class Meta:
        db_table = "users"

    def __str__(self) -> str:
        return self.email

    @property
    def is_staff(self) -> bool:
        return self.is_admin
