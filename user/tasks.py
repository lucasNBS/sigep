from django.core.mail import send_mail
from celery import shared_task

@shared_task
def send_email_with_otp(to_email, otp):
    from django.conf import settings
    subject = "Seu código OTP"
    message = f"Seu código OTP é: {otp}"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [to_email]

    try:
        send_mail(subject, message, email_from, recipient_list)
    except Exception as e:
        print(f"Error sending email: {e}")