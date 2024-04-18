from django.urls import path
from .views import Registrarse
from django.contrib.auth import views as auth_views
from usuarios.views import logout_view


urlpatterns = [
    
    
    path('registro/', Registrarse.as_view(), name="registro"),
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
  
]