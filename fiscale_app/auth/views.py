from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from client.models import Client
from comptable.models import MembreCabinet


@require_http_methods(["GET","POST"])
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()

        # Try comptable first
        membre = MembreCabinet.objects.filter(email=email, mot_de_passe=password).first()
        if membre:
            request.session["membre_id"] = membre.idmembre
            return redirect(reverse('comptables:mon_espace', kwargs={'idmembre': membre.idmembre}))

        # Then client
        client = Client.objects.filter(email=email, mot_de_passe=password).first()
        if client:
            request.session["client_id"] = client.idclient
            return redirect(reverse('clients:mon_espace', kwargs={'idclient': client.idclient}))

        messages.error(request, "Identifiants invalides.")

    return render(request, "login.html")

@require_http_methods(["GET"])
def home_view(request):
    return render(request, "index.html")