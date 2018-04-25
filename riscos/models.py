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
    id_planejamento = models.ForeignKey(Planejamento, on_delete=models.PROTECT)
    ds_cadeia = models.CharField(max_length=200)
    dt_cadastro = models.DateTimeField(auto_now_add=True)
    ds_usuario = models.CharField(max_length=30)

    def __str__(self):
        return self.ds_cadeia

class Macroprocesso(models.Model):
    id_cadeia = models.ForeignKey(Cadeia, on_delete=models.PROTECT)
    ds_macroprocesso = models.CharField(max_length=200)
    dt_cadastro = models.DateTimeField(auto_now_add=True)
    ds_usuario = models.CharField(max_length=30)

    def __str__(self):
        return self.ds_macroprocesso

class Processo(models.Model):
    id_macroprocesso = models.ForeignKey(Macroprocesso, on_delete=models.PROTECT)
    ds_processo = models.CharField(max_length=200)
    dt_cadastro = models.DateTimeField(auto_now_add=True)
    ds_usuario = models.CharField(max_length=30)

    def __str__(self):
        return self.ds_processo

class Tipo_Risco(models.Model):
    ds_tipo_risco = models.CharField(max_length=200)
    dt_cadastro = models.DateTimeField(auto_now_add=True)
    ds_usuario = models.CharField(max_length=30)

    def __str__(self):
        return self.ds_tipo_risco

class Impacto(models.Model):
    ds_impacto = models.CharField(max_length=200)
    ds_escala = models.CharField(max_length=200)
    nr_valor = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    dt_cadastro = models.DateTimeField(auto_now_add=True)
    ds_usuario = models.CharField(max_length=30)

    def __str__(self):
        return "%s - %s: %s" % (str(self.nr_valor), self.ds_escala , self.ds_impacto)

class Probabilidade(models.Model):
    ds_probabilidade = models.CharField(max_length=200)
    ds_escala = models.CharField(max_length=200)
    nr_valor = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    dt_cadastro = models.DateTimeField(auto_now_add=True)
    ds_usuario = models.CharField(max_length=30)

    def __str__(self):
        return "%s - %s: %s" % (str(self.nr_valor), self.ds_escala , self.ds_probabilidade)

class Risco(models.Model):
    id_processo = models.ForeignKey(Processo, on_delete=models.PROTECT)
    id_tipo_risco = models.ForeignKey(Tipo_Risco, on_delete=models.PROTECT)
    id_impacto = models.ForeignKey(Impacto, on_delete=models.PROTECT)
    id_probabilidade = models.ForeignKey(Probabilidade, on_delete=models.PROTECT)
    ds_risco = models.CharField(max_length=200)
    dt_cadastro = models.DateTimeField(auto_now_add=True)
    ds_usuario = models.CharField(max_length=30)

    def __str__(self):
        return self.ds_risco

class CausaConsequencia(models.Model):
    STATUS_CHOICE = (
        ("Causa", "Causa"),
        ("Consequência", "Consequência"),
    )
    id_risco = models.ForeignKey(Risco, on_delete=models.PROTECT)
    ds_tipo = models.CharField(max_length=30, choices=STATUS_CHOICE,)
    ds_causa_consequencia = models.CharField(max_length=500)
    dt_cadastro = models.DateTimeField(auto_now_add=True)
    ds_usuario = models.CharField(max_length=30)

    def __str__(self):
        return self.ds_causa_consequencia

class Tratamento(models.Model):
    STATUS_CHOICE = (
        ("Inexistente", "Inexistente") ,
        ("Ineficaz", "Ineficaz"),
        ("Ineficiente", "Ineficiente"),
        ("Existente", "Existente"),
    )
    id_causa_consequencia = models.ForeignKey(CausaConsequencia, on_delete=models.PROTECT)
    ds_status = models.CharField(max_length=30, choices=STATUS_CHOICE, default="Inexistente",)
    ds_controle = models.CharField(max_length=500)
    ds_oque = models.CharField(max_length=500)
    ds_quem = models.CharField(max_length=500)
    ds_porque = models.CharField(max_length=500)
    ds_onde = models.CharField(max_length=500)
    dt_quando = models.DateField() 
    ds_como = models.CharField(max_length=500)
    ds_quanto = models.FloatField(validators=[MinValueValidator(0)]) 
    dt_cadastro = models.DateTimeField(auto_now_add=True)
    ds_usuario = models.CharField(max_length=30)

    def __str__(self):
        return self.ds_controle


