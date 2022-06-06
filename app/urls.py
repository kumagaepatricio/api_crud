from django.urls import path

from .views import UserView, TestView

urlpatterns = [
    path(r'users/<uuid:uuid>', UserView.as_view()),
    path('users/', UserView.as_view()),
    path('test/', TestView.as_view()),
]