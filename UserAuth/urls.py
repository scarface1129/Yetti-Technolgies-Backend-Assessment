from django.urls import path
# from . import views
from .views import *


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', login_user, name='login'),
    path('register/', register_user, name='register'),
    path('logout/', logout_view, name='logout'),
]