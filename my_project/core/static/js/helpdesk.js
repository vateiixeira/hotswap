Vue.use(Toasted)
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
    semDados: false,
    prodUrl: 'http://192.168.0.238',
    devdUrl: 'http://127.0.0.1:8000'
  },
  mounted() {
    this.id = document.getElementById("id").innerHTML;
    console.log(`http://http://192.168.0.238/api/helpdesk/usuario/${this.id}`)
    axios
      .get(`http://http://192.168.0.238/api/helpdesk/usuario/${this.id}`)
      .then(function (response) {
        this.setor = response.data.setor;
        this.loja = response.data.loja;
        this.user = response.data.user;
        axios
          .get(`http://http://192.168.0.238/api/helpdesk/lista`, {
            params: {
              loja: this.loja,
              setor: this.setor,
            },
          })
          .then(function (response) {
            vm.atendimentos = response.data;
          })
          .catch(function (error) {
            console.log(error);
          });
      })
      .catch(function (error) {
        console.log(error);
      });
    // axios.get(`http://http://192.168.0.238/api/helpdesk/lista`,
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
      axios.defaults.xsrfCookieName = 'csrftoken'
      axios.defaults.xsrfHeaderName = "X-CSRFTOKEN",
        axios
        .post(`http://http://192.168.0.238/api/helpdesk/novo/atendimento`, {
          setor: this.setor,
          loja: this.loja,
          user: this.user,
          problema: vm.issue,
          solicitante: vm.solicitante,
        })
        .then(function (response) {
          console.log(response.data);
          vm.issue = "";
          vm.solicitante = "";
          vm.$toasted.show('Chamado aberto com sucesso!!', {
            theme: 'outline',
            duration: 5000,
            type: 'success'
          })
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    pendente: function () {
      var lista = vm.atendimentos.filter(function (el) {
        return el.status == "p";
      });
      if (lista.length <= 0) {
        vm.concluidoShow = false
        vm.semDados = true
        vm.novoChamado = false
      } else {
        vm.concluidoShow = true
        vm.novoChamado = false
        vm.listConcluido = lista;
      }
    },
    cancelado: () => {
      var lista = vm.atendimentos.filter(function (el) {
        return el.status == "o";
      });
      if (lista.length <= 0) {
        vm.concluidoShow = false
        vm.semDados = true
        vm.novoChamado = false
      } else {
        vm.concluidoShow = true
        vm.novoChamado = false
        vm.listConcluido = lista;
      }
    },
    concluido: () => {
      var lista = vm.atendimentos.filter(function (el) {
        return el.status == "r";
      });
      if (lista.length <= 0) {
        vm.concluidoShow = false
        vm.semDados = true
        vm.novoChamado = false
      } else {
        vm.concluidoShow = true
        vm.novoChamado = false
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