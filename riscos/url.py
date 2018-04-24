from django.urls import re_path
from . import views

app_name = 'riscos'
urlpatterns = [

    # RISCOS
    re_path(r'^$', views.index, name="index"),

    # CADEIA
    re_path(r'^cadeia/$', views.listar_cadeia, name="listar_cadeia"),
    re_path(r'^cadeia/(?P<target_id>[0-9]+)/$', views.detalhar_cadeia, name="detalhar_cadeia"),
    re_path(r'^cadeia/criar/$', views.criar_cadeia, name="criar_cadeia"),

    # PLANEJAMENTO
    re_path(r'^planejamento/$', views.listar_planejamento, name="listar_planejamento"),
    re_path(r'^planejamento/(?P<target_id>[0-9]+)/$', views.detalhar_planejamento,
            name="detalhar_planejamento"),
    re_path(r'^planejamento/criar/$', views.criar_planejamento, name="criar_planejamento"),

    # MACROPROCESSO
    re_path(r'^macroprocesso/$', views.listar_macroprocesso, name="listar_macroprocesso"),
    re_path(r'^macroprocesso/(?P<target_id>[0-9]+)/$', views.detalhar_macroprocesso,
            name="detalhar_macroprocesso"),
    re_path(r'^macroprocesso/criar/$', views.criar_macroprocesso, name="criar_macroprocesso"),

    # PROCESSO
    re_path(r'^processo/$', views.listar_processo, name="listar_processo"),
    re_path(r'^processo/(?P<target_id>[0-9]+)/$', views.detalhar_processo,
            name="detalhar_processo"),
    re_path(r'^processo/criar/$', views.criar_processo, name="criar_processo"),

    # RISCO
    re_path(r'^risco/$', views.listar_risco, name="listar_risco"),
    re_path(r'^risco/(?P<target_id>[0-9]+)/$', views.detalhar_risco, 
            name="detalhar_risco"),
    re_path(r'^risco/criar/$', views.criar_risco, name="criar_risco"),

    # TRATAMENTO
    re_path(r'^tratamento/$', views.listar_tratamento,
            name="listar_tratamento"),
    re_path(r'^tratamento/(?P<target_id>[0-9]+)/$', views.detalhar_tratamento, 
            name="detalhar_tratamento"),
    re_path(r'^tratamento/criar/$', views.criar_tratamento,
            name="criar_tratamento"),

    # AJAX
    re_path(r'^ajax/cadeia/$', views.load_cadeia, name="ajax_load_cadeia"),
    re_path(r'^ajax/macroprocesso/$', views.load_macroprocesso, name="ajax_load_macroprocesso"),
    re_path(r'^ajax/processo/$', views.load_processo, name="ajax_processo"),
    re_path(r'^ajax/risco/$', views.load_risco, name="ajax_risco"),
    re_path(r'^ajax/causa_consequencia/$', views.load_causa_consequencia, name="ajax_causa_consequencia"),
]
