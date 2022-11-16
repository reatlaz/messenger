from django.urls import path
from users.views import RetrieveUser

urlpatterns = [
    path('<int:user_id>/', RetrieveUser.as_view(), name='user_detail')
]
