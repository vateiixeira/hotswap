var vm = new Vue({
  el: "#app",
  delimiters: ["[", "]"],
  data: {
    message: "adsadasd",
    novoChamado: false,
    id: "",
    setor: "",
    loja: "",
    user: "",
    issue: "",
    solicitante: "",
    atendimentos: null,
    lista: null,
    concluidoShow: false,
    listConcluido: [],
    listPendente: [],
    listCancelado: [],
    semDados: false
  },
  mounted() {
    this.id = document.getElementById("id").innerHTML;
    axios
      .get(`http://localhost:8000/api/helpdesk/usuario/${this.id}`)
      .then(function (response) {
        console.log(response);
        this.setor = response.data.setor;
        this.loja = response.data.loja;
        this.user = response.data.user;
        axios
          .get(`http://127.0.0.1:8000/api/helpdesk/lista`, {
            params: {
              loja: this.loja,
              setor: this.setor,
            },
          })
          .then(function (response) {
            console.log(response.data);
            this.atendimentos = response.data;
          })
          .catch(function (error) {
            console.log(error);
          });
      })
      .catch(function (error) {
        console.log(error);
      });
    // axios.get(`http://127.0.0.1:8000/api/helpdesk/lista`,
    // {
    //     params: {
    //         'loja': vm.loja,
    //         'setor' : vm.setor
    //     }
    // })
    // .then(function (response) {
    //     console.log(response)
    // })
    // .catch(function (error) {
    //     console.log(error)
    // })
  },
  methods: {
    submita: () => {
      console.log(this.problema);
      axios
        .post(`http://localhost:8000/api/helpdesk/novo/atendimento`, {
          setor: this.setor,
          loja: this.loja,
          user: this.user,
          problema: vm.issue,
          solicitante: vm.solicitante,
        })
        .then(function (response) {
          console.log(response);
          vm.issue = "";
          vm.solicitante = "";
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    pendente: () => {    
        var lista = vm.atendimentos.filter(function (el) {
            return el.status == "p";
        });
        if (lista.length <= 0 ) {
            vm.concluidoShow = false
            vm.semDados = true
        } else {
            vm.concluidoShow = true
            console.log(lista);
            vm.listConcluido = lista;
        }
    },
    cancelado: () => {
        var lista = this.atendimentos.filter(function (el) {
            return el.status == "o";
        });
        if (lista.length <= 0 ) {
            vm.concluidoShow = false
            vm.semDados = true
        } else {
            vm.concluidoShow = true
            console.log(lista);
            vm.listConcluido = lista;
        }
    },
    concluido: () => {
        var lista = this.atendimentos.filter(function (el) {
            return el.status == "r";
        });
        if (lista.length <= 0 ) {
            vm.concluidoShow = false
            vm.semDados = true
        } else {
            vm.concluidoShow = true            
            console.log(lista);
            vm.listConcluido = lista;
        }
    },
    novo: function (event) {
      vm.concluidoShow = false
      vm.semDados = false
      vm.novoChamado = !vm.novoChamado;
    },
  },
});