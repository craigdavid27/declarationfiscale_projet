from django.urls import path
from .views import ClientDashboardView, RevenuView, DepenseView, ClientDetailView

app_name = 'clients'

urlpatterns = [
    # Pour tous les clients
    path('<int:idclient>/mon-espace/', ClientDashboardView().dashboard, name='mon_espace'),
    path('<int:idclient>/mes-revenus/', RevenuView().liste_revenus, name='mes_revenus'),
    path('<int:idclient>/mes-revenus/new/', RevenuView().ajouter_revenu, name='new_revenu'),
    path('<int:idclient>/mes-depenses/', DepenseView().liste_depenses, name='mes_depenses'),
    path('<int:idclient>/mes-depenses/new/', DepenseView().ajouter_depense, name='new_depense'),
    path('<int:idclient>/mes-infos-personnelles/', ClientDetailView().mon_profil, name='mon_profil'),
    path('<int:idclient>/mes-infos-personnelles/mon-adresse/', ClientDetailView().mon_adresse, name='mon_adresse'),
    path('<int:idclient>/mes-infos-personnelles/connexion/', ClientDetailView().connexion, name='connexion'),
    path('<int:idclient>/mes-infos-personnelles/mes-charges/', ClientDetailView().mes_charges, name='mes_charges'),

    # Pour les clients indépendants
    # path('<int:idclient>/mon-activite-professionnelle/', IndependantView().infos_pro, name='infos_pro'),
]