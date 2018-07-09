from datetime import date, timedelta
import pandas as pd
import json
import random

from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.core import serializers
from django.urls import reverse
from django.forms.models import modelformset_factory
from django.db.models import F, Q
from django import forms
from itertools import chain
from . import forms
from . import models

LIMITE_GRAVES = 12
DS_USUARIO = "usuario-teste"

# ------- FUNÇÕES -------

def populate_risco(list_risco):
    for values in list_risco:
        link = models.Processo.objects.filter(ds_processo=values["ds_processo"])[0]
        link2 = models.Probabilidade.objects.filter(nr_valor=values["probabilidade"])[0]
        link3 = models.Impacto.objects.filter(nr_valor=values["impacto"])[0]
        link4 = models.Tipo_Risco.objects.filter(ds_tipo_risco="Operacionais")[0]
        u = models.Risco.objects.get_or_create(
            id_processo=link, id_probabilidade=link2, id_impacto=link3,
            ds_risco=values["ds_risco"], id_tipo_risco=link4, ds_usuario=DS_USUARIO)
        if u[1] == True:
            u[0].save()
    print("[DATABASE] Risco populated!")

def populate_causaconsequencia(list_causaconsequencia):
    for values in list_causaconsequencia:
        link = models.Risco.objects.filter(ds_risco=values["ds_risco"])[0]
        u = models.CausaConsequencia.objects.get_or_create(
            id_risco=link, ds_causa_consequencia=values["ds_causa_consequencia"],
            ds_tipo=values["ds_tipo"], ds_usuario=DS_USUARIO)
        if u[1] == True:
            u[0].save()
    print("[DATABASE] CausaConsequencia populated!")

def cadastrar_importacao(obj_processo, json_xls):
    # Montagem lista de cadastro
    lista_riscos = []
    lista_causa_conseq = []
    try:
        for i in json_xls:
            risco = {}
            risco["ds_processo"] = obj_processo.ds_processo
            risco["ds_tipo_risco"] = i["Tipo"]
            risco["impacto"] = i["I"]
            risco["probabilidade"] = i["P"]
            risco["ds_risco"] = i["Riscos"].strip()
            lista_riscos.append(risco)
            causa = {}
            causa["ds_risco"] = i["Riscos"].strip()
            causa["ds_causa_consequencia"] = i["Causa ou Fator"].strip()
            causa["ds_tipo"] = "Causa"
            conseq = {}
            conseq["ds_risco"] = i["Riscos"].strip()
            conseq["ds_causa_consequencia"] = i["Consequência"].strip()
            conseq["ds_tipo"] = "Consequência"
            lista_causa_conseq.append(causa)
            lista_causa_conseq.append(conseq)
    except Exception as ds_error:
        pass
        # return redirect(reverse("riscos:status_importacao", kwargs={"target_id": target_id, "json_import": output, "status":ds_error}))
    # Cadastro dos dados
    populate_risco(lista_riscos)
    populate_causaconsequencia(lista_causa_conseq)
    return redirect(reverse("riscos:detalhar_processo", kwargs={"target_id":obj_processo.pk}))

# ------- INDEX -------
def index(request):
    macroprocessos = models.Macroprocesso.objects.all()
    processos = models.Processo.objects.all()
    riscos = models.Risco.objects.all()
    processos_com_risco = [risco.id_processo for risco in riscos]
    graves = models.Risco.objects.filter(id_probabilidade__gte=LIMITE_GRAVES/F('id_impacto'))
    tratamentos = models.Tratamento.objects.all()
    vencidos = models.Tratamento.objects.filter(dt_quando__lt=date.today()).exclude(ds_status="Concluído")
    proximos = models.Tratamento.objects.filter(dt_quando__lt=date.today() + timedelta(days=15)).exclude(ds_status="Concluído").exclude(pk__in=vencidos)
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

