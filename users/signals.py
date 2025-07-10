from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.core.mail import send_mail
from django.utils.timezone import now
from uuid import uuid4

from .models import LoginRecord

def get_client_ip(request):
    proxy_ip_header = request.META.get("HTTP_X_FORWARDED_FOR")
    if proxy_ip_header:
        client_ip = proxy_ip_header.split(",")[0].strip()
    else:
        client_ip = request.META.get("REMOTE_ADDR")
    return client_ip


@receiver(user_logged_in)
def check_ip_on_login(sender, request, user, **kwargs):
    ip = get_client_ip(request)
    if not LoginRecord.objects.filter(user=user, ip_address=ip).exists():
        code = uuid4().hex[:6] 
        LoginRecord.objects.create(
            user=user,
            ip_address=ip,
            confirmed=False,
            confirmation_code=code
        )

        send_mail(
            subject="Подозрительный вход",
            message=f"Обнаружен вход с нового IP: {ip}\nКод подтверждения: {code}",
            from_email="noreply@yourapp.com",
            recipient_list=[user.email],
        )
