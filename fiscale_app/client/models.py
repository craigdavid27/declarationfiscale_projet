from django.db import models


class Ville(models.Model):
    idville = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    code_postal = models.CharField(db_column='code postal', max_length=10)  # Field renamed to remove unsuitable characters.
    
    class Meta:
        db_table = 'ville'


class Adresse(models.Model):
    idadresse = models.AutoField(db_column='idAdresse', primary_key=True)  # Field name made lowercase.
    rue = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    complement = models.CharField(max_length=100, blank=True, null=True)
    ville = models.ForeignKey(Ville, on_delete=models.PROTECT, db_column='idville')  # Field name made lowercase.

    class Meta:
        db_table = 'adresse'


class Client(models.Model):
    idclient = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.CharField(max_length=150)
    telephone = models.CharField(max_length=20)
    mot_de_passe = models.CharField(db_column='mot de passe', max_length=50)  # Field renamed to remove unsuitable characters.
    iban = models.CharField(db_column='IBAN', max_length=16)  # Field name made lowercase.
    adresse = models.ForeignKey(Adresse, on_delete=models.PROTECT, db_column='idadresse')  # Field name made lowercase.

    class Meta:
        db_table = 'client'


class Independant(models.Model):
    numero_entreprise = models.CharField(primary_key=True, max_length=10)
    nom_entreprise = models.CharField(max_length=100)
    date_debut_entreprise = models.CharField(max_length=45, blank=True, null=True)
    client_idclient = models.ForeignKey(Client, on_delete=models.CASCADE, db_column='idclient', related_name='independants')  # Field name made lowercase.

    class Meta:
        db_table = 'independant'


class Particulier(models.Model):
    registre_national = models.CharField(primary_key=True, max_length=15)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, db_column='idclient', related_name='particuliers')  # Field name made lowercase.

    class Meta:
        db_table = 'particulier'

class PersonneACharge(models.Model):
    registre_national = models.CharField(db_column='registre_national', max_length=15, primary_key=True)  # Field name made lowercase.
    date_de_naissance = models.IntegerField(blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, db_column='idclient')  # Field name made lowercase.

    class Meta:
        db_table = 'personne_a_charge'