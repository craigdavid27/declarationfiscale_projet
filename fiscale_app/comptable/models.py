from django.db import models
from activite.models import DeclarationFiscale

# Create your models here.

class Poste(models.Model):
    idposte = models.AutoField(db_column='idPoste', primary_key=True)  # Field name made lowercase.
    poste = models.CharField(max_length=45)

    class Meta:
        db_table = 'poste'

class MembreCabinet(models.Model):
    idmembre = models.AutoField(db_column='idMembre', primary_key=True)  # Field name made lowercase.
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    mot_de_passe = models.CharField(max_length=255, db_column='mot de passe')
    poste = models.ForeignKey('Poste', on_delete=models.PROTECT, db_column='idposte')  # Field name made lowercase.

    class Meta:
        db_table = 'membre_cabinet'

class AttributionDeclarationFiscaleAMembre(models.Model):
    membre_cabinet = models.ForeignKey(MembreCabinet, on_delete=models.CASCADE, db_column='Membre_cabinet')  # Field name made lowercase.
    declaration_fiscale = models.ForeignKey(DeclarationFiscale, on_delete=models.CASCADE, db_column='Declaration_fiscale')  # Field name made lowercase.

    class Meta:
        db_table = 'attribution_declaration_fiscale_a_membre'
        unique_together = [['membre_cabinet', 'declaration_fiscale']]
        constraints = [
            models.UniqueConstraint(fields=['membre_cabinet', 'declaration_fiscale'], name='unique_attribution')
        ]