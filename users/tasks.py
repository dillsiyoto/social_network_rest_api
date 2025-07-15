from celery import Task
from settings.celery import celery_app
from common.mail import send_email


class ActivateAccountTask(Task):
    name = "activate-account"
    default_retry_delay = 60  # seconds

    def run(self, pk: int, username: str, email: str, code: str):
        try:
            send_email(
                template="activation.html",
                to=email,
                context={
                    "username": username,
                    "code": f"http://127.0.0.1:8000/api/v1/users/activate/{pk}/?code={code}",
                },
                title="Confirm your account",
            )
        except Exception as e:
            raise self.retry(exc=e, countdown=60 * (self.request.retries + 1))



activate_account_task = ActivateAccountTask()
celery_app.register_task(activate_account_task)