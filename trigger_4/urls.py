from django.urls import path
from trigger_4.views import *

app_name = 'trigger_4'

urlpatterns = [
    path('daftar-event/', pilih_stadium, name='pilih_stadium'),
    path('daftar-event/stadium/<str:nama_stadium>/', pilih_event, name='pilih_event'),
    path('daftar-event/<str:nama_event>/<int:tahun_event>/', pilih_kategori, name='pilih_kategori'),
]