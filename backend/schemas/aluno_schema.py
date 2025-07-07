from pydantic import BaseModel
from pydantic import Field
from typing import Optional, List
from model.aluno import Aluno
import json
import numpy as np

class AlunoSchema(BaseModel):
    """ Define como um novo aluno a ser inserido deve ser representado
    """
    age: int = Field(..., example=20, description="Idade do aluno")
    gender: int = Field(..., example=1, description="Gênero do aluno")
    academic_level: int = Field(..., example=2, description="Nível acadêmico do aluno")
    country: int = Field(..., example=7, description="País de origem do aluno")
    avg_daily_usage_hours: float = Field(..., example=3.5, description="Média de horas de uso diário de redes sociais")
    most_used_platform: int = Field(..., example=4, description="Plataforma de mídia social mais utilizada")
    affects_academic_performance: int = Field(..., example=1, description="Indica se o uso de redes sociais afeta o desempenho acadêmico")
    sleep_hours_per_night: float = Field(..., example=7.5, description="Média de horas de sono por noite")
    mental_health_score: int = Field(..., example=7, description="Pontuação de saúde mental (ex: 0-10)")
    relationship_status: int = Field(..., example=3, description="Status de relacionamento")
    conflicts_over_social_media: int = Field(..., example=1, description="Número de conflitos causados por mídias sociais")


class AlunoViewSchema(BaseModel):
    """Define como um aluno será retornado
    """
    id: int = Field(..., example=1, description="ID único do aluno") 
    age: int = Field(..., example=20, description="Idade do aluno")
    gender: int = Field(..., example=1, description="Gênero do aluno")
    academic_level: int = Field(..., example=2, description="Nível acadêmico do aluno")
    country: int = Field(..., example=7, description="País de origem do aluno")
    avg_daily_usage_hours: float = Field(..., example=3.5, description="Média de horas de uso diário de redes sociais")
    most_used_platform: int = Field(..., example=4, description="Plataforma de mídia social mais utilizada")
    affects_academic_performance: int = Field(..., example=0, description="Indica se o uso de redes sociais afeta o desempenho acadêmico")
    sleep_hours_per_night: float = Field(..., example=7.0, description="Média de horas de sono por noite")
    mental_health_score: int = Field(..., example=7, description="Pontuação de saúde mental (ex: 0-10)")
    relationship_status: int = Field(..., example=3, description="Status de relacionamento")
    conflicts_over_social_media: int = Field(..., example=0, description="Número de conflitos causados por mídias sociais")
    outcome: int = Field(..., example=1, description="Resultado do aluno (ex: 0-1)")

class AlunoBuscaSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca.
    Ela será feita com base no ID do aluno.
    """
    id: int = 1

class ListaAlunosSchema(BaseModel):
    """Define como uma lista de alunos será representada
    """
    alunos: List[AlunoViewSchema] 


class AlunoDelSchema(BaseModel):
    """Define como um aluno para deleção será representado
    """
    id: int = 1

# Apresenta apenas os dados de um aluno
def apresenta_aluno(aluno: Aluno):
    """ Retorna uma representação do aluno seguindo o schema definido em
        AlunoViewSchema.
    """
    return {
        "id": aluno.id,
        "age": aluno.age,
        "gender": aluno.gender,
        "academic_level": aluno.academic_level,
        "country": aluno.country,
        "avg_daily_usage_hours": aluno.avg_daily_usage_hours,
        "most_used_platform": aluno.most_used_platform,
        "affects_academic_performance": aluno.affects_academic_performance,
        "sleep_hours_per_night": aluno.sleep_hours_per_night,
        "mental_health_score": aluno.mental_health_score,
        "relationship_status": aluno.relationship_status,
        "conflicts_over_social_media": aluno.conflicts_over_social_media,
        "outcome": aluno.outcome
    }

# Apresenta uma lista de alunos
def apresenta_alunos(alunos: List[Aluno]):
    """ Retorna uma representação da lista de alunos seguindo o schema definido em
        AlunoViewSchema.
    """
    result = []
    for aluno in alunos:
        result.append({
            "id": aluno.id, # Adicionado o ID aqui
            "age": aluno.age,
            "gender": aluno.gender,
            "academic_level": aluno.academic_level,
            "country": aluno.country,
            "avg_daily_usage_hours": aluno.avg_daily_usage_hours,
            "most_used_platform": aluno.most_used_platform,
            "affects_academic_performance": aluno.affects_academic_performance,
            "sleep_hours_per_night": aluno.sleep_hours_per_night,
            "mental_health_score": aluno.mental_health_score,
            "relationship_status": aluno.relationship_status,
            "conflicts_over_social_media": aluno.conflicts_over_social_media,
            "outcome": aluno.outcome
        })

    return {"alunos": result}
