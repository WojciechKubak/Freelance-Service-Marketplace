from enum import Enum


class EmailSendingStrategy(Enum):
    CONSOLE = "console"
    SMTP = "smtp"