# ------- CONSULTAR -------
def consultar(request):
    if request.method == 'POST':
        form = forms.FormConsulta(request.POST)
        if form.is_valid():
            parametros = dict(request.POST)
            parametros.pop("csrfmiddlewaretoken")
            parametros.pop("submit")
    else:
        parametros = dict(request.GET)
        iniciais = {
            "tipo": parametros.get("tipo", [1])[0],
            "plan": parametros.get("plan", [None])[0],
            "cad": parametros.get("cad", [None])[0],
            "macro": parametros.get("macro", [None])[0],
            "proc": parametros.get("proc", [None])[0],
            "ativ": parametros.get("ativ", [None])[0],
            "risc": parametros.get("risc", [None])[0]
        }
        form = forms.FormConsulta(initial=iniciais)
    context = {
        "active_bar": "consultar",
        "form": form,
        "parametros": parametros
    }
    if parametros:
        consulta_vazia = [parametros[key][0] for key in parametros if parametros.get(key, [""])[0] != ""]
        resposta = models.Processo.objects.all()
        if len(consulta_vazia) > 1:
            if parametros.get("plan", [""])[0] != "":
                resposta = resposta.filter(id_macroprocesso__id_cadeia__id_planejamento=parametros.get("plan")[0])
            if parametros.get("cad", [""])[0] != "":
                resposta = resposta.filter(id_macroprocesso__id_cadeia=parametros.get("cad")[0])
            if parametros.get("macro", [""])[0] != "":
                resposta = resposta.filter(id_macroprocesso=parametros.get("macro")[0])
            if parametros.get("proc", [""])[0] != "":
                resposta = resposta.filter(ds_processo__icontains=parametros.get("proc")[0])
            if parametros.get("ativ", [""])[0] != "" and parametros.get("risc", [""])[0] != "":
                processos = [x.pk for x in resposta]
                filtro_risco = models.Risco.objects.filter(id_processo__in=processos)
                filtro_risco = filtro_risco.filter(id_atividade__ds_atividade__icontains=parametros.get("ativ")[0])
                filtro_risco = filtro_risco.filter(ds_risco__icontains=parametros.get("risc")[0])
            elif parametros.get("ativ", [""])[0] != "":
                processos = [x.pk for x in resposta]
                filtro_ativ = models.Atividade.objects.filter(id_processo__in=processos, ds_atividade__icontains=parametros.get("ativ")[0])
            elif parametros.get("risc", [""])[0] != "":
                processos = [x.pk for x in resposta]
                filtro_risco = models.Risco.objects.filter(id_processo__in=processos).filter(ds_risco__icontains=parametros.get("risc")[0])
        if int(parametros.get("tipo", [1])[0]) == 1 and 'filtro_risco' in locals():
            riscos = [x.id_processo.pk for x in filtro_risco]
            resposta = resposta.filter(pk__in=riscos)
        if int(parametros.get("tipo", [1])[0]) == 1 and 'filtro_ativ' in locals():
            filtro_ativ = [x.id_processo.pk for x in filtro_ativ]
            resposta = resposta.filter(pk__in=filtro_ativ)
        elif int(parametros.get("tipo", [1])[0]) == 2 and 'filtro_risco' in locals():
            resposta = filtro_risco
        elif int(parametros.get("tipo", [1])[0]) == 2 and 'filtro_ativ' in locals():
            filtro_ativ = [x.pk for x in filtro_ativ]
            resposta = models.Risco.objects.filter(id_atividade__in=filtro_ativ)
        elif int(parametros.get("tipo", [1])[0]) == 2 and 'filtro_risco' not in locals():
            riscos = [x.pk for x in resposta]
            resposta = models.Risco.objects.filter(id_processo__in=riscos)
        context["res"] = resposta
        context["tipo_res"] = parametros.get("tipo", [1])[0]
    return render(request, "riscos/consultar.html", context)

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
            saved_id = instance.pk
            if "submit-e-detalhar" in request.POST:
                return redirect(reverse("riscos:detalhar_processo", kwargs={"target_id":saved_id}))
            else:
                return redirect(reverse("riscos:criar_processo", kwargs={"parent_id":parent_id}))
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

    # Importação de dados

    if request.method == 'POST':
        form = forms.FormImportacao(request.POST, request.FILES)
        if form.is_valid():
            tipo_risco = models.Tipo_Risco.objects.all()
            tipo_risco = [x.ds_tipo_risco for x in tipo_risco]

            # Leitura XLS
            planilha = request.FILES["xls_file"]
            riscos = pd.read_excel(planilha, header=10, usecols="B:J")
            riscos.columns = riscos.columns.map(lambda x: x.strip())
            riscos2 = riscos.dropna(subset=["Tipo"])
            output = json.loads(riscos2.to_json(orient="records", force_ascii=False))
            tipo_risco_xls = [x.strip() for x in json.loads(riscos2.to_json(force_ascii=False))["Tipo"].values()]

            # Checagem dos Tipos
            for i in tipo_risco_xls:
                if i not in tipo_risco:
                    request.session["output_importacao"] = output
                    request.session["id_processo"] = target_id
                    return redirect(reverse("riscos:importacao_confirm"))

            cadastrar_importacao(observacao, output)

    else:
        form = forms.FormImportacao()

    context = {
        "observacao": observacao,
        "riscos": riscos,
        "data": data,
        "atividades": atividades,
        "sem_tratamento": sem_tratamento,
        "active_bar": "processo",
        "form": form
    }
    return render(request, 'riscos/detalhar_processo.html', context)

