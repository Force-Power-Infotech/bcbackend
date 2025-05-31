from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

class MethodOverrideMiddleware(BaseHTTPMiddleware):
    """
    Middleware for method override in HTML forms.
    
    This allows HTML forms (which only support GET and POST) to use
    other HTTP methods like PUT and DELETE by including a "_method" parameter.
    """
    async def dispatch(self, request: Request, call_next):
        # Only apply to POST form submissions
        if request.method == "POST":
            form_data = None
            
            # Get the content type
            content_type = request.headers.get("Content-Type", "")
            
            if "application/x-www-form-urlencoded" in content_type or "multipart/form-data" in content_type:
                # Parse form data, clone request scope
                form = await request.form()
                if "_method" in form:
                    method = form["_method"].upper()
                    if method in ["PUT", "PATCH", "DELETE"]:
                        # Create a new scope with modified method
                        request.scope["method"] = method
                        
        # Continue with the modified request
        response = await call_next(request)
        return response
