from django.urls import path
from umpire.views import show_semi
from umpire.views import show_final
from umpire.views import show_hasil
from umpire.views import show_perempat
from umpire.views import *

app_name = 'umpire'

urlpatterns = [
    path('perempat', show_perempat, name='show_perempat'),
    path('semi', show_semi, name='show_semi'),
    path('final', show_final, name='show_final'),
    path('hasil', show_hasil, name='show_hasil'),
    path('list-event', list_event, name='list_event'),
]
