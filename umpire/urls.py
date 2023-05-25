from django.urls import path
from umpire.views import show_semi
from umpire.views import show_final
from umpire.views import show_perempat
from umpire.views import *

app_name = 'umpire'

urlpatterns = [
    path('perempat', show_perempat, name='show_perempat'),
    path('semi', show_semi, name='show_semi'),
    path('final', show_final, name='show_final'),
    path('mulai/<str:nama_event>/<str:jenis_partai>', show_mulai, name='show_mulai'),
    path('hasil_pertandingan/<str:nama_event>/<str:jenis_partai>', hasil_pertandingan, name='hasil_pertandingan'),
    path('list-event', list_event, name='list_event'),
    path('list_daftar_atlet', list_daftar_atlet, name='list_daftar_atlet'),
    path('partai_kompetisi_event', partai_kompetisi_event, name='partai_kompetisi_event'),
]
