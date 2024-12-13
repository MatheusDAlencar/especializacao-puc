from pydantic import BaseModel
from typing import Optional, List
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


class ListagemLeadsSchema(BaseModel):
    """ Define como uma listagem de leads será retornada.
    """
    leads:List[LeadSchema]


def apresenta_leads(leads:List[Lead]):
    """ Retorna uma representação do lead seguindo o schema definido em
        LeadViewSchema.
    """
    result = []
    for lead in leads:
        result.append({
            "nome": lead.nome,
            "idade": lead.idade,
            "genero": lead.genero,
            "cidade_residencia": lead.cidade_residencia,
            "grau_formacao": lead.grau_formacao,
            "curso_formacao": lead.curso_formacao
        })
    return {"leads": result}


class LeadViewSchema(BaseModel):
    """ Define como um lead será retornado
    """
    id: int = 1
    nome: str = "Ana Maria"
    idade: Optional[int] = 21
    genero: str = "feminino"
    cidade_residencia: str = "Franca/SP"
    grau_formacao: str = "cursando ensino superior"
    curso_formacao: str = "Direito"


class LeadDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    message: str
    nome: str

def apresenta_lead(lead:Lead):
    """ Retorna uma representação do lead seguindo o schema definido em
        LeadViewSchema.
    """
    return {
        "id": lead.id,
        "nome": lead.nome,
        "idade": lead.idade,
        "genero": lead.genero,
        "cidade_residencia": lead.cidade_residencia,
        "grau_formacao": lead.grau_formacao,
        "curso_formacao": lead.curso_formacao,
    }
