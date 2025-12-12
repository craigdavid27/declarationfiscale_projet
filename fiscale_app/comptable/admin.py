from django.contrib import admin
from .models import Poste, MembreCabinet, AttributionDeclarationFiscaleAMembre
# Register your models here.

admin.site.register(Poste)
admin.site.register(MembreCabinet)
admin.site.register(AttributionDeclarationFiscaleAMembre)