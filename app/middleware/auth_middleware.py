
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi import HTTPException
from ..core.security import verify_token
import logging

logger = logging.getLogger(__name__)


class AuthMiddleware(BaseHTTPMiddleware):
    """
    Custom middleware for authentication extraction.
    Reads an Authorization header (or `authorization`) and verifies the token.
    If token is valid, sets `request.state.user_id` and `request.state.user_role`.
    """

    async def dispatch(self, request: Request, call_next):
        """
        Process request and attach authentication context
        """
        # Log incoming request
        logger.info(f"{request.method} {request.url.path}")

        # Default state
        request.state.user_id = None
        request.state.user_role = None

        auth_header = request.headers.get("authorization") or request.headers.get("Authorization")
        if auth_header:
            # Accept either 'Bearer <token>' or raw token in header
            token = auth_header
            if isinstance(auth_header, str) and auth_header.lower().startswith("bearer "):
                token = auth_header.split(None, 1)[1]
            try:
                payload = verify_token(token)
                request.state.user_id = payload.get("id")
                request.state.user_role = payload.get("role")
            except HTTPException:
                # Invalid token: leave state as None and continue
                logger.debug("Invalid auth token in request; continuing as anonymous")

        # Call next middleware/route
        response = await call_next(request)

        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"

        return response
