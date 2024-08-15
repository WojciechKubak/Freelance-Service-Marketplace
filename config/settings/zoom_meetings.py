from typing import Final
import os


ZOOM_ACCOUNT_ID: Final[str] = os.environ.get("ZOOM_ACCOUNT_ID")
ZOOM_CLIENT_ID: Final[str] = os.environ.get("ZOOM_CLIENT_ID")
ZOOM_CLIENT_SECRET: Final[str] = os.environ.get("ZOOM_CLIENT_SECRET")
