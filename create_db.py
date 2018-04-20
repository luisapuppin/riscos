#!/usr/bin/env python
import os
import sys

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

def populate():
    from riscos import models

    populate = {
        'Planejamento': [
            {"nr_inicio": 2016, "nr_fim": 2019, "ds_planejamento": "2016-2019"}
        ],
        'Cadeia': [
            {'ds_cadeia': 'ANÁLISE DO SETOR E FORMULAÇÃO DE POLÍTICAS', "ds_planejamento": "2016-2019"},
            {'ds_cadeia': 'INCENTIVO À AGROPECUÁRIA', "ds_planejamento": "2016-2019"},
            {'ds_cadeia': 'GESTÃO DE CONHECIMENTO E TECNOLOGIA AGROPECUÁRIA', "ds_planejamento": "2016-2019"},
            {'ds_cadeia': 'APOIO AO DESENVOLVIMENTO DOS PRODUTORES RURAIS', "ds_planejamento": "2016-2019"},
            {'ds_cadeia': 'FOMENTO À PRODUÇÃO AGROPECUÁRIA SUSTENTÁVEL E À AGREGAÇÃO DE VALOR', "ds_planejamento": "2016-2019"},
            {'ds_cadeia': 'GESTÃO DE DEFESA AGROPECUÁRIA', "ds_planejamento": "2016-2019"},
            {'ds_cadeia': 'INSERÇÃO DOS PRODUTOS E INSUMOS NOS MERCADOS AGROPECUÁRIOS', "ds_planejamento": "2016-2019"},
            {'ds_cadeia': 'SUPORTE', "ds_planejamento": "2016-2019"}
        ],
        "Macroprocesso": [
            {"ds_cadeia": "ANÁLISE DO SETOR E FORMULAÇÃO DE POLÍTICAS",
             "ds_macroprocesso": "GESTÃO DE POLÍTICAS PÚBLICAS AGROPECUÁRIAS"},
            {"ds_cadeia": "ANÁLISE DO SETOR E FORMULAÇÃO DE POLÍTICAS",
             "ds_macroprocesso": "INTELIGÊNCIA AGROPECUÁRIA"},
            {"ds_cadeia": "INCENTIVO À AGROPECUÁRIA",
             "ds_macroprocesso": "FOMENTO AO CRÉDITO AGROPECUÁRIO"},
            {"ds_cadeia": "INCENTIVO À AGROPECUÁRIA",
             "ds_macroprocesso": "APOIO ECONÔMICO À PRODUÇÃO AGROPECUÁRIA "},
            {"ds_cadeia": "GESTÃO DE CONHECIMENTO E TECNOLOGIA AGROPECUÁRIA",
             "ds_macroprocesso": "CONCESSÃO DE REGISTROS, CERTIFICAÇÕES E CLASSIFICAÇÕES AGROPECUÁRIAS"},
            {"ds_cadeia": "APOIO AO DESENVOLVIMENTO DOS PRODUTORES RURAIS",
             "ds_macroprocesso": "FORTALECIMENTO DOS PRODUTORES RURAIS"},
            {"ds_cadeia": "FOMENTO À PRODUÇÃO AGROPECUÁRIA SUSTENTÁVEL E À AGREGAÇÃO DE VALOR",
             "ds_macroprocesso": "FOMENTO À MELHORIA DA QUALIDADE E PRÁTICAS AGROPECUÁRIAS, AGROINDUSTRIAIS, EXTRATIVISTAS SUSTENTÁVEIS"},
            {"ds_cadeia": "FOMENTO À PRODUÇÃO AGROPECUÁRIA SUSTENTÁVEL E À AGREGAÇÃO DE VALOR",
             "ds_macroprocesso": "FOMENTO À AGREGAÇÃO DE VALOR E DIFERENCIAÇÃO"},
            {"ds_cadeia": "GESTÃO DE DEFESA AGROPECUÁRIA",
             "ds_macroprocesso": "CONCESSÃO DE REGISTROS, CERTIFICAÇÕES E CLASSIFICAÇÕES AGROPECUÁRIAS"},
            {"ds_cadeia": "GESTÃO DE DEFESA AGROPECUÁRIA",
             "ds_macroprocesso": "INSPEÇÃO E FISCALIZAÇÃO DE PRODUTOS E INSUMOS AGROPECUÁRIOS"},
            {"ds_cadeia": "GESTÃO DE DEFESA AGROPECUÁRIA",
             "ds_macroprocesso": "MONITORAMENTO E PREVENÇÃO DE DOENÇAS E PRAGAS"},
            {"ds_cadeia": "GESTÃO DE DEFESA AGROPECUÁRIA",
             "ds_macroprocesso": "GESTÃO DO SISTEMA UNIFICADO DE ATENÇÃO À SANIDADE AGROPECUÁRIA"},
            {"ds_cadeia": "GESTÃO DE DEFESA AGROPECUÁRIA",
             "ds_macroprocesso": "GESTÃO DE ANÁLISES LABORATORIAIS AGROPECUÁRIAS"},
            {"ds_cadeia": "INSERÇÃO DOS PRODUTOS E INSUMOS NOS MERCADOS AGROPECUÁRIOS",
             "ds_macroprocesso": "DEFINIÇÃO E EXECUÇÃO DAS ESTRATÉGIAS DE TRANSPORTE, ESCOAMENTO E ABASTECIMENTO INTERNO"},
            {"ds_cadeia": "INSERÇÃO DOS PRODUTOS E INSUMOS NOS MERCADOS AGROPECUÁRIOS",
             "ds_macroprocesso": "PROMOÇÃO, ABERTURA E MANUTENÇÃO DE MERCADOS"},
            {"ds_cadeia": "INSERÇÃO DOS PRODUTOS E INSUMOS NOS MERCADOS AGROPECUÁRIOS",
             "ds_macroprocesso": "PROTEÇÃO DO MERCADO AGROPECUÁRIO BRASILEIRO"},
            {"ds_cadeia": "SUPORTE", "ds_macroprocesso": "GESTÃO E CONTROLE INSTITUCIONAL"},
            {"ds_cadeia": "SUPORTE", "ds_macroprocesso": "PLANEJAMENTO E DESENVOLVIMENTO INSTITUCIONAL"},
            {"ds_cadeia": "SUPORTE", "ds_macroprocesso": "GESTÃO ORÇAMENTÁRIA, FINANCEIRA E CONTÁBIL"},
            {"ds_cadeia": "SUPORTE", "ds_macroprocesso": "COMUNICAÇÃO E MEMÓRIA INSTITUCIONAL"},
            {"ds_cadeia": "SUPORTE", "ds_macroprocesso": "GESTÃO DE PESSOAS"},
            {"ds_cadeia": "SUPORTE", "ds_macroprocesso": "GESTÃO DE TECNOLOGIA DA INFORMAÇÃO"},
            {"ds_cadeia": "SUPORTE", "ds_macroprocesso": "ADMINISTRAÇÃO E LOGÍSTICA"}
        ],
        "Tipo_Risco": [
            {"ds_tipo_risco": "Ambientais"},
            {"ds_tipo_risco": "Climáticos"},
            {"ds_tipo_risco": "Financeiros ou orçamentários"},
            {"ds_tipo_risco": "Fitossanitários"},
            {"ds_tipo_risco": "Sanitários"},
            {"ds_tipo_risco": "Fraude econômica"},
            {"ds_tipo_risco": "Imagem/reputação do órgão"},
            {"ds_tipo_risco": "Legais"},
            {"ds_tipo_risco": "Operacionais"}
        ],
        "Impacto": [
            {"ds_impacto": "Impactos mínimos (de tempo, prazo, custo, quantidade, qualidade, acesso, escopo, imagem, etc.)", "ds_escala": "Muito baixo", "nr_valor": 1},
            {"ds_impacto": "Impactos pequenos", "ds_escala": "Baixo", "nr_valor": 2},
            {"ds_impacto": "Impactos significativos, porém recuperáveis", "ds_escala": "Médio", "nr_valor": 3},
            {"ds_impacto": "Impactos de reversão muito difícil", "ds_escala": "Alto", "nr_valor": 4},
            {"ds_impacto": "Impactos de dificílima reversão", "ds_escala": "Muito alto", "nr_valor": 5}
        ],
        "Probabilidade": [
            {"ds_probabilidade": "Evento pode ocorrer apenas em circunstâncias excepcionais", "ds_escala": "Rara", "nr_valor": 1},
            {"ds_probabilidade": "Evento pode ocorrer em algum momento", "ds_escala": "Improvável", "nr_valor": 2},
            {"ds_probabilidade": "Evento deve ocorrer em algum momento", "ds_escala": "Possível", "nr_valor": 3},
            {"ds_probabilidade": "Evento provavelmente ocorra na maioria das circunstâncias", "ds_escala": "Provável", "nr_valor": 4},
            {"ds_probabilidade": "Evento esperado que ocorra na maioria das circunstâncias", "ds_escala": "Quase certo", "nr_valor": 5}
        ]
    }

    ds_usuario = "usuario-teste"

    print("[DATABASE] Populating database...")

    for values in populate["Tipo_Risco"]:
        u = models.Tipo_Risco.objects.get_or_create(
            ds_tipo_risco=values["ds_tipo_risco"], ds_usuario=ds_usuario)
        if u[1] == True:
            u[0].save()

    print("[DATABASE] Tipo_Risco populated!")

    for values in populate["Impacto"]:
        u = models.Impacto.objects.get_or_create(
            ds_impacto=values["ds_impacto"], ds_escala=values["ds_escala"],
            nr_valor=values["nr_valor"], ds_usuario=ds_usuario)
        if u[1] == True:
            u[0].save()
    
    print("[DATABASE] Impacto populated!")

    for values in populate["Probabilidade"]:
        u = models.Probabilidade.objects.get_or_create(
            ds_probabilidade=values["ds_probabilidade"], ds_escala=values["ds_escala"],
            nr_valor=values["nr_valor"], ds_usuario=ds_usuario)
        if u[1] == True:
            u[0].save()

    print("[DATABASE] Probabilidade populated!")

    for values in populate["Planejamento"]:
        u = models.Planejamento.objects.get_or_create(
            nr_inicio=values["nr_inicio"], nr_fim=values["nr_fim"],
            ds_planejamento=values["ds_planejamento"], ds_usuario=ds_usuario)
        if u[1] == True:
            u[0].save()

    print("[DATABASE] Planejamento populated!")

    for values in populate["Cadeia"]:
        link = models.Planejamento.objects.filter(ds_planejamento=values["ds_planejamento"])[0]
        u = models.Cadeia.objects.get_or_create(
            id_planejamento=link, ds_cadeia=values["ds_cadeia"], ds_usuario=ds_usuario)
        if u[1] == True:
            u[0].save()

    print("[DATABASE] Cadeia populated!")

    for values in populate["Macroprocesso"]:
        link = models.Cadeia.objects.filter(ds_cadeia=values["ds_cadeia"])[0]
        u = models.Macroprocesso.objects.get_or_create(
            id_cadeia=link, ds_macroprocesso=values["ds_macroprocesso"], ds_usuario=ds_usuario)
        if u[1] == True:
            u[0].save()

    print("[DATABASE] Macroprocesso populated!")

    print("[DATABASE] Done.")

    sys.exit(0)


if __name__ == '__main__':
    django.setup()
    populate()
