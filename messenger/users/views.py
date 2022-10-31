from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

# Create your views here.

def user_detail(request, user_id):
    return  JsonResponse({'user_info': 'You'})
