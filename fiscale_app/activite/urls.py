from django.urls import path
from .views import DeclarationView

app_name = "activites"

urlpatterns = [
    path('<int:idclient>/mes-declarations/', DeclarationView().liste_declaration, name='mes_declarations'),
]