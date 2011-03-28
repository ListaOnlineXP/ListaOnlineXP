from django.contrib import admin
from ListaOnline.disciplina.models import Disciplina, Professor

class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome', 'professor')
    
admin.site.register(Disciplina, DisciplinaAdmin)
admin.site.register(Professor)