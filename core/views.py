from django.http import JsonResponse
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def api_root(request):
    """API root endpoint that lists available endpoints."""
    return JsonResponse({
        "message": "Vibe Task Manager API",
        "version": "1.0",
        "endpoints": {
            "admin": "/admin/",
            "api_root": "/api/",
            "auth": {
                "login": "/api/auth/token/",
                "refresh": "/api/auth/token/refresh/",
                "register": "/api/auth/register/",
            },
            "resources": {
                "projects": "/api/projects/",
                "tasks": "/api/tasks/",
                "tags": "/api/tags/",
                "profile": "/api/profile/",
            },
        },
        "frontend": "http://localhost:5173",
    })
