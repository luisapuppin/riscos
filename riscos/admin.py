from django.contrib import admin

# Register your models here.

from . import models

admin.site.register(models.Planejamento)
admin.site.register(models.Cadeia)
admin.site.register(models.Macroprocesso)
admin.site.register(models.Processo)
admin.site.register(models.Tipo_Risco)
admin.site.register(models.Impacto)
admin.site.register(models.Probabilidade)
admin.site.register(models.Risco)
admin.site.register(models.CausaConsequencia)
admin.site.register(models.Tratamento)
