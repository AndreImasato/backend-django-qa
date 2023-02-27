from django.urls import path
#? from rest_framework import renderers

from .views import LoginView, UserView


user_list = UserView.as_view({
    'get': 'list',
    'post': 'create'
})

user_detail = UserView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('login/', LoginView.as_view(), name="user_login"),
    path(route='users/', view=user_list, name='users-list'),
    path(route='users/<public_id>/', view=user_detail, name='users-detail'),
]
