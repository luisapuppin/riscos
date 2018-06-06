from datetime import date, timedelta
import random

from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.core import serializers
from django.urls import reverse
from django.forms.models import modelformset_factory
from django.db.models import F
from django import forms
from . import forms
from . import models

LIMITE_GRAVES = 12

# ------- INDEX -------
def index(request):
    macroprocessos = models.Macroprocesso.objects.all()
    processos = models.Processo.objects.all()
    riscos = models.Risco.objects.all()
    processos_com_risco = [risco.id_processo for risco in riscos]
    graves = models.Risco.objects.filter(id_probabilidade__gte=LIMITE_GRAVES/F('id_impacto'))
    tratamentos = models.Tratamento.objects.all()
    vencidos = models.Tratamento.objects.filter(dt_quando__lt=date.today())
    proximos = models.Tratamento.objects.filter(dt_quando__lt=date.today() + timedelta(days=15)).exclude(pk__in=vencidos)
    context = {
        "macroprocessos": macroprocessos,
        "processos": processos,
        "processos_com_risco": processos_com_risco,
        "riscos": riscos,
        "tratamentos": tratamentos,
        "vencidos": vencidos,
        "proximos": proximos,
        "graves": graves,
        "active_bar": "home",
    }
    return render(request, "riscos/index.html", context)

# ------- SOBRE -------
def sobre(request):
    context = {
        "active_bar": "sobre",
    }
    return render(request, "riscos/sobre.html", context)
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
    context = {"form": form, "active_bar": "macroprocesso"}
    return render(request, 'riscos/criar_planejamento.html', context)

def listar_planejamento(request):
    lista = models.Planejamento.objects.order_by("ds_planejamento")
    context = {'lista': lista, "active_bar": "macroprocesso",}
    return render(request, 'riscos/listar_planejamento.html', context)

def detalhar_planejamento(request, target_id):
    observacao = get_object_or_404(models.Planejamento, pk=target_id)
    cadeias = models.Cadeia.objects.filter(id_planejamento=target_id).order_by('ds_cadeia')
    macroprocessos = models.Macroprocesso.objects.filter(id_cadeia__id_planejamento=target_id).order_by('id_cadeia', 'ds_macroprocesso')
    context = {
        'observacao': observacao,
        "cadeias": cadeias,
        "macroprocessos": macroprocessos,
        "active_bar": "macroprocesso"
    }
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
    context = {"form": form, "active_bar": "macroprocesso",}
    return render(request, 'riscos/criar_cadeia.html', context)

def listar_cadeia(request):
    lista = models.Cadeia.objects.order_by("id_planejamento")
    context = {'lista': lista, "active_bar": "macroprocesso",}
    return render(request, 'riscos/listar_cadeia.html', context)

def detalhar_cadeia(request, target_id):
    observacao = get_object_or_404(models.Cadeia, pk=target_id)
    macroprocessos = models.Macroprocesso.objects.filter(id_cadeia=target_id).order_by('ds_macroprocesso')
    processos = models.Processo.objects.filter(id_macroprocesso__id_cadeia=target_id).order_by('id_macroprocesso', 'ds_processo')
    context = {
        'observacao': observacao,
        "macroprocessos": macroprocessos,
        "processos": processos,
        "active_bar": "macroprocesso"
    }
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
    processos = models.Processo.objects.filter(id_macroprocesso=target_id)
    context = {
        "observacao": observacao,
        "processos": processos,
        "active_bar": "macroprocesso",
    }
    return render(request, 'riscos/detalhar_macroprocesso.html', context)

