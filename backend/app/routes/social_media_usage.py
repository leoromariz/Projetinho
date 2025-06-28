# backend/app/routes/social_media_usage.py

from flask import Blueprint, request, jsonify
from pydantic import BaseModel, Field, ValidationError

social_media_bp = Blueprint('social_media', __name__)

class SocialMediaData(BaseModel):
    age: int = Field(..., gt=0, description="Idade do usuário")
    gender: str = Field(..., description="Gênero do usuário")
    academicLevel: str = Field(..., description="Nível acadêmico do usuário")
    country: str = Field(..., description="País do usuário")
    avgDailyUsageHours: int = Field(..., ge=0, description="Média de horas de uso diário de redes sociais")
    mostUsedPlatform: str = Field(..., description="Plataforma mais utilizada")
    affectsAcademicPerformance: str = Field(..., description="Se afeta ou não o desempenho acadêmico ('Sim' ou 'Não')")
    sleepHoursPerNight: int = Field(..., ge=0, description="Horas de sono por noite")
    mentalHealthScore: int = Field(..., ge=1, le=10, description="Pontuação de saúde mental (1-10)")
    relationshipStatus: str = Field(..., description="Status de relacionamento")
    socialMediaConflicts: int = Field(..., ge=0, description="Número de conflitos relacionados a redes sociais")

@social_media_bp.route("/social-media-data", methods=["POST"])
def receive_social_media_data():
    """
    Recebe e processa os dados de uso de redes sociais enviados pelo frontend.
    """
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    try:
        data = SocialMediaData(**request.get_json())
        # Aqui você pode adicionar a lógica para processar os dados,
        # como salvá-los em um banco de dados, fazer análises, etc.
        # Por enquanto, vamos apenas retornar os dados recebidos.
        print(f"Dados recebidos: {data.model_dump_json(indent=2)}")
        return jsonify({"message": "Dados recebidos com sucesso!", "received_data": data.model_dump()}), 200
    except ValidationError as e:
        # Erro de validação do Pydantic
        return jsonify({"error": "Validation Error", "details": e.errors()}), 422
    except Exception as e:
        # Outros erros inesperados
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500