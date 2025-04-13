from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from typing import Union

from  model import Base


class Lead(Base):
    __tablename__ = 'lead'

    id = Column("pk_lead", Integer, primary_key=True)
    nome = Column(String(140))
    idade = Column(Integer)
    genero = Column(String(140))
    cidade_residencia = Column(String(140))
    grau_formacao = Column(String(140))
    curso_formacao = Column(String(140))
    data_insercao = Column(DateTime, default=datetime.now())


    def __init__(self, nome:str, idade:int, genero:str,
                 cidade_residencia:str, grau_formacao:str,
                 curso_formacao:str,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria um Lead

        Arguments:
            nome: nome do lead
            idade: idade do lead
            genero: gênero do lead (masculino, feminino, intersexo etc.) 
            cidade_residencia: onde o lead reside atualmente
            grau_formacao: grau de estudo do lead (graduando, doutor etc.)
            curso_formacao: o curso ao qual se relaciona o grau_formacao
            data_insercao: data de quando o lead foi inserido à base
        """
        self.nome = nome
        self.idade = idade
        self.genero = genero
        self.cidade_residencia = cidade_residencia
        self.grau_formacao = grau_formacao
        self.curso_formacao = curso_formacao

        # se data da inserção não for informada (uso esperado),
        # será a data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao