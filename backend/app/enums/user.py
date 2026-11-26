"""
User-related enumerations.
"""

from enum import Enum


class UserRole(str, Enum):
    """
    Supported user roles.
    """

    ADMINISTRATOR = "ADMINISTRATOR"
    TEACHER = "TEACHER"