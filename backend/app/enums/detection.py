"""
Detection event related enumerations.
"""

from enum import Enum


class BehaviourType(str, Enum):
    """
    Supported AI behaviour types.
    """

    LOOKING_AWAY = "LOOKING_AWAY"
    HEAD_DOWN = "HEAD_DOWN"
    PHONE_DETECTED = "PHONE_DETECTED"
    PEER_CONVERSATION = "PEER_CONVERSATION"