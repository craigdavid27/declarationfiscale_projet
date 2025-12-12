from django.shortcuts import render, get_object_or_404

from client.models import Client, PersonneACharge
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
    """Ancienne fonction de calcul simple (taux fixe).

    Conservée pour compatibilité éventuelle mais non utilisée pour
    les nouveaux calculs ISOC/IPP détaillés.
    """

    taxable_income = max(taxable_income, 0)

    if tax_type == "ISOC":
        rate = 0.25
    else:
        rate = 0.40

    tax_amount = taxable_income * rate
    return tax_amount, rate


def _compute_isoc_tax(benefice: float) -> dict:
    """Calcule l'ISOC belge (impôt des sociétés) de façon simplifiée.

    Règles applicables :
    1. Bénéfice imposable = revenus_totaux - depenses_deductibles
    2. Si bénéfice <= 100 000 €, ISOC = 20 % du bénéfice
    3. Si bénéfice > 100 000 € :
       ISOC = (20 % de 100 000 €) + 25 % du montant au‑delà de 100 000 €
    4. Si le bénéfice est négatif ou nul, l'ISOC dû est 0.

    Retourne un dictionnaire contenant :
    - tax_amount     : montant total de l'ISOC dû
    - effective_rate : taux moyen effectif appliqué (en % du bénéfice)
    - brackets       : détail par tranche
    """

    benefice = max(float(benefice), 0.0)

    if benefice <= 0:
        return {"tax_amount": 0.0, "effective_rate": 0.0, "brackets": []}

    seuil = 100_000.0
    taux_bas = 20.0  # %
    taux_haut = 25.0  # %

    base_bas = min(benefice, seuil)
    base_haut = max(benefice - seuil, 0.0)

    impot_bas = base_bas * (taux_bas / 100.0)
    impot_haut = base_haut * (taux_haut / 100.0)

    tax_amount = impot_bas + impot_haut
    effective_rate = (tax_amount / benefice) * 100.0 if benefice > 0 else 0.0

    brackets: list[dict] = []
    if base_bas > 0:
        brackets.append(
            {
                "label": "Tranche jusqu'à 100 000 €",
                "base": base_bas,
                "rate": taux_bas,
                "tax": impot_bas,
            }
        )
    if base_haut > 0:
        brackets.append(
            {
                "label": "Au‑delà de 100 000 €",
                "base": base_haut,
                "rate": taux_haut,
                "tax": impot_haut,
            }
        )

    return {"tax_amount": tax_amount, "effective_rate": effective_rate, "brackets": brackets}


