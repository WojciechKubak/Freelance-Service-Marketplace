from enum import Enum
from dataclasses import dataclass
from abc import ABC


@dataclass
class EmailTemplate(ABC):
    subject: str = ""
    html_path: str = ""
    plain_text_path: str = ""


@dataclass
class ActivationEmail(EmailTemplate):
    subject: str = "Activate your account"
    html_path: str = "account_activation.html"
    plain_text_path: str = "account_activation.txt"


class EmailType(Enum):
    ACTIVATION: EmailTemplate = ActivationEmail
