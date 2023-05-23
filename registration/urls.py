from django.urls import path
from registration.views import *

app_name = 'registration'

urlpatterns = [
    path('', show_registration, name='reg'),
    path('atlet', show_registration_atlet, name='reg_atlet'),
    path('pelatih', show_registration_pelatih, name='reg_pelatih'),
    path('umpire', show_registration_umpire, name='reg_umpire'),
]