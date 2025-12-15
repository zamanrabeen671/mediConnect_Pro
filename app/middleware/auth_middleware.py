"""
Authentication middleware
"""
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)


class AuthMiddleware(BaseHTTPMiddleware):
    """
    Custom middleware for authentication validation
    """
    
    async def dispatch(self, request: Request, call_next):
        """
        Process request and add authentication context
        """
        # Log incoming request
        logger.info(f"{request.method} {request.url.path}")
        
        # Call next middleware/route
        response = await call_next(request)
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        
        return response
