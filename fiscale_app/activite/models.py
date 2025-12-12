from django.db import models
from client.models import Client

# Create your models here.

class TypeImpot(models.Model):
    idtype_impot = models.AutoField(db_column='idType_impot', primary_key=True)  # Field name made lowercase.
    denomination = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'type_impot'

class DeclarationFiscale(models.Model):
    iddeclaration_fiscale = models.AutoField(db_column='idDeclaration_fiscale', primary_key=True)  # Field name made lowercase.
    annee = models.IntegerField()
    lien = models.CharField(max_length=255, blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, db_column='idclient')  # Field name made lowercase.
    type_impot = models.ForeignKey(TypeImpot, on_delete=models.PROTECT, db_column='idtype_impot')  # Field name made lowercase.
    STATUS_CHOICES = [
        ('en_attente', 'En attente'),
        ('en_cours', 'En cours'),
        ('soumise', 'Soumise'),
        ('à_reviser', 'À réviser'),
        ('valide', 'Validée'),
    ]
    statut = models.CharField(max_length=20, choices=STATUS_CHOICES)

    class Meta:
        db_table = 'declaration_fiscale'

class TypeDepense(models.Model):
    codetype = models.IntegerField(db_column='codeType', primary_key=True)  # Field name made lowercase.
    nom = models.CharField(max_length=100)

    class Meta:
        db_table = 'type_depense'

class Depense(models.Model):
    iddepense = models.AutoField(db_column='idDepense', primary_key=True)  # Field name made lowercase.
    montant = models.IntegerField()
    annee_depense = models.IntegerField()
    client = models.ForeignKey(Client, on_delete=models.PROTECT, db_column='idclient')  # Field name made lowercase.
    type_depense = models.ForeignKey(TypeDepense, on_delete=models.PROTECT, db_column='code_type_depense')  # Field name made lowercase.

    class Meta:
        db_table = 'depense'

class DocumentDepense(models.Model):
    iddocument_depense = models.AutoField(db_column='idDocument_depense', primary_key=True)  # Field name made lowercase.
    nom = models.CharField(max_length=100, blank=True, null=True)
    lien = models.URLField(max_length=255)
    depense = models.ForeignKey(Depense, on_delete=models.CASCADE, db_column='iddepense')  # Field name made lowercase.

    class Meta:
        db_table = 'document_depense'

class TypeRevenu(models.Model):
    code_type_revenu = models.IntegerField(db_column='code_Type_revenu', primary_key=True)  # Field name made lowercase.
    nom = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'type_revenu'

class Revenu(models.Model):
    idrevenu = models.AutoField(db_column='idRevenu', primary_key=True)  # Field name made lowercase.
    montant = models.IntegerField()
    annee_de_perception = models.IntegerField()
    client = models.ForeignKey(Client, on_delete=models.PROTECT, db_column='idclient')  # Field name made lowercase.
    type_revenu = models.ForeignKey(TypeRevenu, on_delete=models.PROTECT, db_column='code_type_revenu')  # Field name made lowercase.

    class Meta:
        db_table = 'revenu'

class DocumentRevenu(models.Model):
    iddocument_revenu = models.AutoField(db_column='idDocument_revenu', primary_key=True)  # Field name made lowercase.
    nom = models.CharField(max_length=100, blank=True, null=True)
    lien = models.URLField(max_length=255)
    revenu = models.ForeignKey(Revenu, on_delete=models.CASCADE, db_column='idrevenu')  # Field name made lowercase.

    class Meta:
        db_table = 'document_revenu'