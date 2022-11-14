from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods, require_GET

from .models import User
# Create your views here.


@require_GET  # 12
def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return JsonResponse({
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'birth_date': user.birth_date,
        'status': user.status,
        'bio': user.bio,
        'last_login': user.last_login,
    })
