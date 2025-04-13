am# Minha API

Este pequeno projeto é o trabalho final da Disciplina **Desenvolvimento Full Stack Básico** 

O objetivo aqui é demonstrar o aprendizado obtido a partir das aulas.

O projeto se baseia em um projeto real que precisarei tocar durante o ano de 2025. Utilizei o trabalho final como ponto de partida para o que desejo fazer com maior complexidade em um futuro breve.
Durante a evolução, pretendo trocar a SPA por uma aplicação de várias páginas e trocar o fundo estático (imagem) por uma elaboração no HTML + CSS, com as logos em seus devidos lugares e capazes de estabelecer rotas entre as diferentes páginas.
Outra coisa que será modificada será a troca das tabelas por páginas específicas. Elas serão (2):
1) o formulário de preenchimento dos dados se tornará um cadastro de página própria acessado por link na página inicial.
2) haverá a opção de buscar um usuário no lugar da tabela de exibição. A busca também estará em página própria.
Na página de busca, no futuro, o usuário terá opções de edição (POST) e de deletar (DELETE) um usuário que encontrar.
Todavia, a visualização dos dados não estará presente por default. O usuário só poderá ver quem conseguir encontrar (pela busca) fornecendo os principais dados armazenados.
Isso significa que, nesse momento, o usuário só poderá deletar ou editar os dados de usuário que ele já conhece, ou seja, os dele próprio. A não ser que o usuário seja alguém com acesso ao banco, que vê todos, no caso, necessariamente um adm.

---
## Como executar 


Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
(amb_api)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

```
(amb_api)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(amb_api)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.
