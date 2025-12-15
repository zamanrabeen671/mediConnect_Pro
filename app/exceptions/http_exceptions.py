"""
Custom HTTP exceptions
"""
from fastapi import HTTPException, status


class EmailAlreadyExistsException(HTTPException):
    """Exception raised when email already exists"""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )


class InvalidCredentialsException(HTTPException):
    """Exception raised for invalid credentials"""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )


class NotAuthenticatedException(HTTPException):
    """Exception raised when user is not authenticated"""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"}
        )


class PermissionDeniedException(HTTPException):
    """Exception raised when user doesn't have permission"""
    def __init__(self, detail: str = "Permission denied"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )


class ResourceNotFoundException(HTTPException):
    """Exception raised when resource is not found"""
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )


class ValidationException(HTTPException):
    """Exception raised for validation errors"""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        )
