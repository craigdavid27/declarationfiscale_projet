from django.shortcuts import render, get_object_or_404

from client.models import Client
from .models import DeclarationFiscale, Depense, Revenu


def _get_client_tax_type(client: Client) -> str:
    """Retourne le type d'impôt applicable pour un client.

    - ISOC : client avec une activité d'indépendant (simplification)
    - IPP : client particulier (par défaut)
    """

    # Si le client a au moins un enregistrement Independant lié
    if hasattr(client, "independants") and client.independants.exists():
        return "ISOC"

    return "IPP"


def _compute_tax_amount(tax_type: str, taxable_income: float) -> tuple[float, float]:
    """Calcule un montant d'impôt simple selon le type d'impôt.

    Retourne (montant_impot, taux_applique).
    Cette logique est volontairement simplifiée pour l'affichage.
    """

    taxable_income = max(taxable_income, 0)

    if tax_type == "ISOC":
        rate = 0.25  # 25 % pour ISOC (simplifié)
    else:
        rate = 0.40  # 40 % pour IPP (simplifié)

    tax_amount = taxable_income * rate
    return tax_amount, rate


class DeclarationView:
    def liste_declaration(self, request, idclient):
        client = get_object_or_404(Client, pk=idclient)

        declarations = (
            DeclarationFiscale.objects.filter(client=client)
            .select_related("type_impot")
            .order_by("-annee")
        )

        tax_type = _get_client_tax_type(client)

        declarations_data = []
        for declaration in declarations:
            # Somme des revenus et dépenses pour l'année fiscale de la déclaration
            revenus_qs = Revenu.objects.filter(
                client=client, annee_de_perception=declaration.annee
            )
            depenses_qs = Depense.objects.filter(
                client=client, annee_depense=declaration.annee
            )

            total_revenus = sum(r.montant for r in revenus_qs)
            total_depenses = sum(d.montant for d in depenses_qs)
            base_imposable = total_revenus - total_depenses

            tax_amount, rate = _compute_tax_amount(tax_type, base_imposable)

            declarations_data.append(
                {
                    "instance": declaration,
                    "annee": declaration.annee,
                    "label": f"Revenus annuels {declaration.annee}",
                    "statut": declaration.statut,
                    "statut_label": declaration.get_statut_display(),
                    "total_revenus": total_revenus,
                    "total_depenses": total_depenses,
                    "base_imposable": base_imposable,
                    "tax_type": tax_type,
                    "tax_amount": tax_amount,
                    "tax_rate": rate * 100,  # en pourcentage
                }
            )

        context = {
            "client": client,
            "tax_type": tax_type,
            "declarations_data": declarations_data,
        }

        return render(request, "activite/mes_declarations.html", context)