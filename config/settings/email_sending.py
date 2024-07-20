from config.env import env_to_enum, env_to_bool
from apps.emails.enums import EmailSendingStrategy
import os


EMAIL_SENDING_STRATEGY = env_to_enum(
    EmailSendingStrategy, os.environ.get("EMAIL_SENDING_STRATEGY", "console")
)

EMAIL_ACTIVATION_TIMEOUT = int(os.environ.get("EMAIL_ACTIVATION_TIMEOUT", 60 * 60 * 24))

if EMAIL_SENDING_STRATEGY == EmailSendingStrategy.CONSOLE:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

if EMAIL_SENDING_STRATEGY == EmailSendingStrategy.SMTP:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = os.environ.get("EMAIL_HOST")
    EMAIL_USE_TLS = env_to_bool(os.environ.get("EMAIL_USE_TLS"), False)
    EMAIL_USE_SSL = env_to_bool(os.environ.get("EMAIL_USE_SSL"), True)
    EMAIL_PORT = os.environ.get("EMAIL_PORT")
    EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
