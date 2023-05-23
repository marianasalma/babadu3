from django.urls import path
from trigger_1.views import *

app_name = 'trigger_1'

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
]