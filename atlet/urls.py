from django.urls import path
from atlet.views import *

app_name = 'atlet'

urlpatterns = [
    path('form-kualifikasi', form_kualifikasi, name='form_kualifikasi'),
    path('pertanyaan-kualifikasi', pertanyaan_kualifikasi,
         name='pertanyaan_kualifikasi'),
    path('daftar-event/pilih-stadium', pilih_stadium, name='pilih_stadium'),
    path('daftar-event/pilih-event', pilih_event, name='pilih_event'),
    path('daftar-event/pilih-kategori', pilih_kategori, name='pilih_kategori'),
    path('daftar-atlet', daftar_atlet, name='daftar_atlet'),
    path('daftar-atlet/list-atlet', list_atlet, name='list_atlet'),
    path('daftar-sponsor', daftar_sponsor, name='daftar_sponsor'),
    path('enrolled-event', enrolled_event, name='enrolled_event'),
    path('list-event', list_event, name='list_event'),
    path("sponsor", get_all_sponsor, name="get_all_sponsor"),
    path('enrolled-partai-event', enrolled_partai_event,
         name='enrolled_partai_event'),
]
