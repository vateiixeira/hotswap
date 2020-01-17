$(document).ready( function() {
      $('#dataTable').DataTable( {
        "scrollY": "true",
        "scroller": {
            "rowHeight": 300 },
        "orderFixed": [ 0, 'desc' ],
        "language": {
          "info": "Mostrando pag. _PAGE_ de _PAGES_",
          "infoEmpty": "Sem dados para mostrar",
          "lengthMenu": "Mostrando _MENU_ registros",
          "search": "Buscar:",
          "zeroRecords": "Não foram encontrados registros",
          "paginate":{
            "previous": "fuckoff",
            "next": "fuckoff"
          }
          
        }
      } );
    } );

