from . import models
from django import forms

class FormPlanejamento(forms.ModelForm):
    class Meta:
        model = models.Planejamento
        fields = ("nr_inicio", "nr_fim",)
        labels = {
            "nr_inicio": 'Ano inicial do Planejamento',
            "nr_fim": 'Ano final do Planejamento'
        }
        widgets = {
            'nr_inicio': forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ano início"
                }),
            'nr_fim': forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ano fim"
                }),
        }

class FormCadeia(forms.ModelForm):
    class Meta:
        model = models.Cadeia
        fields = ("id_planejamento", "ds_cadeia",)
        labels = {
            "id_planejamento": 'Planejamento Estratégico',
            "ds_cadeia": 'Nome da cadeia'
        }
        widgets = {
            "id_planejamento": forms.Select(
                attrs={
                    "class": "selectpicker form-control"
                }),
            'ds_cadeia': forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nome da Cadeia"
                })
        }

class FormMacroprocesso(forms.ModelForm):
    class Meta:
        model = models.Macroprocesso
        fields = ("id_cadeia", "ds_macroprocesso",)
        labels = {
            "id_cadeia": 'Nome da cadeia',
            "ds_macroprocesso": 'Nome do macroprocesso'
        }
        widgets = {
            'id_cadeia': forms.Select(attrs={"class": "selectpicker form-control"}),
            "ds_macroprocesso": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nome do macroprocesso"})
        }

class FormProcesso(forms.ModelForm):
    class Meta:
        model = models.Processo
        fields = ("id_macroprocesso", "ds_processo",)
        labels = {
            "id_macroprocesso": 'Nome do Macroprocesso',
            "ds_processo": 'Nome do processo'
        }
        widgets = {
            'id_macroprocesso': forms.Select(attrs={"class": "selectpicker form-control"}),
            "ds_processo": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nome do processo"})
        }

class FormRisco(forms.ModelForm):
    class Meta:
        model = models.Risco
        fields = ("id_processo", "ds_risco", "id_dimensao", "id_tipo_risco",
                  "nr_impacto", "nr_probabilidade",)
        labels = {
            "id_processo": 'Nome do processo',
            "id_dimensao": 'Dimensão do risco',
            "id_tipo_risco": "Tipo do risco",
            "ds_risco": "Nome do risco",
            "nr_impacto": "Impacto",
            "nr_probabilidade": "Probabilidade"
        }
        widgets = {
            "id_processo": forms.Select(attrs={"class": "selectpicker form-control"}),
            "id_dimensao": forms.Select(attrs={"class": "selectpicker form-control"}),
            "id_tipo_risco": forms.Select(attrs={"class": "selectpicker form-control"}),
            "ds_risco": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nome do risco"}),
            "nr_impacto": forms.NumberInput(attrs={"class": "form-control", "placeholder": "0-5"}),
            "nr_probabilidade": forms.NumberInput(attrs={"class": "form-control", "placeholder": "0-5"})
        }

class FormSelecionarPlanejamento(forms.Form):
    plan = forms.ModelChoiceField(
        label="Planejamento Estratégico",
        queryset=models.Planejamento.objects.all(),
        empty_label="Selecione o Planejamento Estratégico",
        widget=forms.Select(attrs={'class':'form-control', 'readonly': 'True'})
    )

class FormSelecionarCadeia(forms.Form):
    cadeia = forms.ModelChoiceField(
        label="Cadeia",
        queryset=models.Cadeia.objects.none(),
        empty_label="Selecione a Cadeia",
        widget=forms.Select(attrs={'class':'form-control', 'readonly': 'True'})
    )

class FormSelecionarMacroprocesso(forms.Form):
    macroprocesso = forms.ModelChoiceField(
        label="Macroprocesso",
        queryset=models.Macroprocesso.objects.none(),
        empty_label="Selecione o Macroprocesso",
        widget=forms.Select(attrs={'class':'form-control', 'readonly': 'True'})
    )
