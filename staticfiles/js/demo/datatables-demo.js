$(document).ready(function () {
  $('#dataTable').DataTable({
    "language": {
      "info": "Mostrando pag. _PAGE_ de _PAGES_",
      "infoEmpty": "Sem dados para mostrar",
      "lengthMenu": "Mostrando _MENU_ registros",
      "search": "Buscar:",
      "zeroRecords": "Não foram encontrados registros",
      "paginate": {
        "previous": "Anterior",
        "next": "Seguinte"
      }

    }
  });
});

$(document).ready(function () {
  $('#dataTable_pendente_atendimento').DataTable({
    "order": [
      [8, "desc"]
    ],
    "language": {
      "info": "Mostrando pag. _PAGE_ de _PAGES_",
      "infoEmpty": "Sem dados para mostrar",
      "lengthMenu": "Mostrando _MENU_ registros",
      "search": "Buscar:",
      "zeroRecords": "Não foram encontrados registros",
      "paginate": {
        "previous": "Anterior",
        "next": "Seguinte"
      }

    }
  });
});

$(document).ready(function () {
  $('#dataTable_atendimento').DataTable({
    "order": [
      [8, "desc"]
    ],
    "language": {
      "info": "Mostrando pag. _PAGE_ de _PAGES_",
      "infoEmpty": "Sem dados para mostrar",
      "lengthMenu": "Mostrando _MENU_ registros",
      "search": "Buscar:",
      "zeroRecords": "Não foram encontrados registros",
      "paginate": {
        "previous": "Anterior",
        "next": "Seguinte"
      }

    }
  });
});

$(document).ready(function () {
  $('#dataTableEnvio').DataTable({
    "order": [
      [0, "desc"]
    ],
    "language": {
      "info": "Mostrando pag. _PAGE_ de _PAGES_",
      "infoEmpty": "Sem dados para mostrar",
      "lengthMenu": "Mostrando _MENU_ registros",
      "search": "Buscar:",
      "zeroRecords": "Não foram encontrados registros",
      "paginate": {
        "previous": "Anterior",
        "next": "Seguinte"
      }

    }
  });
});