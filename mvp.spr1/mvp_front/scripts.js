/*
  --------------------------------------------------------------------------------------
  Função para obter a lista existente do servidor via requisição GET
  --------------------------------------------------------------------------------------
*/

const getList = async () => {
  let url = 'http://127.0.0.1:5000/leads';
  fetch(url, {
    method: 'get',
  })
    .then((response) => response.json())
    .then((data) => {
      data.leads.forEach(lead => insertList(lead.nome, lead.idade, lead.genero, lead.cidade_residencia, lead.grau_formacao, lead.curso_formacao))
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}


/*
  --------------------------------------------------------------------------------------
  Chamada da função para carregamento inicial dos dados
  --------------------------------------------------------------------------------------
*/
getList()


/*
  --------------------------------------------------------------------------------------
  Função para colocar um lead na lista do servidor via requisição POST
  --------------------------------------------------------------------------------------
*/
const postLead = async (inputInput, inputQuantity, inputGender, inputCity, inputForm, inputCourse) => {
  const formData = new FormData();
  formData.append('nome', inputInput);
  formData.append('idade', inputQuantity);
  formData.append('genero', inputGender);
  formData.append('cidade_residencia', inputCity);
  formData.append('grau_formacao', inputForm);
  formData.append('curso_formacao', inputCourse);

  let url = 'http://127.0.0.1:5000/lead';
  fetch(url, {
    method: 'post',
    body: formData
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error:', error);
    });
}


/*
  --------------------------------------------------------------------------------------
  Função para criar um botão close para cada lead da lista
  --------------------------------------------------------------------------------------
*/
const insertButton = (parent) => {
  let span = document.createElement("span");
  let txt = document.createTextNode("\u00D7");
  span.className = "close";
  span.appendChild(txt);
  parent.appendChild(span);
}


/*
  --------------------------------------------------------------------------------------
  Função para remover um lead da lista de acordo com o click no botão close
  --------------------------------------------------------------------------------------
*/
const removeElement = () => {
  let close = document.getElementsByClassName("close");
  // var table = document.getElementById('myTable');
  let i;
  for (i = 0; i < close.length; i++) {
    close[i].onclick = function () {
      let div = this.parentElement.parentElement;
      const nomeLead = div.getElementsByTagName('td')[0].innerHTML
      if (confirm("Você tem certeza?")) {
        div.remove()
        deleteLead(nomeLead)
        alert("Removido!")
      }
    }
  }
}

/*
  --------------------------------------------------------------------------------------
  Função para deletar um lead da lista do servidor via requisição DELETE
  --------------------------------------------------------------------------------------
*/
const deleteLead = (lead) => {
  console.log(lead)
  let url = 'http://127.0.0.1:5000/lead?nome=' + lead;
  fetch(url, {
    method: 'delete'
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
  --------------------------------------------------------------------------------------
  Função para adicionar um novo lead com seus respectivos atributos 
  --------------------------------------------------------------------------------------
*/
const newLead = () => {
  let inputInput = document.getElementById("newInput").value;
  let inputQuantity = document.getElementById("newQuantity").value;
  let inputGender = document.getElementById("newGender").value;
  let inputCity = document.getElementById("newCity").value;
  let inputForm = document.getElementById("newForm").value;
  let inputCourse = document.getElementById("newCourse").value;

  if (inputInput === '') {
    alert("Escreva o seu nome");
  } else if (isNaN(inputQuantity)) {
    alert("Idade precisa ser preenchida em números!");
  } else if (inputGender === '') {
    alert("Preencha com o gênero ou informe que não deseja responder");
  } else if (inputCity === '') {
    alert("Preencha com a cidade de sua residência atual");
  } else if (inputForm === '') {
    alert("Preencha com seu grau de escolaridade");
  } else if (inputCourse === '') {
    alert("Preencha com o curso da sua formação de maior grau");
  } else {
    insertList(inputInput, inputQuantity, inputGender, inputCity, inputForm, inputCourse)
    postItem(inputInput, inputQuantity, inputGender, inputCity, inputForm, inputCourse)
    alert("Dados adicionados com sucesso!")
  }
}

/*
  --------------------------------------------------------------------------------------
  Função para inserir leads na lista apresentada
  --------------------------------------------------------------------------------------
*/
const insertList = (nameInput, quantity, gender, city, form, course) => {
  var lead = [nameInput, quantity, gender, city, form, course]
  var table = document.getElementById('myTable');
  var row = table.insertRow();

  for (var i = 0; i < lead.length; i++) {
    var cel = row.insertCell(i);
    cel.textContent = lead[i];
  }
  insertButton(row.insertCell(-1))
  document.getElementById("newInput").value = "";
  document.getElementById("newQuantity").value = "";
  document.getElementById("newGender").value = "";
  document.getElementById("newCity").value = "";
  document.getElementById("newForm").value = "";
  document.getElementById("newCourse").value = "";

  removeElement()
}