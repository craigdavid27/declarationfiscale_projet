from django.contrib import admin
from .models import DeclarationFiscale, Depense, DocumentDepense, TypeDepense, TypeImpot, TypeRevenu

# Register your models here.
admin.site.register(DeclarationFiscale)
admin.site.register(Depense)
admin.site.register(DocumentDepense)
admin.site.register(TypeDepense)
admin.site.register(TypeImpot)
admin.site.register(TypeRevenu)