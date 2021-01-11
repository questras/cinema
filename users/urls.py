from django.urls import path
from django.contrib.auth import views as auth_views

from .views import SignUpView, ProfileView

urlpatterns = [
    path('login/',
         auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name='auth/login.html'),
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
