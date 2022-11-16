from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveAPIView
from .serializers import UserSerializer
from .models import User


class RetrieveUser(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_url_kwarg = 'user_id'

    '''def user_detail(request, user_id):  # 12
        user = get_object_or_404(User, id=user_id)
        return JsonResponse({
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'birth_date': user.birth_date,
            'status': user.status,
            'bio': user.bio,
            'last_login': user.last_login,
        })'''
