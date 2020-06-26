from django.urls import path,re_path
from .views import manual,log_out

urlpatterns = [
    path('login/',manual),
    path('logout/',log_out),
]
