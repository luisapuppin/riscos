from datetime import date

from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.core import serializers
from django.urls import reverse
from django.forms.models import modelformset_factory
from django import forms
from . import forms
from . import models

# Create your views here.

# ------- INDEX -------
def index(request):
    return render(request, "riscos/index.html", {"active_bar": "home"})

# ------- PLANEJAMENTO -------
def criar_planejamento(request):
    if request.method == 'POST':
        form = forms.FormPlanejamento(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.ds_planejamento = str(instance.nr_inicio) + "-" + str(instance.nr_fim)
            instance.ds_usuario = "usuario-teste"
            instance.save()
            return redirect(reverse("riscos:listar_planejamento"))
    else:
        form = forms.FormPlanejamento()
    context = {"form": form, "active_bar": "planejamento"}
    return render(request, 'riscos/criar_planejamento.html', context)

def listar_planejamento(request):
    lista = models.Planejamento.objects.order_by("ds_planejamento")
    context = {'lista': lista, "active_bar": "planejamento",}
    return render(request, 'riscos/listar_planejamento.html', context)

def detalhar_planejamento(request, target_id):
    observacao = get_object_or_404(models.Planejamento, pk=target_id)
    context = {'observacao': observacao, "active_bar": "planejamento",}
    return render(request, 'riscos/detalhar_planejamento.html', context)

# ------- CADEIA -------
def criar_cadeia(request):
    if request.method == 'POST':
        form = forms.FormCadeia(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.ds_usuario = "usuario-teste"
            instance.save()
            return redirect(reverse("riscos:listar_cadeia"))
    else:
        form = forms.FormCadeia()
    context = {"form": form, "active_bar": "cadeia",}
    return render(request, 'riscos/criar_cadeia.html', context)

def listar_cadeia(request):
    lista = models.Cadeia.objects.order_by("id_planejamento")
    context = {'lista': lista, "active_bar": "cadeia",}
    return render(request, 'riscos/listar_cadeia.html', context)

def detalhar_cadeia(request, target_id):
    observacao = get_object_or_404(models.Cadeia, pk=target_id)
    context = {'observacao': observacao, "active_bar": "cadeia",}
    return render(request, 'riscos/detalhar_cadeia.html', context)

# ------- MACROPROCESSO -------
def criar_macroprocesso(request):
    if request.method == 'POST':
        form2 = forms.FormSelecionarPlanejamento()
        form = forms.FormMacroprocesso(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.ds_usuario = "usuario-teste"
            instance.save()
            return redirect(reverse("riscos:listar_macroprocesso"))
    else:
        form2 = forms.FormSelecionarPlanejamento()
        form = forms.FormMacroprocesso()
    context = {
        "form": form,
        "form2": form2,
        "active_bar": "macroprocesso",
    }
    return render(request, 'riscos/criar_macroprocesso.html', context)

def listar_macroprocesso(request):
    lista = models.Macroprocesso.objects.order_by(
        "id_cadeia__id_planejamento", "id_cadeia__ds_cadeia", "ds_macroprocesso"
    )
    context = {'lista': lista, "active_bar": "macroprocesso",}
    return render(request, 'riscos/listar_macroprocesso.html', context)

def detalhar_macroprocesso(request, target_id):
    observacao = get_object_or_404(models.Macroprocesso, pk=target_id)
    context = {'observacao': observacao, "active_bar": "macroprocesso",}
    return render(request, 'riscos/detalhar_macroprocesso.html', context)

# ------- PROCESSO -------
def criar_processo(request):
    if request.method == 'POST':
        form2 = forms.FormSelecionarPlanejamento()
        form3 = forms.FormSelecionarCadeia()
        form = forms.FormProcesso(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.ds_usuario = "usuario-teste"
            instance.save()
            return redirect(reverse("riscos:listar_processo"))
    else:
        form2 = forms.FormSelecionarPlanejamento()
        form3 = forms.FormSelecionarCadeia()
        form = forms.FormProcesso()
    context = {
        "form": form,
        "form2": form2,
        "form3": form3,
        "active_bar": "processo",
    }
    return render(request, 'riscos/criar_processo.html', context)

def listar_processo(request):
    lista = models.Processo.objects.order_by("ds_processo")
    context = {'lista': lista,"active_bar": "processo",}
    return render(request, 'riscos/listar_processo.html', context)

def detalhar_processo(request, target_id):
    observacao = get_object_or_404(models.Processo, pk=target_id)
    context = {'observacao': observacao,"active_bar": "processo",}
    return render(request, 'riscos/detalhar_processo.html', context)

# ------- RISCO -------
def criar_risco(request):
    N_EXTRA = 5
    RiscoCausaFormset = modelformset_factory(   
        models.CausaConsequencia, form=forms.FormCausaConsequencia, extra=(N_EXTRA * 2 ) + 1, min_num=1, 
    )
    queryset = models.CausaConsequencia.objects.none()
    formset = RiscoCausaFormset(request.POST or None, queryset=queryset)
    form2 = forms.FormSelecionarPlanejamento()
    form3 = forms.FormSelecionarCadeia()
    form4 = forms.FormSelecionarMacroprocesso()
    form = forms.FormRisco(request.POST or None)
    if form.is_valid() and formset.is_valid():
        instance = form.save(commit=False)
        instance.ds_usuario = "usuario-teste"
        instance.save()
        saved_id = instance.pk
        instances = formset.save(commit=False)
        for insta in instances:
            insta.id_risco_id = saved_id
            insta.ds_usuario = 'usuario-teste'
            insta.save()
        if "submit-e-detalhar" in request.POST:
            return redirect(reverse("riscos:detalhar_risco", kwargs={"target_id":saved_id}))
        else:
            return redirect(reverse("riscos:criar_risco"))
    context = {
        "form": form,
        "form2": form2,
        "form3": form3,
        "form4": form4,
        "formset": formset,
        "active_bar": "risco",
        "causa": ":" + str(N_EXTRA + 1),
        "conseq": str(N_EXTRA + 1) + ":",
    }
    return render(request, 'riscos/criar_risco.html', context)

def listar_risco(request):
    lista = models.Risco.objects.order_by("ds_risco")
    context = {'lista': lista, "active_bar": "risco",}
    return render(request, 'riscos/listar_risco.html', context)

def detalhar_risco(request, target_id):
    observacao = get_object_or_404(models.Risco, pk=target_id)
    causas = models.CausaConsequencia.objects.filter(id_risco=target_id, ds_tipo="Causa")
    consequencias = models.CausaConsequencia.objects.filter(id_risco=target_id, ds_tipo="Consequência")
    tratamentos = models.Tratamento.objects.filter(id_causa_consequencia=target_id)
    context = {
        'observacao': observacao,
        "causas": causas,
        "consequencias": consequencias,
        "tratamentos": tratamentos,
        "active_bar": "risco",
    }
    return render(request, 'riscos/detalhar_risco.html', context)

# ------- TRATAMENTO -------
def criar_tratamento(request):
    form2 = forms.FormSelecionarPlanejamento()
    form3 = forms.FormSelecionarCadeia()
    form4 = forms.FormSelecionarMacroprocesso()
    form5 = forms.FormSelecionarProcesso()
    form6 = forms.FormSelecionarRisco()
    
    form = forms.FormTratamento(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.ds_usuario = 'usuario-teste'
        instance.save()
        saved_id = instance.pk
        return redirect(reverse("riscos:detalhar_tratamento", kwargs={"target_id":saved_id}))

    context = {
        "form": form,
        "form2": form2,
        "form3": form3,
        "form4": form4,
        "form5": form5,
        "form6": form6,
        "active_bar": "controle",
    }
    return render(request, "riscos/criar_tratamento.html", context)

def listar_tratamento(request):
    lista = models.Tratamento.objects.order_by("ds_oque")
    context = {
        'lista': lista,
        "active_bar": "controle",
    }
    return render(request, "riscos/listar_tratamento.html", context)

def detalhar_tratamento(request, target_id):
    observacao = get_object_or_404(models.Tratamento, pk=target_id)
    context = {
        'observacao': observacao,
        "hoje": date.today(),
        # "cor": cor,
        "active_bar": "controle",
    }
    return render(request, "riscos/detalhar_tratamento.html", context)

# ------- AJAX -------
def load_cadeia(request):
    id_get = request.GET.get('targetId')
    opcoes = models.Cadeia.objects.filter(id_planejamento=id_get).order_by('ds_cadeia')
    return render(request, 'riscos/dropdown_cadeia.html', {'opcoes': opcoes})

def load_macroprocesso(request):
    id_get = request.GET.get('targetId')
    opcoes = models.Macroprocesso.objects.filter(id_cadeia=id_get).order_by('ds_macroprocesso')
    return render(request, 'riscos/dropdown_macroprocesso.html', {'opcoes': opcoes})

def load_processo(request):
    id_get = request.GET.get('targetId')
    opcoes = models.Processo.objects.filter(id_macroprocesso=id_get).order_by('ds_processo')
    return render(request, 'riscos/dropdown_processo.html', {'opcoes': opcoes})

def load_risco(request):
    id_get = request.GET.get('targetId')
    opcoes = models.Risco.objects.filter(id_processo=id_get).order_by('ds_risco')
    return render(request, 'riscos/dropdown_risco.html', {'opcoes': opcoes})

def load_causa_consequencia(request):
    id_get = request.GET.get('targetId')
    opcoes = models.CausaConsequencia.objects.filter(id_risco=id_get).order_by('ds_causa_consequencia')
    return render(request, 'riscos/dropdown_causa_consequencia.html', {'opcoes': opcoes})
