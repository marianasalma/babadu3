from pelatih.views import *
from django.urls import path

app_name = 'pelatih'

urlpatterns = [
    path('pelatihan', pelatihan, name='pelatihan'),

]
