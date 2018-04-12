function ajaxForm(targetElementId, onChangeElementId, onChangeElementsToHide, onChangeFormId, dataUrlAttr) {
    $(targetElementId + " option:not(:first-child)").remove();
    $(onChangeElementId).change(function() {
        var url = $(onChangeFormId).attr(dataUrlAttr); // Pega a url do Form
        var targetId = $(this).val(); // Pega o Id da opção

        if (targetId == "") {
            for (var i = 0; i < onChangeElementsToHide.length; i++) { // Se o ID for 0 (nada) remover as opções
                $(onChangeElementsToHide[i] + " option:not(:first-child)").remove();
            }
        } else {
            for (var i = 0; i < onChangeElementsToHide.length; i++) { // Se o ID mudar remover as opções
                $(onChangeElementsToHide[i] + " option:not(:first-child)").remove();
            }
            $.ajax({ // Inicia o AJAX request
                url: url, // Estabelece a url de consulta
                data: {
                    'targetId': targetId // Adiciona o ID para o parâmetro GET
                },
                success: function(data) { // `data` é o retorno da url de consulta
                    $(targetElementId).html(data); // Substitui os opções pelo resultado da consulta
                }
            });
        }
    });
};