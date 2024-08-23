from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello_world, name='hello-world'),
    path('user/<int:id>/', views.get_user, name='get_user'),
    path('user/create', views.create_user, name='create_user'),
    path('auth/sign-in', views.sign_in, name='sign_in'),
]