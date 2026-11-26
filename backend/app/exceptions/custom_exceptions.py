"""
Custom exceptions used throughout the application.
"""


class AppException(Exception):
    """
    Base exception for all custom application exceptions.
    """

    def __init__(
        self,
        message: str,
    ):
        self.message = message
        super().__init__(message)


# ------------------------------------------------------------------------------
# Authentication Exceptions
# ------------------------------------------------------------------------------


class AuthenticationException(AppException):
    """
    Raised when authentication fails.
    """

    pass


class AuthorizationException(AppException):
    """
    Raised when a user does not have permission.
    """

    pass


# ------------------------------------------------------------------------------
# Resource Exceptions
# ------------------------------------------------------------------------------


class UserNotFoundException(AppException):
    """
    Raised when a user cannot be found.
    """

    pass


class ClassroomNotFoundException(AppException):
    """
    Raised when a classroom cannot be found.
    """

    pass


class CameraNotFoundException(AppException):
    """
    Raised when a camera cannot be found.
    """

    pass


class MonitoringSessionNotFoundException(AppException):
    """
    Raised when a monitoring session cannot be found.
    """

    pass


class DetectionEventNotFoundException(AppException):
    """
    Raised when a detection event cannot be found.
    """

    pass


class AlertNotFoundException(AppException):
    """
    Raised when an alert cannot be found.
    """

    pass


class ReportNotFoundException(AppException):
    """
    Raised when a report cannot be found.
    """

    pass


# ------------------------------------------------------------------------------
# Business Logic Exceptions
# ------------------------------------------------------------------------------


class ValidationException(AppException):
    """
    Raised when business validation fails.
    """

    pass


class DuplicateResourceException(AppException):
    """
    Raised when attempting to create a duplicate resource.
    """

    pass


class ReportGenerationException(AppException):
    """
    Raised when report generation fails.
    """

    pass