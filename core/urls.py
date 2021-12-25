from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('signup/', views.UserRegistrationView.as_view(), name='signup'),
    path('user_signup/', views.signup, name='user_signup'),
    path('user_login/', views.login_view, name='user_login'),
]
