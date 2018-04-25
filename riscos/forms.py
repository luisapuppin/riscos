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
        fields = ("id_processo", "ds_risco", "id_tipo_risco",
                  "id_impacto", "id_probabilidade",)
        labels = {
            "id_processo": 'Nome do processo',
            "id_tipo_risco": "Tipo do risco",
            "ds_risco": "Descrição do risco",
            "id_impacto": "Impacto",
            "id_probabilidade": "Probabilidade"
        }
        widgets = {
            "id_processo": forms.Select(attrs={"class": "selectpicker form-control"}),
            "id_tipo_risco": forms.Select(attrs={"class": "selectpicker form-control"}),
            "ds_risco": forms.TextInput(attrs={"class": "form-control", "placeholder": "Descrição do risco"}),
            "id_impacto": forms.Select(attrs={"class": "form-control"}),
            "id_probabilidade": forms.Select(attrs={"class": "form-control"})
        }

class FormCausaConsequencia(forms.ModelForm):
    class Meta:
        model = models.CausaConsequencia
        fields = ("ds_causa_consequencia", "ds_tipo", )
        labels = {"ds_causa_consequencia": "", "ds_tipo": ""}
        widgets = {
            "ds_causa_consequencia": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Descrição"}
            ),
            "ds_tipo": forms.Select(attrs={"class": "selectpicker form-control", "style":"display:none"}),
        }

class FormTratamento(forms.ModelForm):
    class Meta:
        model = models.Tratamento
        fields = ("id_causa_consequencia", "ds_controle", "ds_status", "ds_oque", "ds_quem", "ds_porque",
                  "ds_onde", "dt_quando", "ds_como", "ds_quanto",)
        labels = {
            "id_causa_consequencia": "Controle sobre:",
            "ds_status": "Status do controle",
            "ds_controle": "Descrição do controle",
            "ds_oque": "O que?",
            "ds_quem": "Quem?",
            "ds_porque": "Por que?",
            "ds_onde": "Onde?",
            "dt_quando": "Quando?",
            "ds_como": "Como?",
            "ds_quanto": "Quanto?",
        }
        widgets = {
            "id_causa_consequencia": forms.Select(
                attrs={"class": "selectpicker form-control"}
            ),
            "ds_status": forms.Select(
                attrs={"class": "selectpicker form-control"}
            ),
            "ds_controle": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Descreva o que será realizado"}
            ),
            "ds_oque": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Descreva o que será realizado"}
            ),
            "ds_quem": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Quem será o responsável?"}
            ),
            "ds_porque": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Por que isso será feito?"}
            ),
            "ds_onde": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Onde isso será feito?"}
            ),
            "dt_quando": forms.DateInput(
                attrs={"class": "form-control"}, format="%d/%m/%Y", 
            ),
            "ds_como": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Como isso ocorrerá?"}
            ),
            "ds_quanto": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Quanto isso custará (R$) ?"}
            )
        }


# ----- FORMS AJAX ----- #

class FormSelecionarPlanejamento(forms.Form):
    plan = forms.ModelChoiceField(
        label="Planejamento Estratégico",
        queryset=models.Planejamento.objects.all(),
        empty_label="Selecione o Planejamento Estratégico",
        widget=forms.Select(attrs={'class':'form-control', 'readonly': "True"})
    )

class FormSelecionarCadeia(forms.Form):
    cadeia = forms.ModelChoiceField(
        label="Cadeia",
        queryset=models.Cadeia.objects.none(),
        empty_label="Selecione a Cadeia",
        widget=forms.Select(attrs={'class':'form-control', 'readonly': "True"})
    )

class FormSelecionarMacroprocesso(forms.Form):
    macroprocesso = forms.ModelChoiceField(
        label="Macroprocesso",
        queryset=models.Macroprocesso.objects.none(),
        empty_label="Selecione o Macroprocesso",
        widget=forms.Select(attrs={'class':'form-control', 'readonly': "True"})
    )

class FormSelecionarProcesso(forms.Form):
    processo = forms.ModelChoiceField(
        label="Processo",
        queryset=models.Processo.objects.none(),
        empty_label="Selecione o Processo",
        widget=forms.Select(attrs={'class':'form-control', 'readonly': "True"})
    )

class FormSelecionarRisco(forms.Form):
    risco = forms.ModelChoiceField(
        label="Risco",
        queryset=models.Risco.objects.none(),
        empty_label="Selecione o Risco",
        widget=forms.Select(attrs={'class':'form-control', 'readonly': "True"})
    )
