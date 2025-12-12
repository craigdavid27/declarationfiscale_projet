from django.urls import path
from .views import *

app_name = 'comptables'

urlpatterns = [
    path('<int:idmembre>/mon-espace/', mon_espace_view, name='mon_espace'),
    path('<int:idmembre>/mes-clients/', gestion_clients_view, name='gestion_clients'),
    path('<int:idmembre>/declarations/', suivi_declaration_view, name='suivi_declaration'),
    path('<int:idmembre>/calendrier/', calendrier_view, name='calendrier'),
]