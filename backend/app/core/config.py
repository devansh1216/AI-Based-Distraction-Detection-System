"""
Application configuration.

Loads environment variables required by the backend.
"""

import os

from dotenv import load_dotenv

# ------------------------------------------------------------------------------
# Load Environment Variables
# ------------------------------------------------------------------------------

load_dotenv()

# ------------------------------------------------------------------------------
# Database
# ------------------------------------------------------------------------------

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./distraction.db",
)

# ------------------------------------------------------------------------------
# JWT Authentication
# ------------------------------------------------------------------------------

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "change-this-development-secret-key",
)

ALGORITHM = os.getenv("ALGORITHM", "HS256")

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
)