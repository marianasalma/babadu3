from django.urls import path
<<<<<<< Updated upstream:landing_page/urls.py
from landing_page.views import *
=======
from kira.views import *
from . import views 
>>>>>>> Stashed changes:kira/urls.py

app_name = 'kira'

urlpatterns = [
    # path('login', login, name='login'),
    path('login/', login, name='login'),
    # path('', landing, name='landing'),
    # path("user_login",views.user_login,name='user_login'),
    # path("user_logout",views.user_logout,name='user_logout'),
]