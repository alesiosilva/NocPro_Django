function atualizaTabChamados(){
    //console.log(id);
    token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    fila = document.getElementsByName("filtro_filas")[0].value;

    $("#tab_lista_chamados tbody").empty();

    $.ajax({
        type: 'POST',
        //type: 'GET',
        url: '/topdesk/lista_chamados',
        //url: '/topdesk/lista_chamados/' + fila + '/',
        data: {
            csrfmiddlewaretoken: token,
            fila: fila
        },
        success: function(result){
            //console.log('teste');
            //$("#mensagem").text(result);

            for(var result_cont in result){
                //$("#mensagem").text(result[result_cont].id);
                var row = '<tr>'
                var row = row + '<td><input type="checkbox" id="alterar" name="alterar" value="' + result[result_cont].id + '"></td>'
                var row = row + '<td>' + result[result_cont].number + '</td>'
                var row = row + '<td>' + result[result_cont].briefDescription + '</td>'
                var row = row + '<td>' + result[result_cont].processingStatus.name + '</td>'
                var row = row + '</tr>'
                $("#tab_lista_chamados tbody").append(row);

            }
        }
      }
    );
}