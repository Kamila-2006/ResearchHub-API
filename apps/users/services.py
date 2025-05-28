import uuid
from django.core.cache import cache
from django.core.mail import send_mail


def send_verification_token(email, user_data):
    token = str(uuid.uuid4())
    cache.set(token, email, timeout=60 * 15)
    cache.set(email, (token, user_data), timeout=60 * 15)

    send_mail(
        "Verify your email",
        f"Here is your verification token: {token}",
        "noreply@example.com",
        [email],
        fail_silently=False,
    )
