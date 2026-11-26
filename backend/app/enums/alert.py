"""
Alert-related enumerations.
"""

from enum import Enum


class AlertSeverity(str, Enum):
    """
    Supported alert severity levels.
    """

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class AlertStatus(str, Enum):
    """
    Supported alert statuses.
    """

    ACTIVE = "ACTIVE"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    DISMISSED = "DISMISSED"


class AlertType(str, Enum):
    """
    Supported alert types.
    """

    LOOKING_AWAY = "LOOKING_AWAY"
    HEAD_DOWN = "HEAD_DOWN"
    PHONE_DETECTED = "PHONE_DETECTED"
    PEER_CONVERSATION = "PEER_CONVERSATION"