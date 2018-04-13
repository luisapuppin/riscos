from django.shortcuts import render, redirect, get_object_or_404
from django.core import serializers
from django.urls import reverse
from django.http import HttpResponse
from django import forms
from . import forms
from . import models

# Create your views here.

# ------- INDEX -------
def index(request):
    return render(request, "riscos/index.html")

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
    return render(request, 'riscos/criar_planejamento.html', {"form": form})

def listar_planejamento(request):
    lista = models.Planejamento.objects.order_by("ds_planejamento")
    context = {'lista': lista}
    return render(request, 'riscos/listar_planejamento.html', context)

def detalhar_planejamento(request, target_id):
    observacao = get_object_or_404(models.Planejamento, pk=target_id)
    context = {'observacao': observacao}
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
    return render(request, 'riscos/criar_cadeia.html', {"form": form})

def listar_cadeia(request):
    lista = models.Cadeia.objects.order_by("id_planejamento")
    context = {'lista': lista}
    return render(request, 'riscos/listar_cadeia.html', context)

def detalhar_cadeia(request, target_id):
    observacao = get_object_or_404(models.Cadeia, pk=target_id)
    context = {'observacao': observacao}
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
    return render(request, 'riscos/criar_macroprocesso.html', {"form": form, "form2": form2})

def listar_macroprocesso(request):
    lista = models.Macroprocesso.objects.order_by(
        "id_cadeia__id_planejamento", "id_cadeia__ds_cadeia", "ds_macroprocesso"
    )
    context = {'lista': lista}
    return render(request, 'riscos/listar_macroprocesso.html', context)

def detalhar_macroprocesso(request, target_id):
    observacao = get_object_or_404(models.Macroprocesso, pk=target_id)
    context = {'observacao': observacao}
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
    return render(request, 'riscos/criar_processo.html',
                  {"form": form, "form2": form2, "form3": form3})

def listar_processo(request):
    lista = models.Processo.objects.order_by("ds_processo")
    context = {'lista': lista}
    return render(request, 'riscos/listar_processo.html', context)

def detalhar_processo(request, target_id):
    observacao = get_object_or_404(models.Processo, pk=target_id)
    context = {'observacao': observacao}
    return render(request, 'riscos/detalhar_processo.html', context)

# ------- RISCO -------
def criar_risco(request):
    if request.method == 'POST':
        form2 = forms.FormSelecionarPlanejamento(request.POST)
        form3 = forms.FormSelecionarCadeia(request.POST)
        form4 = forms.FormSelecionarMacroprocesso(request.POST)
        form = forms.FormRisco(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance2 = form2.save(commit=False)
            instance3 = form3.save(commit=False)
            instance4 = form4.save(commit=False)
            instance.ds_usuario = "usuario-teste"
            instance.save()
            return redirect(reverse("riscos:listar_risco"))
    else:
        form2 = forms.FormSelecionarPlanejamento()
        form3 = forms.FormSelecionarCadeia()
        form4 = forms.FormSelecionarMacroprocesso()
        form = forms.FormRisco()
    return render(request, 'riscos/criar_risco.html',
                  {"form": form, "form2": form2, "form3": form3, "form4": form4})

def listar_risco(request):
    lista = models.Risco.objects.order_by("ds_risco")
    context = {'lista': lista}
    return render(request, 'riscos/listar_risco.html', context)

def detalhar_risco(request, target_id):
    observacao = get_object_or_404(models.Risco, pk=target_id)
    context = {'observacao': observacao}
    return render(request, 'riscos/detalhar_risco.html', context)

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
