from django.urls import re_path
from . import views

app_name = 'riscos'
urlpatterns = [

    # INDEX
    re_path(r'^$', views.index, name="index"),
    
    # SOBRE
    re_path(r'^sobre/$', views.sobre, name="sobre"),

    # CONSULTAR
    re_path(r'^consultar/$', views.consultar, name="consultar"),

    # CADEIA
    re_path(r'^cadeia/listar/$', views.listar_cadeia, name="listar_cadeia"),
    re_path(r'^cadeia/(?P<target_id>[0-9]+)/detalhar/$', views.detalhar_cadeia, name="detalhar_cadeia"),
    re_path(r'^cadeia/criar/$', views.criar_cadeia, name="criar_cadeia"),

    # PLANEJAMENTO
    re_path(r'^planejamento/listar/$', views.listar_planejamento, name="listar_planejamento"),
    re_path(r'^planejamento/(?P<target_id>[0-9]+)/detalhar/$', views.detalhar_planejamento,
            name="detalhar_planejamento"),
    re_path(r'^planejamento/criar/$', views.criar_planejamento, name="criar_planejamento"),

    # MACROPROCESSO
    re_path(r'^macroprocesso/listar/$', views.listar_macroprocesso, name="listar_macroprocesso"),
    re_path(r'^macroprocesso/(?P<target_id>[0-9]+)/detalhar/$', views.detalhar_macroprocesso,
            name="detalhar_macroprocesso"),
    re_path(r'^macroprocesso/criar/$', views.criar_macroprocesso, name="criar_macroprocesso"),

    # PROCESSO
    re_path(r'^processo/listar/$', views.listar_processo, name="listar_processo"),
    re_path(r'^processo/(?P<target_id>[0-9]+)/detalhar/$', views.detalhar_processo,
            name="detalhar_processo"),
    re_path(r'^processo/(?P<target_id>[0-9]+)/editar/$', views.editar_processo,
            name="editar_processo"),
    re_path(r'^macroprocesso/(?P<parent_id>[0-9]+)/criar/processo/$', views.criar_processo, name="criar_processo"),

    # ATIVIDADE 
    re_path(r'^processo/(?P<parent_id>[0-9]+)/atividade/(?P<acao>[a-z]+)/$', views.criar_atividade, name="criar_atividade"),  

    # RISCO
    re_path(r'^risco/listar/$', views.listar_risco, name="listar_risco"),
    re_path(r'^risco/(?P<target_id>[0-9]+)/detalhar/$', views.detalhar_risco, 
            name="detalhar_risco"),
    re_path(r'^processo/(?P<parent_id>[0-9]+)/criar/risco/$', views.criar_risco, name="criar_risco"),

    # TRATAMENTO
    re_path(r'^tratamento/listar/$', views.listar_tratamento,
            name="listar_tratamento"),
    re_path(r'^tratamento/(?P<target_id>[0-9]+)/detalhar/$', views.detalhar_tratamento, 
            name="detalhar_tratamento"),
    re_path(r'^risco/(?P<parent_id>[0-9]+)/criar/tratamento/$', views.criar_tratamento, name="criar_tratamento"),

]
