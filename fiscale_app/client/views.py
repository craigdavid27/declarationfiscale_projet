from django.shortcuts import render, get_object_or_404
from .models import Client, Particulier, Independant
from activite.models import DeclarationFiscale, Depense, Revenu, TypeDepense, TypeRevenu
from django.shortcuts import redirect

# Create your views here.

class ClientDashboardView:

    def dashboard(self, request, idclient: int):
        # Basic session gate: allow if logged client matches or staff logged
        session_client_id = request.session.get("client_id")
        session_membre_id = request.session.get("membre_id")
        if not session_membre_id and session_client_id != idclient:
            return redirect("login")
        # Load client and related address + city
        client = get_object_or_404(Client.objects.select_related("adresse__ville"), pk=idclient)

        # Determine type: Particulier or Independant
        particulier = Particulier.objects.filter(client=client).first()
        independant = Independant.objects.filter(client_idclient=client).first()
        is_particulier = particulier is not None
        is_independant = independant is not None

        # Recent fiscal declarations, revenues, expenses
        declarations = (DeclarationFiscale.objects
                        .select_related("type_impot")
                        .filter(client=client)
                        .order_by('-annee')[:5])
        revenus = (Revenu.objects
                   .select_related("type_revenu")
                   .filter(client=client)
                   .order_by('-annee_de_perception')[:5])
        depenses = (Depense.objects
                    .select_related("type_depense")
                    .filter(client=client)
                    .order_by('-annee_depense')[:5])

        context = {
            "title": "Espace Client",
            "client": client,
            "is_particulier": is_particulier,
            "is_independant": is_independant,
            "particulier": particulier,
            "independant": independant,
            "declarations": declarations,
            "revenus": revenus,
            "depenses": depenses,
        }

        # Choose template based on client type
        if is_particulier:
            template = 'client/particulier/particulier.html'
        elif is_independant:
            template = 'client/independant/independant.html'
        else:
            template = 'login.html' # Fallback, should not happen

        return render(request, template, context=context)
    
def type_de_client(client_obj: Client):
        particulier = Particulier.objects.filter(client=client_obj).first()
        independant = Independant.objects.filter(client_idclient=client_obj).first()
        if particulier:
            return "Particulier"
        elif independant:
            return "Independant"
        else:
            return "Client"

class RevenuView:
        
    def liste_revenus(self, request, idclient: int):
        # Basic session gate: allow if logged client matches or staff logged
        session_client_id = request.session.get("client_id")
        session_membre_id = request.session.get("membre_id")
        if not session_membre_id and session_client_id != idclient:
            return redirect("login")
        # Load client
        client = get_object_or_404(Client, pk=idclient)

        # Load revenues
        revenus = (Revenu.objects
                    .select_related("type_revenu")
                    .filter(client=client)
                    .order_by('-annee_de_perception'))

        context = {
            "title": "Mes revenus",
            "client": client,
            "revenus": revenus,
            "client_type": type_de_client(client),
        }

        return render(request, 'client/revenus_liste.html', context=context)
    
    def ajouter_revenu(self, request, idclient: int):
        # Basic session gate: allow if logged client matches or staff logged
        session_client_id = request.session.get("client_id")
        session_membre_id = request.session.get("membre_id")
        if not session_membre_id and session_client_id != idclient:
            return redirect("login")
        # Load client
        client = get_object_or_404(Client, pk=idclient)

        # liste des types de revenus pour le formulaire
        type_revenus = TypeRevenu.objects.all()

        errors = []
        initial = {
            "montant": "",
            "annee_de_perception": "",
            "type_revenu": "",
        }

        if request.method == "POST":
            montant_raw = request.POST.get("montant", "").strip()
            annee_raw = request.POST.get("annee_de_perception", "").strip()
            type_revenu_raw = request.POST.get("type_revenu", "").strip()

            initial["montant"] = montant_raw
            initial["annee_de_perception"] = annee_raw
            initial["type_revenu"] = type_revenu_raw

            if not montant_raw:
                errors.append("Le montant est obligatoire.")
            if not annee_raw:
                errors.append("L'année de perception est obligatoire.")
            if not type_revenu_raw:
                errors.append("Le type de revenu est obligatoire.")

            montant = None
            annee = None

            # --- new: parse numeric values and create revenu if valid ---
            if not errors:
                try:
                    montant = float(montant_raw.replace(",", "."))
                except ValueError:
                    errors.append("Le montant doit être un nombre.")

                try:
                    annee = int(annee_raw)
                except ValueError:
                    errors.append("L'année de perception doit être un nombre entier.")

            if not errors:
                Revenu.objects.create(
                    client=client,
                    montant=montant,
                    annee_de_perception=annee,
                    type_revenu_id=type_revenu_raw,
                )
                return redirect(f"/clients/{idclient}/mes-revenus/")
            # --- end new code ---

        # Always return an HttpResponse (redirect to the revenus list)
        return render(request, f"client/revenus_form.html", context={"errors": errors, "initial": initial, "client": client, "type_revenus": type_revenus})
    

