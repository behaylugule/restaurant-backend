from django.urls import include, path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('me/', views.me_view, name='me'),
    path('update-profile/<int:pk>/', views.UpdateUser.as_view(), name='update-profile'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('password-reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('users/', views.RetrieveUser.as_view(), name='get_user'),
] 