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
 Função para criar um botão de edição para cada lead da lista
 --------------------------------------------------------------------------------------
*/
const insertEditButton = (parent) => {
  let button = document.createElement("button");
  button.textContent = "Editar";
  button.className = "edit";
  parent.appendChild(button);
  button.addEventListener('click', editLeadRow);
}

/*
 --------------------------------------------------------------------------------------
 Função para habilitar a edição de uma linha da tabela
 --------------------------------------------------------------------------------------
*/
function editLeadRow() {
  const row = this.parentNode.parentNode;
  const cells = row.querySelectorAll('td:not(:last-child)');
  // Seleciona todas as células, exceto as de ação
  const originalData = Array.from(cells).map(cell => cell.textContent);

  // Transforma as células em campos de input
  cells.forEach(cell => {
    if (!cell.classList.contains('actions')) {
      // Evita editar as células de ação
      const input = document.createElement('input');
      input.type = 'text';
      input.value = cell.textContent;
      cell.textContent = '';
      cell.appendChild(input);
    }
  });

  // Remove os botões "Editar" e "Excluir"
  const editCell = row.querySelector('td.edit-action');
  const deleteCell = row.querySelector('td.delete-action');
  editCell.innerHTML = '';
  deleteCell.innerHTML = '';

  // Adiciona botões "Salvar" e "Cancelar"
  const saveButton = document.createElement('button');
  saveButton.textContent = 'Salvar';
  saveButton.addEventListener('click', () => saveEditedLead(row, originalData));
  editCell.appendChild(saveButton);

  const cancelButton = document.createElement('button');
  cancelButton.textContent = 'Cancelar';
  cancelButton.addEventListener('click', () => cancelEdit(row, originalData));
  editCell.appendChild(cancelButton);
}

/*
 --------------------------------------------------------------------------------------
 Função para cancelar a edição de uma linha
 --------------------------------------------------------------------------------------
*/
function cancelEdit(row, originalData) {
  const cells = row.querySelectorAll('td:not(:last-child)');
  cells.forEach((cell, index) => {
    if (!cell.classList.contains('actions')) {
      // Evita restaurar as células de ação
      cell.textContent = originalData[index];
    }
  });

  const editCell = row.querySelector('td.edit-action');
  const deleteCell = row.querySelector('td.delete-action');
  editCell.innerHTML = '';
  deleteCell.innerHTML = '';
  insertEditButton(editCell);
  insertDeleteButton(deleteCell);
}

/*
 --------------------------------------------------------------------------------------
 Função para salvar o lead editado no frontend e enviar a atualização para o backend
 --------------------------------------------------------------------------------------
*/
const saveEditedLead = async (row, originalData) => {
  const cells = row.querySelectorAll('td:not(:last-child)');
  const updatedData = Array.from(cells).map(cell => cell.querySelector('input')?.value || cell.textContent);
  // Pega o valor do input ou o texto existente
  const nomeOriginal = originalData[0];
  // Assume que o nome é a primeira coluna e é usado para identificar o lead

  const [nome, idade, genero, cidade_residencia, grau_formacao, curso_formacao] = updatedData;

  if (confirm("Salvar as alterações?")) {
    // Atualiza a tabela no frontend
    cells.forEach((cell, index) => {
      if (!cell.classList.contains('actions')) {
        cell.textContent = updatedData[index];
      }
    });

    // Envia a requisição PUT para o backend
    let url = `http://127.0.0.1:5000/lead/${encodeURIComponent(nomeOriginal)}`;
    const data = {
    nome: nome,
    idade: idade,
    genero: genero,
    cidade_residencia: cidade_residencia,
    grau_formacao: grau_formacao,
    curso_formacao: curso_formacao
  };

  fetch(url, {
    method: 'put',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data),
  })
      .then((response) => {
        if (!response.ok) {
          return response.json().then(err => { throw err; });
        }
        return response.json();
      })
      .then((data) => {
        alert(`Lead "${nomeOriginal}" atualizado para "${nome}" com sucesso!`);
        // Atualiza os botões da linha após a edição
        const editCell = row.querySelector('td.edit-action');
        const deleteCell = row.querySelector('td.delete-action');
        editCell.innerHTML = '';
        deleteCell.innerHTML = '';
        insertEditButton(editCell);
        insertDeleteButton(deleteCell);
      })
      .catch((error) => {
        console.error('Error:', error);
        alert(`Erro ao atualizar o lead "${nomeOriginal}": ${error.message || 'Erro desconhecido'}`);
        // Reverte a tabela para os dados originais em caso de erro
        cells.forEach((cell, index) => {
          if (!cell.classList.contains('actions')) {
            cell.textContent = originalData[index];
          }
        });
        const editCell = row.querySelector('td.edit-action');
        const deleteCell = row.querySelector('td.delete-action');
        editCell.innerHTML = '';
        deleteCell.innerHTML = '';
        insertEditButton(editCell);
        insertDeleteButton(deleteCell);
      });
  } else {
    // Cancela a edição se o usuário não confirmar
    cancelEdit(row, originalData);
  }
};


