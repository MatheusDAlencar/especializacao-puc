# Minha API

Este pequeno projeto é o trabalho final da Disciplina **Desenvolvimento Full Stack Avançado** 

O objetivo aqui é demonstrar o aprendizado obtido a partir das aulas.

O projeto se baseia em um projeto real que precisarei tocar durante o ano de 2025. Utilizei o trabalho final como ponto de partida
para o que desejo fazer com maior complexidade no futuro. Durante a evolução, pretendo trocar a SPA por uma aplicação de várias
páginas, com login, rotas entre as diferentes páginas etc. Por ora, a SPA foi suficiente para atingir o objetivo.

Entre o MVP Full Stack Básico e o MVP Full Stack Avançado, foram realizadas duas (2) mudanças:
1) Inserção da função PUT no meu backend, para finalmente ter GET, POST, DELETE e PUT;
2) Containerização da API utilizando o Dockerfile.

Sobre a arquitetura de software, como se percebe, o frontend é a página principal, que conecta API externa e API autoral.
Já a API autoral é o que se liga ao banco de dados, garantindo a persistência dos dados. Visualmente, ficou assim:

![Arquitetura](img\Arquitetura.jpg)

Importante ressalvar que a função PUT tem relação de dependência com o frontend. A SPA não consegue modificar os dados do Lead
sem a validação de verdade no banco de dados, o que só ocorre quando a função PUT está ativa e funcional.

A API externa atualmente preenche o front end. A interação com ela, além do preenchimento, é de edição de todos os cards de venda
e adequação ao navegador do usuário. A API é 100% gratuita e não precisa de licença de uso ou cadastro. As rotas estão declaradas
no arquivo JavaScript, a previsão de aparição no frontend está no HTML e a interação com os dados e cards está no CSS. 
No futuro, a intenção é que essa disposição dos itens à venda se torne uma única fila, em carrossel, além de permitir o registro
das compras via site, que gerarão descontos para os clientes, incentivando o acesso ao site e o ganho em marketing orgânico.

Para o futuro, pretendo modificar muito mais coisas, acompanhando o aprendizado. Algumas mudanças já idealizadas:
1) a API externa que atualmente é a Fake Store será substituída pelos links reais de itens à venda,
    em especial os cursos disponibilizados (Hotmart) e os livros dos professores, dispostos em livrarias distintas,
    o que vai exigir algum trabalho a mais de curadoria do que será puxado;
2) inserir outra API externa, agora do YouTube, para que os vídeos do canal fiquem disponíveis na página principal;
3) o formulário de preenchimento dos dados se tornará um cadastro de página própria acessado por link na página inicial.
4) o cadastro exigirá login e senha, estipulando um nível de acesso para usuários distintos, no caso Lead e Administrador.
5) o Lead somente poderá ver seus dados e usar as funções hoje já disponíveis na tabela (inserir, deletar e corrigir).
6) já os Administradores terão opções de buscar um usuário qualquer por campo, baixar carga de dados e usar as mesmas funções acima.
7) outras mudanças no frontend. 


---
### Instalação


Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

---
### Executando o servidor


Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

---
### Acesso no browser

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.

---
## Como executar através do Docker

Certifique-se de ter o [Docker](https://docs.docker.com/engine/install/) instalado e em execução em sua máquina.

Navegue até o diretório que contém o Dockerfile e o requirements.txt no terminal.
Execute **como administrador** o seguinte comando para construir a imagem Docker:

```
$ docker build -t mvp_api .
```

Uma vez criada a imagem, para executar o container basta executar, **como administrador**, seguinte o comando:

```
$ docker run -p 5000:5000 mvp_api
```

Uma vez executando, para acessar a API, basta abrir o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador.


### ATENÇÃO: para melhor funcionamento do projeto como um todo através do Docker, é aconselhável primeiro criar o frontend,
### que é a página principal que liga a interface à API externa e ao backend e seu banco de dados


### Alguns comandos úteis do Docker

>**Para verificar se a imagem foi criada** você pode executar o seguinte comando:
>
>```
>$ docker images
>```
>
> Caso queira **remover uma imagem**, basta executar o comando:
>```
>$ docker rmi <IMAGE ID>
>```
>Substituindo o `IMAGE ID` pelo código da imagem
>
>**Para verificar se o container está em exceução** você pode executar o seguinte comando:
>
>```
>$ docker container ls --all
>```
>
> Caso queira **parar um container**, basta executar o comando:
>```
>$ docker stop <CONTAINER ID>
>```
>Substituindo o `CONTAINER ID` pelo ID do container
>
>
> Caso queira **destruir um container**, basta executar o comando:
>```
>$ docker rm <CONTAINER ID>
>```
>Para mais comandos, veja a [documentação do docker](https://docs.docker.com/engine/reference/run/).