class DepenseView:
    def liste_depenses(self, request, idclient: int):
        # Basic session gate: allow if logged client matches or staff logged
        session_client_id = request.session.get("client_id")
        session_membre_id = request.session.get("membre_id")
        if not session_membre_id and session_client_id != idclient:
            return redirect("login")
        # Load client
        client = get_object_or_404(Client, pk=idclient)

        # Load depenses
        depenses = (Depense.objects
                    .select_related("type_depense")
                    .filter(client=client)
                    .order_by('-annee_depense'))

        context = {
            "title": "Mes dépenses",
            "client": client,
            "depenses": depenses,
            "client_type": type_de_client(client),
        }

        return render(request, 'client/depenses_liste.html', context=context)
    
    def ajouter_depense(self, request, idclient: int):
        # Basic session gate: allow if logged client matches or staff logged
        session_client_id = request.session.get("client_id")
        session_membre_id = request.session.get("membre_id")
        if not session_membre_id and session_client_id != idclient:
            return redirect("login")
        # Load client
        client = get_object_or_404(Client, pk=idclient)

        # liste des types de depenses pour le formulaire
        type_depenses = TypeDepense.objects.all()

        errors = []
        initial = {
            "montant": "",
            "annee_depense": "",
            "type_depense": "",
        }

        if request.method == "POST":
            montant_raw = request.POST.get("montant", "").strip()
            annee_raw = request.POST.get("annee_depense", "").strip()
            type_depense_raw = request.POST.get("type_depense", "").strip()

            initial["montant"] = montant_raw
            initial["annee_depense"] = annee_raw
            initial["type_depense"] = type_depense_raw

            if not montant_raw:
                errors.append("Le montant est obligatoire.")
            if not annee_raw:
                errors.append("L'année de la dépense est obligatoire.")
            if not type_depense_raw:
                errors.append("Le type de dépense est obligatoire.")

            montant = None
            annee = None

            if not errors:
                try:
                    montant = float(montant_raw.replace(",", "."))
                except ValueError:
                    errors.append("Le montant doit être un nombre.")

                try:
                    annee = int(annee_raw)
                except ValueError:
                    errors.append("L'année de la dépense doit être un nombre entier.")

            if not errors:
                Depense.objects.create(
                    client=client,
                    montant=montant,
                    annee_depense=annee,
                    type_depense_id=type_depense_raw,
                )
                return redirect(f"/clients/{idclient}/mes-depenses/")

        return render(request, f"client/depenses_form.html", context={"errors": errors, "initial": initial, "client": client, "type_depenses": type_depenses})
    
class ClientDetailView:
    def mon_profil(self, request, idclient: int):
        # Basic session gate: allow if logged client matches or staff logged
        session_client_id = request.session.get("client_id")
        session_membre_id = request.session.get("membre_id")
        if not session_membre_id and session_client_id != idclient:
            return redirect("login")
        # Load client and related address + city
        
        if request.method == "POST":
            # Process form submission to update client info
            client = get_object_or_404(Client.objects.select_related("adresse__ville"), pk=idclient)

            nom = request.POST.get("nom", "").strip()
            prenom = request.POST.get("prenom", "").strip()
            registre_national = request.POST.get("registre_national", "").strip()   
            telephone = request.POST.get("telephone", "").strip()
            iban = request.POST.get("iban", "").strip()

            # Simple validation (can be expanded)
            errors = []
            if not nom:
                errors.append("Le nom est obligatoire.")
            if not prenom:
                errors.append("Le prénom est obligatoire.")
            if not registre_national:
                errors.append("Le numéro de registre national est obligatoire.")
            if not telephone:
                errors.append("Le téléphone est obligatoire.")
            if not iban:
                errors.append("L'IBAN est obligatoire.")

            if not errors:
                # Update client info
                client.nom = nom
                client.prenom = prenom
                client.telephone = telephone
                client.iban = iban
                client.save()

                return redirect(f"/clients/{idclient}/mon-profil/")

            # If errors, re-render the form with errors
            context = {
                "title": "Mes informations personnelles",
                "client": client,
                "errors": errors,
            }
            return render(request, 'client/mon_profil.html', context=context)
        
        client = get_object_or_404(Client.objects.select_related("adresse__ville"), pk=idclient)

        # récupérer le registre national si le client est un particulier
        particulier = Particulier.objects.filter(client=client).first()
        if particulier:
            client.registre_national = particulier.registre_national

        context = {
            "title": "Mes informations personnelles",
            "client": client,
        }

        return render(request, 'client/mon_profil.html', context=context)
    
    def mon_adresse(self, request, idclient: int):
        # Basic session gate: allow if logged client matches or staff logged
        session_client_id = request.session.get("client_id")
        session_membre_id = request.session.get("membre_id")
        if not session_membre_id and session_client_id != idclient:
            return redirect("login")
        # Load client and related address + city
        client = get_object_or_404(Client.objects.select_related("adresse__ville"), pk=idclient)

        context = {
            "title": "Mon adresse",
            "client": client,
        }

        return render(request, 'client/coordonnees.html', context=context)
    
    def connexion(self, request, idclient: int):
        # Basic session gate: allow if logged client matches or staff logged
        session_client_id = request.session.get("client_id")
        session_membre_id = request.session.get("membre_id")
        if not session_membre_id and session_client_id != idclient:
            return redirect("login")
        # Load client
        client = get_object_or_404(Client, pk=idclient)

        context = {
            "title": "Mes informations de connexion",
            "client": client,
        }

        return render(request, 'client/mon_profil_connexion.html', context=context)
    
    def mes_charges(self, request, idclient: int):
        # Basic session gate: allow if logged client matches or staff logged
        session_client_id = request.session.get("client_id")
        session_membre_id = request.session.get("membre_id")
        if not session_membre_id and session_client_id != idclient:
            return redirect("login")
        # Load client
        client = get_object_or_404(Client, pk=idclient)

        context = {
            "title": "Mes personnes à charge",
            "client": client,
        }

        return render(request, 'client/personnes_a_charge.html', context=context)