from django.urls import path
from trigger_1.views import *

app_name = 'trigger_!'

urlpatterns = [
    path('login/', login, name='login'),
]