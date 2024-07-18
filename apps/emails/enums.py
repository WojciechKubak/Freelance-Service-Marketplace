from enum import Enum


class EmailSendingStrategy(Enum):
    CONSOLE: str = "console"
    SMTP: str = "smtp"
