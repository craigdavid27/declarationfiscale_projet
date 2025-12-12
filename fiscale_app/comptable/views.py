from django.shortcuts import render
from activite.models import DeclarationFiscale
from client.models import Client, Particulier, Independant
from comptable.models import AttributionDeclarationFiscaleAMembre, MembreCabinet

def mon_espace_view(request, idmembre):
	membre_id = request.session.get("membre_id")
	if not membre_id or membre_id != idmembre:
		return render(request, "error.html", {"message": "Accès non autorisé."})

	# Fetch member's name from session
	membre = MembreCabinet.objects.filter(idmembre=idmembre).first()
	# Get total number of clients assigned to this member
	declarations_ids = AttributionDeclarationFiscaleAMembre.objects.filter(
		membre_cabinet_id=idmembre
	).values_list('declaration_fiscale_id', flat=True)
	
	# Get unique clients from declarations
	client_ids = DeclarationFiscale.objects.filter(
		iddeclaration_fiscale__in=declarations_ids
	).values_list('client_id', flat=True).distinct()
	
	total_clients = len(set(client_ids))
	
	# Get declarations in progress (statut: en_cours)
	declarations_en_cours = DeclarationFiscale.objects.filter(
		iddeclaration_fiscale__in=declarations_ids,
		statut='en_cours'
	).count()
	
	# Get declarations to submit (statut: en_attente or à_reviser)
	declarations_a_soumettre = DeclarationFiscale.objects.filter(
		iddeclaration_fiscale__in=declarations_ids,
		statut__in=['en_attente', 'à_reviser']
	).count()
	
	# Get deadlines for this week (this is a placeholder, would need a deadline field in the model)
	# For now, we'll count declarations that need attention
	echeances_cette_semaine = 8  # Placeholder value as shown in screenshot
	
	# Get recent clients with their declarations
	recent_clients = []
	
	# Get all clients with their latest declaration
	clients = Client.objects.filter(idclient__in=client_ids).prefetch_related(
		'particuliers', 'independants'
	)
	
	for client in clients:
		# Get the latest declaration for this client
		latest_declaration = DeclarationFiscale.objects.filter(
			client=client,
			iddeclaration_fiscale__in=declarations_ids
		).order_by('-iddeclaration_fiscale').first()
		
		if latest_declaration:
			# Determine client type
			is_particulier = Particulier.objects.filter(client=client).exists()
			is_independant = Independant.objects.filter(client_idclient=client).exists()
			
			if is_particulier:
				client_type = "Particulier"
			elif is_independant:
				client_type = "Indépendant"
			else:
				client_type = "Client"
			
			# Map status to French labels
			statut_map = {
				'en_cours': 'En cours',
				'en_attente': 'En attente',
				'soumise': 'Complétée',
				'à_reviser': 'À soumettre',
				'valide': 'Complétée'
			}
			
			# Calculate progression based on status
			progression_map = {
				'en_attente': 45,
				'en_cours': 65,
				'à_reviser': 90,
				'soumise': 100,
				'valide': 100
			}
			
			statut_display = statut_map.get(latest_declaration.statut, latest_declaration.statut)
			progression = progression_map.get(latest_declaration.statut, 0)
			
			# Get initials
			initials = f"{client.prenom[0]}{client.nom[0]}".upper() if client.prenom and client.nom else "??"
			
			# Calculate last activity (placeholder - would need a timestamp field)
			derniere_activite = "Il y a 2h"  # Placeholder
			
			recent_clients.append({
				'id': client.idclient,
				'nom': f"{client.prenom} {client.nom}",
				'initials': initials,
				'type': client_type,
				'statut': statut_display,
				'progression': progression,
				'derniere_activite': derniere_activite,
				'declaration_id': latest_declaration.iddeclaration_fiscale
			})
	
	# Sort by most recent activity (for now just take first few)
	recent_clients = recent_clients[:4]  # Show only 4 recent clients as in screenshot

	context = {
		"id": idmembre,
		"nom" : membre.nom,
		"poste": membre.poste.poste,
		"prenom": membre.prenom,
		"total_clients": total_clients,
		"declarations_en_cours": declarations_en_cours,
		"declarations_a_soumettre": declarations_a_soumettre,
		"echeances_cette_semaine": echeances_cette_semaine,
		"recent_clients": recent_clients,
	}
	return render(request, "comptable/comptable.html", context)

def gestion_clients_view(request, idmembre):
	membre_id = request.session.get("membre_id")
	print(membre_id)
	if not membre_id or membre_id != idmembre:
		return render(request, "error.html", {"message": "Accès non autorisé."})
	
	# Fetch member's name from session
	membre = MembreCabinet.objects.filter(idmembre=idmembre).first()

	clients_liste = Client.objects.filter(
		declarationfiscale__attributiondeclarationfiscaleamembre__membre_cabinet_id=idmembre
	).distinct()
	
	context = {
		"id": idmembre,
		"nom" : membre.nom,
		"prenom": membre.prenom,
		"poste": membre.poste.poste,
		"total_clients": clients_liste.count(),
		"total_independants": Independant.objects.filter(client_idclient__in=clients_liste).count(),
		"total_particuliers": Particulier.objects.filter(client__in=clients_liste).count(),
		"clients": clients_liste,
	}
	return render(request, "comptable/gestion_clients.html", context)

def suivi_declaration_view(request, idmembre):
	membre_id = request.session.get("membre_id")
	if not membre_id or membre_id != idmembre:
		return render(request, "error.html", {"message": "Accès non autorisé."})
	
	# Fetch member's name from session
	membre = MembreCabinet.objects.filter(idmembre=idmembre).first()
	
	#récupérer toutes les déclarations fiscales associées à ce membre ainsi les données des clients associés
	declarations_ids = AttributionDeclarationFiscaleAMembre.objects.filter(
		membre_cabinet_id=idmembre
	).values_list('declaration_fiscale_id', flat=True)

	context = {
		"nom" : membre.nom,
		"prenom": membre.prenom,
		"id": idmembre,
		"poste": membre.poste.poste,
		"declarations": DeclarationFiscale.objects.filter(iddeclaration_fiscale__in=declarations_ids),
	}
	return render(request, "comptable/suivi_declarations.html", context)

def calendrier_view(request, idmembre):
	membre_id = request.session.get("membre_id")
	if not membre_id or membre_id != idmembre:
		return render(request, "error.html", {"message": "Accès non autorisé."})
	
	# Fetch member's name from session
	membre = MembreCabinet.objects.filter(idmembre=idmembre).first()
	
	context = {
		"nom" : membre.nom,
		"prenom": membre.prenom,
		"id": idmembre,
		"poste": membre.poste.poste,
	}
	return render(request, "comptable/calendrier_echeances.html", context)
