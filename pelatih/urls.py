from pelatih.views import *
from django.urls import path

app_name = 'pelatih'

urlpatterns = [
    path('pelatihan', pelatihan, name='pelatihan'),
    path('list_atlet_pelatih', list_atlet_pelatih, name='list_atlet_pelatih'),
]
