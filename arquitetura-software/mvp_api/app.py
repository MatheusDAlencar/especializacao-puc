from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from flask import request
from flask import jsonify
from flask import Flask
from urllib.parse import unquote
from model import Session, Lead
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)
    
    
# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
lead_tag = Tag(name="Lead", description="Adição, visualização e remoção de leads à base")
comentario_tag = Tag(name="Comentario", description="Adição de um comentário a um lead cadastrado na base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/lead', tags=[lead_tag],
          responses={"200": LeadViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_lead(form: LeadSchema):
    """Adiciona um novo Lead à base de dados

    Retorna uma representação dos leads e comentários associados.
    """
    lead = Lead(
        nome=form.nome,
        idade=form.idade,
        genero=form.genero,
        cidade_residencia=form.cidade_residencia,
        grau_formacao=form.grau_formacao,
        curso_formacao=form.curso_formacao
        )
    
    logger.debug(f"Adicionando lead de nome: '{lead.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando lead
        session.add(lead)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado lead de nome: '{lead.nome}'")
        return apresenta_lead(lead), 200

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar lead '{lead.nome}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/leads', tags=[lead_tag],
         responses={"200": ListagemLeadsSchema, "404": ErrorSchema})
def get_leads():
    """Faz a busca por todos os Leads cadastrados

    Retorna uma representação da listagem de leads.
    """
    logger.debug(f"Coletando leads")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    leads = session.query(Lead).all()

    if not leads:
        # se não há leads cadastrados
        return ({"não há leads"}), 204
    else:
        logger.debug(f"%d leads encontrados" % len(leads))
        # retorna a representação de lead
        return (apresenta_leads(leads)), 200
    
    
@app.delete('/lead', tags=[lead_tag],
            responses={"200": LeadDelSchema, "404": ErrorSchema})
def del_lead(query: LeadBuscaSchema):
    lead_nome = query.nome
    """Deleta um Lead a partir do nome de lead informado

    Retorna uma mensagem de confirmação da remoção.
    """
    logger.debug(f"Deletando dados sobre lead #{lead_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Lead).filter(Lead.nome == lead_nome).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado lead #{lead_nome}")
        return ({"mesage": "Lead removido", "id": lead_nome}), 200
    else:
        # se o lead não foi encontrado
        error_msg = "Lead não encontrado na base :/"
        logger.warning(f"Erro ao deletar lead #'{lead_nome}', {error_msg}")
        return ({"mesage": error_msg}), 404
    

@app.put('/lead', tags=[lead_tag],
         responses={"200": LeadViewSchema, "404": ErrorSchema, "400": ErrorSchema})
def update_lead(query: LeadBuscaSchema, form: LeadSchema):
    """Edita um Lead da base de dados"""
    lead_nome = query.nome
    
    try:
        logger.debug(f"Atualizando lead com nome: '{lead_nome}'")
        # criando conexão com a base
        session = Session()
        # buscando o lead
        lead = session.query(Lead).filter(Lead.nome == lead_nome).first()
        
        if not lead:
            # se tentar atualizar lead que não existe no banco
            error_msg = "Lead não encontrado"
            logger.warning(error_msg)
            return jsonify({"message": error_msg}), 404

       # Atualiza campos do lead existente em vez de criar novo
        lead.nome = form.nome
        lead.idade = form.idade
        lead.genero = form.genero
        lead.cidade_residencia = form.cidade_residencia
        lead.grau_formacao = form.grau_formacao
        lead.curso_formacao = form.curso_formacao

        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Atualizado lead de nome: '{lead.nome}'")
        return jsonify(apresenta_lead(lead)), 200

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = f"Não foi possível atualizar o lead: {str(e)}"
        logger.warning(f"Erro ao atualizar lead '{lead_nome}': {error_msg}")
        return jsonify({"message": error_msg}), 400