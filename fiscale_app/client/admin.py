from django.contrib import admin
from .models import Client, Particulier, Independant, Adresse, Ville, PersonneACharge
# Register your models here.

admin.site.register(Client)
admin.site.register(Particulier)
admin.site.register(Independant)
admin.site.register(Adresse)
admin.site.register(Ville)
admin.site.register(PersonneACharge)