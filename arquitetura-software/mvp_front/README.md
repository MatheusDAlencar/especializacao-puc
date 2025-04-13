# Meu Front

Este pequeno projeto é o trabalho final da Disciplina **Desenvolvimento Full Stack Avançado** 

O objetivo aqui é demonstrar o aprendizado obtido a partir das aulas.

O projeto se baseia em um projeto real que precisarei tocar durante o ano de 2025. Utilizei o trabalho final como ponto de partida
para o que desejo fazer com maior complexidade no futuro. Durante a evolução, pretendo trocar a SPA por uma aplicação de várias
páginas, com login, rotas entre as diferentes páginas etc. Por ora, a SPA foi suficiente para atingir o objetivo.

Entre o MVP Full Stack Básico e o MVP Full Stack Avançado, foram realizadas algumas mudanças:
1) Inserção da função de edição no meu frontend, para finalmente permitir edição dos dados de Leads;
2) Containerização do front utilizando o Dockerfile;
3) Troca do fundo estático (imagem) por uma elaboração no HTML + CSS, com a logo em seu devido lugar;
4) Conexão com o Backend e seu banco de dados, permitindo a persistência dos dados;
5) Conexão com a API externa Fake Store, disponível em: https://fakestoreapi.com/

A API externa atualmente preenche o front end. A interação com ela, além do preenchimento, é de edição de todos os cards de venda
e adequação ao navegador do usuário. A API é 100% gratuita e não precisa de licença de uso ou cadastro. As rotas estão declaradas
no arquivo JavaScript, a previsão de aparição no frontend está no HTML e a interação com os dados e cards está no CSS. 
No futuro, a intenção é que essa disposição dos itens à venda se torne uma única fila, em carrossel, além de permitir o registro
das compras via site, que gerarão descontos para os clientes, incentivando o acesso ao site e o ganho em marketing orgânico.

Sobre a arquitetura de software, como se percebe, o frontend é a página principal, que conecta API externa e API autoral.
Já a API autoral é o que se liga ao banco de dados, garantindo a persistência dos dados. Visualmente, ficou assim:

![Arquitetura](src\img\Arquitetura.jpg)

Importante ressalvar que o frontend tem relação de dependência com a função PUT do backend. A SPA não consegue modificar os dados
do Lead sem a validação de verdade no banco de dados, o que só ocorre quando a função PUT está ativa e funcional.
Todavia, o front não vai quebrar se o backend não estiver funcionando, somente não vai funcionar a função de edição do Lead.

Para o futuro, pretendo modificar muito mais coisas, acompanhando o aprendizado. Algumas mudanças já idealizadas:
1) a API externa que atualmente é a Fake Store será substituída pelos links reais de itens à venda,
    em especial os cursos disponibilizados (Hotmart) e os livros dos professores, dispostos em livrarias distintas,
    o que vai exigir algum trabalho a mais de curadoria do que será puxado;
2) inserir outra API externa, agora do YouTube, para que os vídeos do canal fiquem disponíveis na página principal;
3) o formulário de preenchimento dos dados se tornará um cadastro de página própria acessado por link na página inicial;
4) o cadastro exigirá login e senha, estipulando um nível de acesso para usuários distintos, no caso Lead e Administrador;
5) o Lead somente poderá ver seus dados e usar as funções hoje já disponíveis na tabela (inserir, deletar e corrigir);
6) já os Administradores terão opções de buscar um usuário qualquer por campo, baixar carga de dados e usar as mesmas funções acima;
7) inserir informações sobre quem são os professores na página inicial e os Contatos no rodapé;
8) com isso, a página principal terá foco somente na apresentação do conteúdo, dos professores e dos cursos e outros produtos à venda. 


---
## Como executar em modo de desenvolvimento

Basta fazer o download do projeto e abrir o arquivo index.html no seu browser.

## Como executar através do Docker

Certifique-se de ter o [Docker](https://docs.docker.com/engine/install/) instalado e em execução em sua máquina.

Navegue até o diretório que contém o Dockerfile no terminal e seus arquivos de aplicação e
Execute **como administrador** o seguinte comando para construir a imagem Docker:

```
$ docker build -t mvp_front .
```

Uma vez criada a imagem, para executar o container basta executar, **como administrador**, seguinte o comando:

```
$ docker run -d -p 8080:80 mvp_front
```

Uma vez executando, para acessar o front-end, basta abrir o [http://localhost:8080/#/](http://localhost:8080/#/) no navegador.

### ATENÇÃO: para melhor funcionamento do projeto como um todo através do Docker, é aconselhável primeiro criar o frontend,
### que é a página principal que liga a interface à API externa e ao backend e seu banco de dados 