def _compute_ipp_tax(
    revenus_totaux: float,
    depenses_deductibles: float,
    nb_personnes_charge: int,
) -> dict:
    """Calcule un IPP belge *simplifié* pour un particulier.

    1. Revenu net imposable = revenus_totaux - depenses_deductibles
    2. Abattement pour personnes à charge = nb_personnes_charge * 1 650 €
    3. Revenu imposable final = revenu_net_imposable - abattement (ramené à 0)
    4. Barème progressif simplifié :
       - 25 % sur 0 à 15 200 €
       - 40 % sur 15 200 à 26 830 €
       - 45 % sur 26 830 à 46 440 €
       - 50 % au‑delà de 46 440 €

    Retourne un dictionnaire avec :
    - tax_amount      : montant total de l'IPP dû
    - effective_rate  : taux moyen effectif (en % du revenu imposable final)
    - taxable_income  : revenu imposable final après abattement
    - net_income      : revenu net imposable avant abattement
    - allowance       : montant total d'abattement
    - brackets        : détail par tranche
    """

    # Normalisation des entrées
    revenus_totaux = max(float(revenus_totaux), 0.0)
    depenses_deductibles = max(float(depenses_deductibles), 0.0)
    nb_personnes_charge = max(int(nb_personnes_charge), 0)

    # 1. Revenu net imposable
    revenu_net_imposable = max(revenus_totaux - depenses_deductibles, 0.0)

    # 2. Abattement pour personnes à charge
    allowance_per_person = 1650.0
    allowance = nb_personnes_charge * allowance_per_person

    # 3. Revenu imposable final
    revenu_imposable = max(revenu_net_imposable - allowance, 0.0)

    if revenu_imposable <= 0:
        return {
            "tax_amount": 0.0,
            "effective_rate": 0.0,
            "taxable_income": 0.0,
            "net_income": revenu_net_imposable,
            "allowance": allowance,
            "brackets": [],
        }

    # Seuils
    t1 = 15_200.0
    t2 = 26_830.0
    t3 = 46_440.0

    # Taux en pourcentage
    r1 = 25.0
    r2 = 40.0
    r3 = 45.0
    r4 = 50.0

    remaining = revenu_imposable
    total_tax = 0.0
    brackets: list[dict] = []

    # Tranche 1 : 0 -> 15 200 €
    base1 = min(remaining, t1)
    if base1 > 0:
        tax1 = base1 * (r1 / 100.0)
        total_tax += tax1
        remaining -= base1
        brackets.append({"label": "0 à 15 200 €", "base": base1, "rate": r1, "tax": tax1})

    # Tranche 2 : 15 200 -> 26 830 €
    if remaining > 0:
        span2 = t2 - t1
        base2 = min(remaining, span2)
        if base2 > 0:
            tax2 = base2 * (r2 / 100.0)
            total_tax += tax2
            remaining -= base2
            brackets.append(
                {
                    "label": "15 200 à 26 830 €",
                    "base": base2,
                    "rate": r2,
                    "tax": tax2,
                }
            )

    # Tranche 3 : 26 830 -> 46 440 €
    if remaining > 0:
        span3 = t3 - t2
        base3 = min(remaining, span3)
        if base3 > 0:
            tax3 = base3 * (r3 / 100.0)
            total_tax += tax3
            remaining -= base3
            brackets.append(
                {
                    "label": "26 830 à 46 440 €",
                    "base": base3,
                    "rate": r3,
                    "tax": tax3,
                }
            )

    # Tranche 4 : au‑delà de 46 440 €
    if remaining > 0:
        base4 = remaining
        tax4 = base4 * (r4 / 100.0)
        total_tax += tax4
        brackets.append({"label": "> 46 440 €", "base": base4, "rate": r4, "tax": tax4})

    effective_rate = (total_tax / revenu_imposable) * 100.0

    return {
        "tax_amount": total_tax,
        "effective_rate": effective_rate,
        "taxable_income": revenu_imposable,
        "net_income": revenu_net_imposable,
        "allowance": allowance,
        "brackets": brackets,
    }


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

            # Calcul de l'impôt en fonction du type de client
            if tax_type == "ISOC":
                isoc_data = _compute_isoc_tax(base_imposable)
                tax_amount = isoc_data["tax_amount"]
                tax_rate = isoc_data["effective_rate"]  # en pourcentage
                tax_brackets = isoc_data["brackets"]
            else:
                # IPP pour un particulier : prise en compte des personnes à charge
                nb_personnes_charge = PersonneACharge.objects.filter(client=client).count()
                ipp_data = _compute_ipp_tax(total_revenus, total_depenses, nb_personnes_charge)
                tax_amount = ipp_data["tax_amount"]
                tax_rate = ipp_data["effective_rate"]  # en pourcentage
                tax_brackets = ipp_data["brackets"]

            # Préparation du détail pour l'affichage
            revenus_details = [
                {
                    "type": getattr(revenu.type_revenu, "nom", "Revenu"),
                    "montant": revenu.montant,
                    "sign": "+",
                }
                for revenu in revenus_qs
            ]

            depenses_details = [
                {
                    "type": getattr(depense.type_depense, "nom", "Dépense"),
                    "montant": depense.montant,
                    "sign": "-",
                }
                for depense in depenses_qs
            ]

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
                    "tax_rate": tax_rate,
                    "tax_brackets": tax_brackets,
                    "revenus_details": revenus_details,
                    "depenses_details": depenses_details,
                }
            )

        context = {
            "client": client,
            "tax_type": tax_type,
            "declarations_data": declarations_data,
        }

        return render(request, "activite/mes_declarations.html", context)