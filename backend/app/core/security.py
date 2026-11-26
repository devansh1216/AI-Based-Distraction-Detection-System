"""
Security utilities for JWT authentication.
"""

from datetime import datetime, timedelta, timezone
from typing import Any

import jwt

from app.core.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    SECRET_KEY,
)



# ------------------------------------------------------------------------------
# JWT Access Token
# ------------------------------------------------------------------------------

def create_access_token(
    subject: str,
    expires_delta: timedelta | None = None,
) -> str:
    """
    Create a signed JWT access token.
    """

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    payload: dict[str, Any] = {
        "sub": subject,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


# ------------------------------------------------------------------------------
# JWT Verification
# ------------------------------------------------------------------------------

def verify_access_token(
    token: str,
) -> dict[str, Any]:
    """
    Decode and verify a JWT access token.

    Raises an exception if the token is invalid or expired.
    """

    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM],
    )