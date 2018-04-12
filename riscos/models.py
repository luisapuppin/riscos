from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Planejamento(models.Model):
    nr_inicio = models.PositiveSmallIntegerField("ano inicial do pe")
    nr_fim = models.PositiveSmallIntegerField("ano final do pe")
    ds_planejamento = models.CharField(max_length=9)
    dt_cadastro = models.DateTimeField(auto_now_add=True)
    ds_usuario = models.CharField(max_length=30)

    def __str__(self):
        return self.ds_planejamento

class Cadeia(models.Model):
    id_planejamento = models.ForeignKey(Planejamento, on_delete=models.CASCADE)
    ds_cadeia = models.CharField(max_length=200)
    dt_cadastro = models.DateTimeField(auto_now_add=True)
    ds_usuario = models.CharField(max_length=30)

    def __str__(self):
        return self.ds_cadeia

class Macroprocesso(models.Model):
    id_cadeia = models.ForeignKey(Cadeia, on_delete=models.CASCADE)
    ds_macroprocesso = models.CharField(max_length=200)
    dt_cadastro = models.DateTimeField(auto_now_add=True)
    ds_usuario = models.CharField(max_length=30)

    def __str__(self):
        return self.ds_macroprocesso

class Processo(models.Model):
    id_macroprocesso = models.ForeignKey(Macroprocesso, on_delete=models.CASCADE)
    ds_processo = models.CharField(max_length=200)
    dt_cadastro = models.DateTimeField(auto_now_add=True)
    ds_usuario = models.CharField(max_length=30)

    def __str__(self):
        return self.ds_processo

class Dimensao(models.Model):
    ds_dimensao = models.CharField(max_length=200)
    dt_cadastro = models.DateTimeField(auto_now_add=True)
    ds_usuario = models.CharField(max_length=30)

    def __str__(self):
        return self.ds_dimensao

class Tipo_Risco(models.Model):
    ds_tipo_risco = models.CharField(max_length=200)
    dt_cadastro = models.DateTimeField(auto_now_add=True)
    ds_usuario = models.CharField(max_length=30)

    def __str__(self):
        return self.ds_tipo_risco

class Risco(models.Model):
    id_processo = models.ForeignKey(Processo, on_delete=models.CASCADE)
    id_dimensao = models.ForeignKey(Dimensao, on_delete=models.CASCADE)
    id_tipo_risco = models.ForeignKey(Tipo_Risco, on_delete=models.CASCADE)
    ds_risco = models.CharField(max_length=200)
    nr_impacto = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    nr_probabilidade = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    dt_cadastro = models.DateTimeField(auto_now_add=True)
    ds_usuario = models.CharField(max_length=30)

    def __str__(self):
        return self.ds_risco
