from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveAPIView
from .serializers import UserSerializer
from .models import User


class RetrieveUser(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_url_kwarg = 'user_id'