# ------- PROCESSO -------
def criar_processo(request, parent_id):
    parent = get_object_or_404(models.Macroprocesso, pk=parent_id)
    if request.method == 'POST':
        form = forms.FormProcesso(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.id_macroprocesso = parent
            instance.ds_usuario = "usuario-teste"
            instance.save()
            return redirect(reverse("riscos:listar_processo"))
    else:
        form = forms.FormProcesso()
    context = {
        "form": form,
        "parent": parent,
        "active_bar": "processo",
    }
    return render(request, 'riscos/criar_processo.html', context)

def listar_processo(request):
    lista = models.Processo.objects.order_by("ds_processo")
    context = {'lista': lista, "active_bar": "processo",}
    return render(request, 'riscos/listar_processo.html', context)

def detalhar_processo(request, target_id):
    observacao = get_object_or_404(models.Processo, pk=target_id)
    riscos = models.Risco.objects.filter(id_processo=target_id)
    com_tratamento = models.Tratamento.objects.filter(id_causa_consequencia__id_risco__id_processo=target_id)
    com_tratamento = [x.id_causa_consequencia.id_risco.pk for x in com_tratamento]
    sem_tratamento = models.Risco.objects.filter(id_probabilidade__gte=LIMITE_GRAVES/F('id_impacto'), id_processo=target_id).exclude(pk__in=com_tratamento)
    x = [(x.id_impacto.nr_valor-(random.randint(10, 60)/100)) for x in riscos]
    y = [(y.id_probabilidade.nr_valor-(random.randint(10, 60)/100)) for y in riscos]
    texto = [z.ds_risco for z in riscos]
    data = {
        "x": x,
        "y": y,
        "mode": 'markers',
        "type": 'scatter',
        "text": texto,
        "textposition": 'bottom center',
        "marker": {"size": 12},
    }
    atividades = models.Atividade.objects.filter(id_processo=target_id).order_by("nr_atividade")
    context = {
        "observacao": observacao,
        "riscos": riscos,
        "data": data,
        "atividades": atividades,
        "sem_tratamento": sem_tratamento,
        "active_bar": "processo",
    }
    return render(request, 'riscos/detalhar_processo.html', context)

# ------- ATIVIDADE ------- 
def criar_atividade(request, parent_id): 
    N_EXTRA = 50
    parent = get_object_or_404(models.Processo, pk=parent_id)
    AtividadeFormset = modelformset_factory(
        models.Atividade, form=forms.FormAtividade, extra=N_EXTRA, min_num=1,
    )
    queryset = models.Atividade.objects.none()
    formset = AtividadeFormset(request.POST or None, queryset=queryset)
    if formset.is_valid():
        instances = formset.save(commit=False)
        for insta in instances:
            insta.id_processo = parent
            insta.ds_usuario = 'usuario-teste'
            insta.save()
        if "submit-e-detalhar" in request.POST:
            return redirect(reverse("riscos:detalhar_processo", kwargs={"target_id":parent_id}))
        else:
            return redirect(reverse("riscos:criar_atividade", kwargs={"parent_id":parent_id}))
    context = {
        "formset": formset,
        "parent": parent,
        "active_bar": "processo",
    }
    return render(request, 'riscos/criar_atividade.html', context)

# ------- RISCO -------
def criar_risco(request, parent_id):
    N_EXTRA = 5
    RiscoCausaFormset = modelformset_factory(
        models.CausaConsequencia, form=forms.FormCausaConsequencia, extra=(N_EXTRA * 2 ) + 1, min_num=1,
    )
    queryset = models.CausaConsequencia.objects.none()
    formset = RiscoCausaFormset(request.POST or None, queryset=queryset)
    parent = get_object_or_404(models.Processo, pk=parent_id)
    form = forms.FormRisco(parent_id, request.POST or None)
    if form.is_valid() and formset.is_valid():
        instance = form.save(commit=False)
        instance.id_processo = parent
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
            return redirect(reverse("riscos:criar_risco", kwargs={"parent_id":parent_id}))
    context = {
        "form": form,
        "parent": parent,
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
    tratamentos = models.Tratamento.objects.filter(id_causa_consequencia__id_risco=target_id)
    riscos = models.Risco.objects.filter(
        id_processo=observacao.id_processo
    ).exclude(
        pk=target_id
    )
    x = [(x.id_impacto.nr_valor - (random.randint(20, 80)/100)) for x in riscos]
    y = [(y.id_probabilidade.nr_valor - (random.randint(20, 80)/100)) for y in riscos]
    texto = [z.ds_risco for z in riscos]
    fator = observacao.id_impacto.nr_valor * observacao.id_probabilidade.nr_valor
    sem_tratamento = fator >= 12 and len(tratamentos) == 0
    data = {
        "x": x,
        "y": y,
        "mode": 'markers',
        "type": 'scatter',
        "text": texto,
        "name": "riscos",
        "textposition": 'bottom center',
        "marker": {"size": 12},
    }
    ponto = {
        "x": [observacao.id_impacto.nr_valor-(random.randint(20, 80)/100)],
        "y": [observacao.id_probabilidade.nr_valor-(random.randint(20, 80)/100)],
        "mode": 'markers+text',
        "type": 'scatter',
        "text": [observacao.ds_risco],
        "name": observacao.ds_risco,
        "textposition": 'bottom center',
        "marker": {"size": 18},
    }
    context = {
        'observacao': observacao,
        "causas": causas,
        "consequencias": consequencias,
        "tratamentos": tratamentos,
        "sem_tratamento": sem_tratamento,
        "data": data,
        "ponto": ponto,
        "active_bar": "risco",
    }
    return render(request, 'riscos/detalhar_risco.html', context)

# ------- TRATAMENTO -------
def criar_tratamento(request, parent_id): 
    form = forms.FormTratamento(parent_id, request.POST or None)
    parent = get_object_or_404(models.Risco, pk=parent_id)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.ds_usuario = 'usuario-teste'
        instance.save()
        return redirect(reverse("riscos:detalhar_risco", kwargs={"target_id":parent_id}))

    context = {
        "form": form,
        "parent": parent,
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
