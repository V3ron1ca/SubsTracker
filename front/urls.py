from django.urls import path
from front.views import front_view

urlpatterns = [
    path("", front_view)
]
