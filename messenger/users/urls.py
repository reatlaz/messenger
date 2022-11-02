from django.urls import path
from users.views import user_detail

urlpatterns = [
    path('<int:user_id>/', user_detail, name='user_detail')
]
