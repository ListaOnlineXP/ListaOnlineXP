from django.db import models

class Professor(models.Model):
    nome = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.nome

class Disciplina(models.Model):
    codigo = models.CharField(max_length=10)
    nome = models.CharField(max_length=50)
    descricao = models.TextField(max_length=200, blank=True)
    professor = models.ForeignKey(Professor)
    
    def __unicode__(self):
        return self.codigo
    