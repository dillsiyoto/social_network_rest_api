from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Codes(models.Model):
    code = models.CharField(
        verbose_name="код активации",
        unique=False,
        default="qwertyuiop"
    )
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name="user_code",
        verbose_name="пользователь"
    )
    created_at = models.DateTimeField(
        verbose_name="дата создания",
        default=timezone.now
    )

    class Meta:
        ordering = ("created_at",)
        verbose_name = "код активации"
        verbose_name_plural = "коды активации"

    def __str__(self):
        return f"{self.user.username} | {self.created_at}"

class LoginRecord(models.Model):
    user = models.ForeignKey(
        to=User, 
        on_delete=models.CASCADE, 
        related_name="login_records"
    )
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)

    confirmation_code = models.CharField(
        max_length=64,
        default="",
        blank=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.ip_address}"
