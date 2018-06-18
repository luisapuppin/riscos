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
        ],
        "Processo": [
            {"ds_macroprocesso": "GESTÃO DE POLÍTICAS PÚBLICAS AGROPECUÁRIAS", "ds_processo": "Pagamento de faturas de águas, energia e telefonia"}
        ],
        "Atividade": [
            {'ds_processo': 'Pagamento de faturas de águas, energia e telefonia', 'nr_atividade': 1, 'ds_atividade': 'Assinar recebimento da fatura física', 'ds_responsavel': 'Fiscal do contrato'},
            {'ds_processo': 'Pagamento de faturas de águas, energia e telefonia', 'nr_atividade': 11, 'ds_atividade': 'Registrar liquidação no SIAFI', 'ds_responsavel': 'Divisão Financeira - CGOF'},
            {'ds_processo': 'Pagamento de faturas de águas, energia e telefonia', 'nr_atividade': 12, 'ds_atividade': 'Gerar programação finanaceira no SIAFI', 'ds_responsavel': 'Divisão Financeira - CGOF'},
            {'ds_processo': 'Pagamento de faturas de águas, energia e telefonia', 'nr_atividade': 13, 'ds_atividade': 'Elaborar programação financeira categorias gasto C e D vinc. 400', 'ds_responsavel': 'Coordenação Financeira - CFN/CGOF'},
            {'ds_processo': 'Pagamento de faturas de águas, energia e telefonia', 'nr_atividade': 14, 'ds_atividade': 'Despachar prog. finan. cat. gasto C e D vinc. 400', 'ds_responsavel': 'Coordenação Geral - CGOF'},
            {'ds_processo': 'Pagamento de faturas de águas, energia e telefonia', 'nr_atividade': 15, 'ds_atividade': 'Submeter prog. financ. cat. gasto C e D vinc. 400 à deliberação', 'ds_responsavel': 'Diretoria de Programa/SE'},
            {'ds_processo': 'Pagamento de faturas de águas, energia e telefonia', 'nr_atividade': 16, 'ds_atividade': 'Autorizar a liberação de recursos financeiros', 'ds_responsavel': 'Secretária Executiva'},
            {'ds_processo': 'Pagamento de faturas de águas, energia e telefonia', 'nr_atividade': 17, 'ds_atividade': 'Despachar prog. financ. cat. gasto C e D vinc. 400 autorizada', 'ds_responsavel': 'Diretoria de Programa/SE'},
            {'ds_processo': 'Pagamento de faturas de águas, energia e telefonia', 'nr_atividade': 18, 'ds_atividade': 'Despachar autorização de liberação dos recursos financeiros', 'ds_responsavel': 'Coordenação-Geral da CGOF'},
            {'ds_processo': 'Pagamento de faturas de águas, energia e telefonia', 'nr_atividade': 19, 'ds_atividade': 'Elaborar planilha de liberação financ. autorizada', 'ds_responsavel': 'Coordenação Financeira - CFN'},
            {'ds_processo': 'Pagamento de faturas de águas, energia e telefonia', 'nr_atividade': 2, 'ds_atividade': 'Emitir fatura via web', 'ds_responsavel': 'Fiscal do contrato'},
            {'ds_processo': 'Pagamento de faturas de águas, energia e telefonia', 'nr_atividade': 3, 'ds_atividade': 'Analisar Fatura', 'ds_responsavel': 'Fiscal do contrato'},
            {'ds_processo': 'Pagamento de faturas de águas, energia e telefonia', 'nr_atividade': 4, 'ds_atividade': 'Instituir processo', 'ds_responsavel': 'Fiscal do contrato'},
            {'ds_processo': 'Pagamento de faturas de águas, energia e telefonia', 'nr_atividade': 5, 'ds_atividade': 'Verificar conformidade do atesto', 'ds_responsavel': 'Coordenador de atividades gerais'},
            {'ds_processo': 'Pagamento de faturas de águas, energia e telefonia', 'nr_atividade': 6, 'ds_atividade': 'Verificar conformidade do processo', 'ds_responsavel': 'Gestor do contrato - Coordenador Geral da CGRL'},
            {'ds_processo': 'Pagamento de faturas de águas, energia e telefonia', 'nr_atividade': 7, 'ds_atividade': 'Distribuir processo de pagamento de fatura', 'ds_responsavel': 'Secretária da CGEOF'},
            {'ds_processo': 'Pagamento de faturas de águas, energia e telefonia', 'nr_atividade': 8, 'ds_atividade': 'Atribuir processo de pagamento de fatura', 'ds_responsavel': 'Chefe da divisão de análise CGEOG'},
            {'ds_processo': 'Pagamento de faturas de águas, energia e telefonia', 'nr_atividade': 9, 'ds_atividade': 'Analisar pagamento de fatura', 'ds_responsavel': 'Analista de processo CGEOF'},
            {'ds_processo': 'Pagamento de faturas de águas, energia e telefonia', 'nr_atividade': 10, 'ds_atividade': 'Assinar despacho de autorização de pagamento', 'ds_responsavel': 'Ordenador de despesas CGEOF'},
            {'ds_processo': 'Pagamento de faturas de águas, energia e telefonia', 'nr_atividade': 20, 'ds_atividade': 'Coordenar liberação financeira', 'ds_responsavel': 'Chefe da DPF/CFIN/CGOF'},
            {'ds_processo': 'Pagamento de faturas de águas, energia e telefonia', 'nr_atividade': 21, 'ds_atividade': 'Liberar Recurso Financeiro', 'ds_responsavel': 'Servidor da DPF/CFN/CGOF'},
            {'ds_processo': 'Pagamento de faturas de águas, energia e telefonia', 'nr_atividade': 22, 'ds_atividade': 'Registrar Ordem Bancária e Retenção de Tributos', 'ds_responsavel': 'Chefe de Divisão Financeira CGEOF'},
            {'ds_processo': 'Pagamento de faturas de águas, energia e telefonia', 'nr_atividade': 23, 'ds_atividade': 'Emitir Relação de Ordem Bancária', 'ds_responsavel': 'Responsável pela emissão de Ordem Bancária'},
            {'ds_processo': 'Pagamento de faturas de águas, energia e telefonia', 'nr_atividade': 24, 'ds_atividade': 'Assinar Ordem Bancária', 'ds_responsavel': 'Corresponsável pela Execução Financeira e Orçamentária'},
            {'ds_processo': 'Pagamento de faturas de águas, energia e telefonia', 'nr_atividade': 25, 'ds_atividade': 'Assinar Ordem Bancária', 'ds_responsavel': 'Ordenador de Despesas CGEOF'},
            {'ds_processo': 'Pagamento de faturas de águas, energia e telefonia', 'nr_atividade': 26, 'ds_atividade': 'Inserir PF no SIAR', 'ds_responsavel': 'Chefe de divisão financeira CGOEF'},
            {'ds_processo': 'Pagamento de faturas de águas, energia e telefonia', 'nr_atividade': 27, 'ds_atividade': 'Solicitar autorização de liberação de recursos financeiros', 'ds_responsavel': 'Servidor da DPF/CFN/CGOF'},
            {'ds_processo': 'Pagamento de faturas de águas, energia e telefonia', 'nr_atividade': 28, 'ds_atividade': 'Despachar Solicitação de autorização financeira', 'ds_responsavel': 'Chefe da DPF/CFN/CGOF'},
            {'ds_processo': 'Pagamento de faturas de águas, energia e telefonia', 'nr_atividade': 29, 'ds_atividade': 'Autorizar liberação financeira', 'ds_responsavel': 'Coordenador Financeiro CFN/CGOF'}
        ],
        "Risco": [
            {'ds_processo': 'Pagamento de faturas de águas, energia e telefonia', 'ds_atividade': 'Registrar liquidação no SIAFI', 'ds_probabilidade': 'Evento provavelmente ocorra na maioria das circunstâncias', 'ds_impacto': 'Impactos significativos, porém recuperáveis', 'ds_tipo_risco': 'Financeiros ou orçamentários', 'ds_risco': 'Financeiro insuficiente no momento da liquidação.'},
            {'ds_processo': 'Pagamento de faturas de águas, energia e telefonia', 'ds_atividade': 'Gerar programação finanaceira no SIAFI', 'ds_probabilidade': 'Evento pode ocorrer apenas em circunstâncias excepcionais', 'ds_impacto': 'Impactos pequenos', 'ds_tipo_risco': 'Financeiros ou orçamentários', 'ds_risco': 'Instruir incorretamente a Programação Financeira no SIAFI.'},
            {'ds_processo': 'Pagamento de faturas de águas, energia e telefonia', 'ds_atividade': 'Assinar recebimento da fatura física', 'ds_probabilidade': 'Evento pode ocorrer em algum momento', 'ds_impacto': 'Impactos significativos, porém recuperáveis', 'ds_tipo_risco': 'Operacionais', 'ds_risco': 'Não receber a fatura física.'},
            {'ds_processo': 'Pagamento de faturas de águas, energia e telefonia', 'ds_atividade': 'Instituir processo', 'ds_probabilidade': 'Evento deve ocorrer em algum momento', 'ds_impacto': 'Impactos significativos, porém recuperáveis', 'ds_tipo_risco': 'Operacionais', 'ds_risco': 'Saldo de empenho insuficiente para liquidação'},
            {'ds_processo': 'Pagamento de faturas de águas, energia e telefonia', 'ds_atividade': 'Registrar liquidação no SIAFI', 'ds_probabilidade': 'Evento pode ocorrer em algum momento', 'ds_impacto': 'Impactos significativos, porém recuperáveis', 'ds_tipo_risco': 'Financeiros ou orçamentários', 'ds_risco': 'Falta de encaminhamento das Propostas de Programação Financeira das Unidades Gestoras Executoras.'},
            {'ds_processo': 'Pagamento de faturas de águas, energia e telefonia', 'ds_probabilidade': 'Evento provavelmente ocorra na maioria das circunstâncias', 'ds_impacto': 'Impactos significativos, porém recuperáveis', 'ds_tipo_risco': 'Operacionais', 'ds_risco': 'Receber a fatura sem tempo hábil para pagamento.'},
            {'ds_processo': 'Pagamento de faturas de águas, energia e telefonia', 'ds_probabilidade': 'Evento pode ocorrer apenas em circunstâncias excepcionais', 'ds_impacto': 'Impactos pequenos', 'ds_tipo_risco': 'Operacionais', 'ds_risco': 'Não receber a fatura.'},
            {'ds_processo': 'Pagamento de faturas de águas, energia e telefonia', 'ds_atividade': 'Liberar Recurso Financeiro', 'ds_probabilidade': 'Evento pode ocorrer apenas em circunstâncias excepcionais', 'ds_impacto': 'Impactos de reversão muito difícil', 'ds_tipo_risco': 'Financeiros ou orçamentários', 'ds_risco': 'Inexistência de recursos financeiros na CGOF'},
            {'ds_processo': 'Pagamento de faturas de águas, energia e telefonia', 'ds_probabilidade': 'Evento provavelmente ocorra na maioria das circunstâncias', 'ds_impacto': 'Impactos significativos, porém recuperáveis', 'ds_tipo_risco': 'Operacionais', 'ds_risco': 'Digitalização Ilegível'},
            {'ds_processo': 'Pagamento de faturas de águas, energia e telefonia', 'ds_atividade': 'Emitir fatura via web', 'ds_probabilidade': 'Evento pode ocorrer apenas em circunstâncias excepcionais', 'ds_impacto': 'Impactos significativos, porém recuperáveis', 'ds_tipo_risco': 'Operacionais', 'ds_risco': 'Não emitir fatura pela web.'},
            {'ds_processo': 'Pagamento de faturas de águas, energia e telefonia', 'ds_atividade': 'Analisar Fatura', 'ds_probabilidade': 'Evento pode ocorrer em algum momento', 'ds_impacto': 'Impactos significativos, porém recuperáveis', 'ds_tipo_risco': 'Operacionais', 'ds_risco': 'Pagamento de valores indevidos relativos ao fornecimento de bens ou serviços'},
            {'ds_processo': 'Pagamento de faturas de águas, energia e telefonia', 'ds_atividade': 'Inserir PF no SIAR', 'ds_probabilidade': 'Evento deve ocorrer em algum momento', 'ds_impacto': 'Impactos de reversão muito difícil', 'ds_tipo_risco': 'Financeiros ou orçamentários', 'ds_risco': 'Falta de autorização para liberação financeira'},
            {'ds_processo': 'Pagamento de faturas de águas, energia e telefonia', 'ds_atividade': 'Elaborar programação financeira categorias gasto C e D vinc. 400', 'ds_probabilidade': 'Evento provavelmente ocorra na maioria das circunstâncias', 'ds_impacto': 'Impactos de reversão muito difícil', 'ds_tipo_risco': 'Financeiros ou orçamentários', 'ds_risco': 'Indisponibilidade de recursos financeiros.'},
            {'ds_processo': 'Pagamento de faturas de águas, energia e telefonia', 'ds_atividade': 'Emitir Relação de Ordem Bancária', 'ds_probabilidade': 'Evento pode ocorrer apenas em circunstâncias excepcionais', 'ds_impacto': 'Impactos de reversão muito difícil', 'ds_tipo_risco': 'Financeiros ou orçamentários', 'ds_risco': 'Impossibilidade de emissão da Relação de Ordem Bancária.'},
            {'ds_processo': 'Pagamento de faturas de águas, energia e telefonia', 'ds_probabilidade': 'Evento pode ocorrer apenas em circunstâncias excepcionais', 'ds_impacto': 'Impactos de reversão muito difícil', 'ds_tipo_risco': 'Financeiros ou orçamentários', 'ds_risco': 'Insuficiência de assinatura dos ordenadores de despesas exigidas.'},
            {'ds_processo': 'Pagamento de faturas de águas, energia e telefonia', 'ds_probabilidade': 'Evento pode ocorrer apenas em circunstâncias excepcionais', 'ds_impacto': 'Impactos de reversão muito difícil', 'ds_tipo_risco': 'Financeiros ou orçamentários', 'ds_risco': 'Atraso na assinatura de Ordem Bancária'},
            {'ds_processo': 'Pagamento de faturas de águas, energia e telefonia', 'ds_probabilidade': 'Evento pode ocorrer apenas em circunstâncias excepcionais', 'ds_impacto': 'Impactos de dificílima reversão', 'ds_tipo_risco': 'Financeiros ou orçamentários', 'ds_risco': 'Incorrer em sanções administrativas devido ao desrespeito injustificado da ordem cronológica de pagamento'},
            {'ds_processo': 'Pagamento de faturas de águas, energia e telefonia', 'ds_probabilidade': 'Evento pode ocorrer em algum momento', 'ds_impacto': 'Impactos significativos, porém recuperáveis', 'ds_tipo_risco': 'Operacionais', 'ds_risco': 'Falta de Saldo para Empenho'}
        ],
        "CausaConsequencia": [
            {'ds_risco': 'Financeiro insuficiente no momento da liquidação.', 'ds_tipo': 'Causa', 'ds_causa_consequencia': 'Priorização do pagamento de outras despesas.'},
            {'ds_risco': 'Financeiro insuficiente no momento da liquidação.', 'ds_tipo': 'Consequência', 'ds_causa_consequencia': 'Atraso na efetivação do pagamento.'},
            {'ds_risco': 'Instruir incorretamente a Programação Financeira no SIAFI.', 'ds_tipo': 'Causa', 'ds_causa_consequencia': 'Deficiência/ausência no treinamento dos técnicos responsáveis pela programação Fianceira.'},
            {'ds_risco': 'Instruir incorretamente a Programação Financeira no SIAFI.', 'ds_tipo': 'Consequência', 'ds_causa_consequencia': 'Atraso na efetivação do pagamento.'},
            {'ds_risco': 'Não receber a fatura física.', 'ds_tipo': 'Causa', 'ds_causa_consequencia': 'Ausência de Fiscal Substituto para receber a fatura'},
            {'ds_risco': 'Não receber a fatura física.', 'ds_tipo': 'Causa', 'ds_causa_consequencia': 'Fatura não foi entregue pela empresa'},
            {'ds_risco': 'Não receber a fatura física.', 'ds_tipo': 'Consequência', 'ds_causa_consequencia': 'Atraso no ateste do fornecimento do bem ou da prestação do serviço'},
            {'ds_risco': 'Saldo de empenho insuficiente para liquidação', 'ds_tipo': 'Causa', 'ds_causa_consequencia': 'Deficiência nos controles de empenhos por parte da unidade gestora do contrato.'},
            {'ds_risco': 'Saldo de empenho insuficiente para liquidação', 'ds_tipo': 'Consequência', 'ds_causa_consequencia': 'Atraso na condução do processo devido a exigência de reforço de empenho.'},
            {'ds_risco': 'Falta de encaminhamento das Propostas de Programação Financeira das Unidades Gestoras Executoras.', 'ds_tipo': 'Causa', 'ds_causa_consequencia': 'Falta de planejamento da unidade demandante.'},
            {'ds_risco': 'Falta de encaminhamento das Propostas de Programação Financeira das Unidades Gestoras Executoras.', 'ds_tipo': 'Causa', 'ds_causa_consequencia': 'Inobservância dos prazos legais. Desconhecimento de recursos financeiros disponíveis.'},
            {'ds_risco': 'Falta de encaminhamento das Propostas de Programação Financeira das Unidades Gestoras Executoras.', 'ds_tipo': 'Consequência', 'ds_causa_consequencia': 'Atraso na condução do processo de pagamento.'},
            {'ds_risco': 'Receber a fatura sem tempo hábil para pagamento.', 'ds_tipo': 'Causa', 'ds_causa_consequencia': 'Atraso dos Correios'},
            {'ds_risco': 'Receber a fatura sem tempo hábil para pagamento.', 'ds_tipo': 'Causa', 'ds_causa_consequencia': 'Atraso na postagem pela operadora'},
            {'ds_risco': 'Receber a fatura sem tempo hábil para pagamento.', 'ds_tipo': 'Consequência', 'ds_causa_consequencia': 'Pedido de prorrogação'},
            {'ds_risco': 'Não receber a fatura.', 'ds_tipo': 'Causa', 'ds_causa_consequencia': 'Falta de envio por parte da operadora'},
            {'ds_risco': 'Não receber a fatura.', 'ds_tipo': 'Causa', 'ds_causa_consequencia': 'Extravio por parte do Correio'},
            {'ds_risco': 'Não receber a fatura.', 'ds_tipo': 'Consequência', 'ds_causa_consequencia': 'Não pagamento da fatura'},
            {'ds_risco': 'Inexistência de recursos financeiros na CGOF', 'ds_tipo': 'Causa', 'ds_causa_consequencia': 'Secretaria do Tesouro  Nacional do Ministério da Fazenda não liberou recursos (Causa Externa);'},
            {'ds_risco': 'Inexistência de recursos financeiros na CGOF', 'ds_tipo': 'Causa', 'ds_causa_consequencia': 'Limite de pagamento do MAPA é insuficiente para receber recursos (Causa Externa)'},
            {'ds_risco': 'Inexistência de recursos financeiros na CGOF', 'ds_tipo': 'Causa', 'ds_causa_consequencia': 'CGOF não lançou no SIAFI a Proposta de Programação Financeira - PPF (Causa Interna).'},
            {'ds_risco': 'Inexistência de recursos financeiros na CGOF', 'ds_tipo': 'Consequência', 'ds_causa_consequencia': 'Não liberação de recursos financeiros às Unidades do MAPA'},
            {'ds_risco': 'Digitalização Ilegível', 'ds_tipo': 'Causa', 'ds_causa_consequencia': 'Baixa Qualidade dos Equipamentos'},
            {'ds_risco': 'Digitalização Ilegível', 'ds_tipo': 'Consequência', 'ds_causa_consequencia': 'Solicitação de fatura física para conferência'},
            {'ds_risco': 'Digitalização Ilegível', 'ds_tipo': 'Consequência', 'ds_causa_consequencia': 'Redigitalização da fatura ocasionando retrabalho'},
            {'ds_risco': 'Não emitir fatura pela web.', 'ds_tipo': 'Causa', 'ds_causa_consequencia': 'Website da empresa fornecedora inoperante.'},
            {'ds_risco': 'Não emitir fatura pela web.', 'ds_tipo': 'Consequência', 'ds_causa_consequencia': 'Dano ao erário'},
            {'ds_risco': 'Não emitir fatura pela web.', 'ds_tipo': 'Consequência', 'ds_causa_consequencia': 'Atraso no pagamento de fatura do mês referente'},
            {'ds_risco': 'Pagamento de valores indevidos relativos ao fornecimento de bens ou serviços', 'ds_tipo': 'Causa', 'ds_causa_consequencia': 'Inobservância de aspectos contratuais de fornecimento, ausência de check list sobre regras contratuais obrigatórias e aspectos similares'},
            {'ds_risco': 'Pagamento de valores indevidos relativos ao fornecimento de bens ou serviços', 'ds_tipo': 'Consequência', 'ds_causa_consequencia': 'Erro na análise do processo de pagamento, atraso no pagamento, retrabalho'},
            {'ds_risco': 'Falta de autorização para liberação financeira', 'ds_tipo': 'Causa', 'ds_causa_consequencia': 'Falta de treinamento adequado para operacionalização do SIAFI.'},
            {'ds_risco': 'Falta de autorização para liberação financeira', 'ds_tipo': 'Consequência', 'ds_causa_consequencia': 'Atraso na condução do processo de pagamento.'},
            {'ds_risco': 'Falta de autorização para liberação financeira', 'ds_tipo': 'Consequência', 'ds_causa_consequencia': 'Retrabalho.'},
            {'ds_risco': 'Indisponibilidade de recursos financeiros.', 'ds_tipo': 'Causa', 'ds_causa_consequencia': 'Contigenciamento por parte do Tesouro Nacional.'},
            {'ds_risco': 'Indisponibilidade de recursos financeiros.', 'ds_tipo': 'Consequência', 'ds_causa_consequencia': 'Atraso na efetivação do pagamento.'},
            {'ds_risco': 'Impossibilidade de emissão da Relação de Ordem Bancária.', 'ds_tipo': 'Causa', 'ds_causa_consequencia': 'Inoperância do SIAFI.'},
            {'ds_risco': 'Impossibilidade de emissão da Relação de Ordem Bancária.', 'ds_tipo': 'Consequência', 'ds_causa_consequencia': 'Atraso na condução do processo de pagamento.'},
            {'ds_risco': 'Insuficiência de assinatura dos ordenadores de despesas exigidas.', 'ds_tipo': 'Causa', 'ds_causa_consequencia': 'Inobservância às autorizações necessárias.'},
            {'ds_risco': 'Insuficiência de assinatura dos ordenadores de despesas exigidas.', 'ds_tipo': 'Causa', 'ds_causa_consequencia': 'Ausência do(s) autorizador(es).'},
            {'ds_risco': 'Insuficiência de assinatura dos ordenadores de despesas exigidas.', 'ds_tipo': 'Consequência', 'ds_causa_consequencia': 'Atraso na condução do processo de pagamento.'},
            {'ds_risco': 'Atraso na assinatura de Ordem Bancária', 'ds_tipo': 'Causa', 'ds_causa_consequencia': 'Exigência da assinatura de mais de um ordenador de despesa.'},
            {'ds_risco': 'Atraso na assinatura de Ordem Bancária', 'ds_tipo': 'Consequência', 'ds_causa_consequencia': 'Atraso no envio da autorização de pagamento à Instituição Financeira.'},
            {'ds_risco': 'Incorrer em sanções administrativas devido ao desrespeito injustificado da ordem cronológica de pagamento', 'ds_tipo': 'Causa', 'ds_causa_consequencia': 'Inobservância dos aspectos descritos na IN 02/2016/MP, especificamente no artigo 5° primeiro parágrafo.'},
            {'ds_risco': 'Incorrer em sanções administrativas devido ao desrespeito injustificado da ordem cronológica de pagamento', 'ds_tipo': 'Consequência', 'ds_causa_consequencia': 'Responsabilização administrativa e/ou penal, conforme previsto no art. 92 da Lei nº 8.666/93, bem como outras sanções legais cabíveis.'},
            {'ds_risco': 'Falta de Saldo para Empenho', 'ds_tipo': 'Causa', 'ds_causa_consequencia': 'Valor estimado insuficiente.'},
            {'ds_risco': 'Falta de Saldo para Empenho', 'ds_tipo': 'Consequência', 'ds_causa_consequencia': 'Atraso na instrução do processo devido a solicitação de reforço'}
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

    for values in populate["Processo"]:
        link = models.Macroprocesso.objects.filter(ds_macroprocesso=values["ds_macroprocesso"])[0]
        u = models.Processo.objects.get_or_create(
            id_macroprocesso=link, ds_processo=values["ds_processo"], ds_usuario=ds_usuario)
        if u[1] == True:
            u[0].save()

    print("[DATABASE] Processo populated!")

    for values in populate["Atividade"]:
        link = models.Processo.objects.filter(ds_processo=values["ds_processo"])[0]
        u = models.Atividade.objects.get_or_create(
            id_processo=link, ds_atividade=values["ds_atividade"], ds_usuario=ds_usuario,
            ds_responsavel=values["ds_responsavel"], nr_atividade=values["nr_atividade"])
        if u[1] == True:
            u[0].save()

    print("[DATABASE] Atividade populated!")

    for values in populate["Risco"]:
        link = models.Processo.objects.filter(ds_processo=values["ds_processo"])[0]
        link2 = models.Probabilidade.objects.filter(ds_probabilidade=values["ds_probabilidade"])[0]
        link3 = models.Impacto.objects.filter(ds_impacto=values["ds_impacto"])[0]
        link4 = models.Tipo_Risco.objects.filter(ds_tipo_risco=values["ds_tipo_risco"])[0]
        if "ds_atividade" in values.keys():
            link5 = models.Atividade.objects.filter(ds_atividade=values["ds_atividade"])[0]
            u = models.Risco.objects.get_or_create(
                id_processo=link, id_atividade=link5, id_probabilidade=link2, id_impacto=link3,
                ds_risco=values["ds_risco"], id_tipo_risco=link4, ds_usuario=ds_usuario)
        else:
            u = models.Risco.objects.get_or_create(
                id_processo=link, id_probabilidade=link2, id_impacto=link3,
                ds_risco=values["ds_risco"], id_tipo_risco=link4, ds_usuario=ds_usuario)
        if u[1] == True:
            u[0].save()

    print("[DATABASE] Risco populated!")

    for values in populate["CausaConsequencia"]:
        link = models.Risco.objects.filter(ds_risco=values["ds_risco"])[0]
        u = models.CausaConsequencia.objects.get_or_create(
            id_risco=link, ds_causa_consequencia=values["ds_causa_consequencia"],
            ds_tipo=values["ds_tipo"], ds_usuario=ds_usuario)
        if u[1] == True:
            u[0].save()

    print("[DATABASE] CausaConsequencia populated!")

    print("[DATABASE] Done.")

    sys.exit(0)


if __name__ == '__main__':
    django.setup()
    populate()
