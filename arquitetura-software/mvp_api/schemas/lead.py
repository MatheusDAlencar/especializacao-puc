from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from flask import jsonify
from model.lead import Lead


class LeadSchema(BaseModel):
    """ Define como um novo lead a ser inserido deve ser representado
    """    
    nome: str = "Ana Maria"
    idade: Optional[int] = 21
    genero: str = "feminino"
    cidade_residencia: str = "Franca/SP"
    grau_formacao: str = "cursando ensino superior"
    curso_formacao: str = "Direito"


class LeadViewSchema(BaseModel):
    """ Define como um lead será retornado
    """
    id: int = 1
    

class ListagemLeadsSchema(BaseModel):
    """ Define como uma listagem de leads será retornada.
    """
    leads:List[LeadViewSchema]


class LeadDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    message: str
    nome: str

class LeadBuscaSchema(BaseModel):
    "Define como um lead existente será encontrado para permitir alterar e deletar"
    nome: str = Field(description="Nome do lead")


def apresenta_leads(leads: List[Lead]) -> Dict[str, List[Dict[str, Any]]]:
    """Retorna uma representação dos leads seguindo o schema definido"""
    return {
        "leads": [apresenta_lead(lead) for lead in leads]
    }

def apresenta_lead(lead: Lead) -> Dict[str, Any]:
    """Retorna uma representação do lead seguindo o schema definido"""
    return {
        "id": lead.id,
        "nome": lead.nome,
        "idade": lead.idade,
        "genero": lead.genero,
        "cidade_residencia": lead.cidade_residencia,
        "grau_formacao": lead.grau_formacao,
        "curso_formacao": lead.curso_formacao
    }