/*
  --------------------------------------------------------------------------------------
  Função para criar um botão close para cada lead da lista
  --------------------------------------------------------------------------------------
*/
const insertDeleteButton = (parent) => {
  let span = document.createElement("span");
  let txt = document.createTextNode("\u00D7");
  span.className = "close";
  span.appendChild(txt);
  parent.appendChild(span);
  span.addEventListener('click', removeElement);
}


/*
  --------------------------------------------------------------------------------------
  Função para remover um lead da lista de acordo com o click no botão close
  --------------------------------------------------------------------------------------
*/
const removeElement = function () {
  let div = this.parentElement.parentElement;
  const nomeLead = div.getElementsByTagName('td')[0].innerHTML
  if (confirm("Você tem certeza?")) {
    div.remove()
    deleteLead(nomeLead)
    alert("Removido!")
  }
}

/*
  --------------------------------------------------------------------------------------
  Função para deletar um lead da lista do servidor via requisição DELETE
  --------------------------------------------------------------------------------------
*/
const deleteLead = (lead) => {
  console.log(lead)
  let url = 'http://127.0.0.1:5000/lead?nome=' + encodeURIComponent(lead);
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
    postLead(inputInput, inputQuantity, inputGender, inputCity, inputForm, inputCourse)
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
  const editCell = row.insertCell(-1);
  editCell.classList.add('edit-action');
  const deleteCell = row.insertCell(-1);
  deleteCell.classList.add('delete-action');
  insertEditButton(editCell);
  insertDeleteButton(deleteCell);
}

/*
  --------------------------------------------------------------------------------------
  Função para obter a lista existente do servidor via requisição GET
  --------------------------------------------------------------------------------------
*/

const getProducts = async () => {
  let url = 'https://fakestoreapi.com/products';
  fetch(url, {
    method: 'get',
  })
    .then((response) => response.json())
    .then((data) => {
      // console.log(data);
      data.forEach(item => insertProductCard(item))
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
  --------------------------------------------------------------------------------------
  Função para obter a lista existente do servidor via requisição GET
  --------------------------------------------------------------------------------------
*/

const getProductsLocal = async () => {  
  let url = 'http://localhost:5000/produtos';     
  fetch(url, {
    method: 'get',
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      // data.forEach(item => insertCard(item))
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
getProductsLocal()

getProducts()

/*
  --------------------------------------------------------------------------------------
  Função para inserir items na lista apresentada
  --------------------------------------------------------------------------------------
*/
const insertProductCard = (product) => {
  var section = document.getElementById('products-list');
  let article = document.createElement('article');
  article.setAttribute('class','product');
  article.setAttribute('id', product.id);

  let img = document.createElement('img');
  img.setAttribute('src', product.image);
  img.setAttribute('alt', 'Não foi possível carregar a imagem do produto');
  
  let h3 = document.createElement('h3');
  h3.setAttribute('class', 'price-product');
  let span = document.createElement('span');
  span.innerHTML = 'R$ ' + product.price;
  h3.appendChild(span);

  let p = document.createElement('p');
  p.setAttribute('class', 'name-product');
  p.innerHTML = product.title;

  let button = document.createElement('button');
  button.setAttribute('class', 'buy-product');
  button.setAttribute('type', 'button');
  button.setAttribute('id', product.id);
  button.innerHTML = 'Comprar';

  article.appendChild(img);
  article.appendChild(h3);
  article.appendChild(p);
  article.appendChild(button);
  section.appendChild(article);
}