def importacao_confirm(request):
    form2 = forms.FormConfirmacao(request.POST or None)
    output = request.session.get('output_importacao')
    target_id = request.session.get('id_processo')
    observacao = get_object_or_404(models.Processo, pk=target_id)
    if form2.is_valid():
        cadastrar_importacao(observacao, output)
        return redirect(reverse("riscos:detalhar_processo", kwargs={"target_id": target_id}))
    context = {
        "form2": form2,
        "observacao": observacao
    }
    return render(request, 'riscos/importacao_confirm.html', context)

def editar_processo(request, target_id):
    processo = get_object_or_404(models.Processo, pk=target_id)
    parent = get_object_or_404(models.Macroprocesso, pk=processo.id_macroprocesso.pk)
    form = forms.FormProcesso(request.POST or None, instance=processo)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.ds_usuario = "usuario-teste"
        instance.save()
        return redirect(reverse("riscos:detalhar_processo", kwargs={"target_id":target_id}))
    context = {
        "form": form,
        "parent": parent,
        "acao": "edit",
        "active_bar": "processo",
    }
    return render(request, 'riscos/criar_processo.html', context)

# ------- ATIVIDADE ------- 
def criar_atividade(request, parent_id, acao): 
    N_EXTRA = 50
    parent = get_object_or_404(models.Processo, pk=parent_id)
    AtividadeFormset = modelformset_factory(
        models.Atividade, form=forms.FormAtividade, extra=N_EXTRA, min_num=1,
    )
    queryset = models.Atividade.objects.filter(id_processo=parent_id).order_by("nr_atividade")
    formset = AtividadeFormset(request.POST or None, queryset=queryset)
    if formset.is_valid():
        instances = formset.save(commit=False)
        for insta in instances:
            insta.id_processo = parent
            insta.ds_usuario = 'usuario-teste'
            insta.save()
        return redirect(reverse("riscos:detalhar_processo", kwargs={"target_id":parent_id}))
    context = {
        "formset": formset,
        "parent": parent,
        "active_bar": "processo",
        "acao": acao
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
        "num_causa": 1,
        "num_consq": 1
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

def editar_risco(request, target_id):
    risco = get_object_or_404(models.Risco, pk=target_id)
    N_EXTRA = 5
    RiscoCausaFormset = modelformset_factory(
        models.CausaConsequencia,
        form=forms.FormCausaConsequencia,
        extra=(N_EXTRA * 2) + 1,
        min_num=1,
    )
    consulta = models.CausaConsequencia.objects.filter(id_risco=target_id).order_by("ds_tipo")
    posicao_inicial = [x.ds_tipo for x in consulta]
    num_causa = len([x for x in posicao_inicial if x == "Causa"])
    num_consq = len([x for x in posicao_inicial if x == "Consequência"])
    causa_posicao = [1 + x*1 for x in range(len(posicao_inicial)) if posicao_inicial[x]=="Causa"]
    consq_posicao = [1 + x*1 for x in range(len(posicao_inicial)) if posicao_inicial[x]=="Consequência"]
    for num in range(1, 13):
        if num not in causa_posicao and num not in consq_posicao and len(causa_posicao) < 6:
            causa_posicao.append(num)
        elif num not in causa_posicao and num not in consq_posicao and len(causa_posicao) == 6:
            consq_posicao.append(num)
    formset = RiscoCausaFormset(request.POST or None, queryset=consulta)
    parent = get_object_or_404(models.Processo, pk=risco.id_processo.pk)
    form = forms.FormRisco(risco.id_processo.pk, request.POST or None, instance=risco)
    if form.is_valid() and formset.is_valid():
        instance = form.save(commit=False)
        instance.ds_usuario = "usuario-teste"
        instance.save()
        instances = formset.save(commit=False)
        for insta in instances:
            insta.id_risco = risco
            insta.ds_usuario = 'usuario-teste'
            insta.save()
        return redirect(reverse("riscos:detalhar_risco", kwargs={"target_id":target_id}))
    context = {
        "form": form,
        "parent": parent,
        "formset": formset,
        "active_bar": "risco",
        "causa": ":" + str(N_EXTRA + 1),
        "conseq": str(N_EXTRA + 1) + ":",
        "acao": "edit",
        "causa_posicao": causa_posicao,
        "consq_posicao": consq_posicao,
        "num_causa": num_causa,
        "num_consq": num_consq
    }
    return render(request, 'riscos/criar_risco.html', context)

# ------- TRATAMENTO -------
def criar_tratamento(request, parent_id): 
    form = forms.FormTratamento(parent_id, request.POST or None)
    parent = get_object_or_404(models.Risco, pk=parent_id)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.ds_usuario = 'usuario-teste'
        instance.save()
        saved_id = instance.pk
        if "submit-e-detalhar" in request.POST:
            return redirect(reverse("riscos:detalhar_risco", kwargs={"target_id":parent_id}))
        else:
            return redirect(reverse("riscos:criar_tratamento", kwargs={"parent_id":parent_id}))

    context = {
        "form": form,
        "parent": parent,
        "active_bar": "controle",
    }
    return render(request, "riscos/criar_tratamento.html", context)

def editar_tratamento(request, target_id):
    tratamento = get_object_or_404(models.Tratamento, pk=target_id)
    form = forms.FormTratamento(
        tratamento.id_causa_consequencia.id_risco.pk,
        request.POST or None,
        instance=tratamento
    )
    parent = get_object_or_404(models.Risco, pk=tratamento.id_causa_consequencia.id_risco.pk)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.ds_usuario = 'usuario-teste'
        instance.save()
        return redirect(reverse("riscos:detalhar_risco", kwargs={"target_id":parent.pk}))
    context = {
        "form": form,
        "parent": parent,
        "active_bar": "controle",
        "acao": "edit"
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
        "active_bar": "controle",
    }
    return render(request, "riscos/detalhar_tratamento.html", context)

# ------- MONITORAMENTO -------
def fazer_monitoramento(request):
    hoje = date.today()
    ano = hoje.strftime("%Y")
    mes = int(hoje.strftime("%m"))
    quadrimestre = (mes - 1)//3 + 1
    ciclo = ano + "/" + str(quadrimestre)
    
    monitoramento = models.Monitoramento.objects.filter(id_ciclo_monitoramento=ciclo)
    monitorados = [x.id_tratamento.pk for x in monitoramento]
    tratamentos = models.Tratamento.objects.all().exclude(pk__in=monitorados)

    form = forms.FormMonitoramento(request.POST or None)
    
    if form.is_valid():
        id_tratamento = [x[11:] for x in request.POST if "tratamento" in x]
        parent =  get_object_or_404(models.Tratamento, pk=id_tratamento[0])
        instance = form.save(commit=False)
        instance.id_tratamento = parent
        instance.id_ciclo_monitoramento = ciclo
        instance.ds_usuario = "usuario-teste"
        models.Tratamento.objects.filter(id=id_tratamento[0]).update(ds_status=instance.ds_status)
        instance.save()
        return redirect(reverse("riscos:fazer_monitoramento"))
    
    context = {
        "form": form,
        "tratamentos": tratamentos,
        "hoje": date.today,
        "active_bar": "monitoramento",
    }
    return render(request, "riscos/fazer_monitoramento.html", context)

