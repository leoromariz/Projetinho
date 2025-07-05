import backend.model.aluno

from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import *
from model.preprocessador import PreProcessador
from model.pipeline import Pipeline
from logger import logger
from schemas.aluno_schema import AlunoBuscaSchema, AlunoSchema, AlunoViewSchema, apresenta_aluno, apresenta_alunos
from schemas.error_schema import ErrorSchema
from flask_cors import CORS
from model.base import Session


aluno = backend.model.aluno.Aluno()

# Instanciando o objeto OpenAPI
info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(
    __name__, info=info, static_folder="../front", static_url_path="/front"
)
CORS(app)

# Definindo tags para agrupamento das rotas
home_tag = Tag(
    name="Documentação",
    description="Seleção de documentação: Swagger, Redoc ou RapiDoc",
)
aluno_tag = Tag(
    id="Aluno",
    description="Adição, visualização, remoção e predição de alunos com base em seu uso de redes sociais",
)


# Rota home - redireciona para o frontend
@app.get("/", tags=[home_tag])
def home():
    """Redireciona para o index.html do frontend."""
    return redirect("/front/index.html")


# Rota para documentação OpenAPI
@app.get("/docs", tags=[home_tag])
def docs():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect("/openapi")


# Rota de listagem de alunos
@app.get(
    "/alunos",
    tags=[aluno_tag],
    responses={"200": AlunoViewSchema, "404": ErrorSchema}, #TODO: Corrigir o nome do schema de resposta
)
def get_alunos():
    """Lista todos os alunos cadastrados na base
    Args:
       none

    Returns:
        list: lista de alunos cadastrados na base
    """
    logger.debug("Coletando dados sobre todos os alunos")
    # Criando conexão com a base
    session = Session()
    # Buscando todos os alunos
    alunos = session.query(Aluno).all()

    if not alunos:
        # Se não houver alunos
        return {"alunos": []}, 200
    else:
        logger.debug(f"%d alunos encontrados" % len(alunos))
        print(alunos)
        return apresenta_alunos(alunos), 200


# Rota de adição de aluno
@app.post(
    "/aluno",
    tags=[aluno_tag],
    responses={
        "200": AlunoViewSchema,
        "400": ErrorSchema,
        "409": ErrorSchema,
    },
)
def predict(form: AlunoSchema):
    """Adiciona um novo aluno à base de dados
    Retorna uma representação dos alunos e diagnósticos associados.

    """
    # Instanciando classes
    preprocessador = PreProcessador()
    pipeline = Pipeline()

    # Recuperando os dados do formulário
    age = form.age
    gender = form.gender
    academic_level = form.academic_level
    country = form.country
    avg_daily_usage_hours = form.avg_daily_usage_hours
    most_used_platform = form.most_used_platform
    affects_academic_performance = form.affects_academic_performance
    sleep_hours_per_night = form.sleep_hours_per_night
    mental_health_score = form.mental_health_score
    relationship_status = form.relationship_status
    conflicts_over_social_media = form.conflicts_over_social_media

    # Preparando os dados para o modelo
    X_input = preprocessador.preparar_form(form)
    # Carregando modelo
    model_path = "./MachineLearning/pipelines/rf_addicted_pipeline.pkl"
    modelo = pipeline.carrega_pipeline(model_path)
    # Realizando a predição
    outcome = int(modelo.predict(X_input)[0])

    aluno = Aluno(
        age = form.age,
        gender = form.gender,
        academic_level = form.academic_level,
        country = form.country,
        avg_daily_usage_hours = form.avg_daily_usage_hours,
        most_used_platform = form.most_used_platform,
        affects_academic_performance = form.affects_academic_performance,
        sleep_hours_per_night = form.sleep_hours_per_night,
        mental_health_score = form.mental_health_score,
        relationship_status = form.relationship_status,
        conflicts_over_social_media = form.conflicts_over_social_media,
        outcome = outcome
        )
    logger.debug(f"Adicionando aluno de id: '{aluno.id}'")

    try:
        # Criando conexão com a base
        session = Session()

        # Checando se aluno já existe na base
        if session.query(Aluno).filter(Aluno.id == aluno.id).first():
            error_msg = "Aluno já existente na base :/"
            logger.warning(
                f"Erro ao adicionar aluno '{aluno.id}', {error_msg}"
            )
            return {"message": error_msg}, 409

        # Adicionando aluno
        session.add(aluno)
        # Efetivando o comando de adição
        session.commit()
        # Concluindo a transação
        logger.debug(f"Adicionado aluno de id: '{aluno.id}'")
        return apresenta_aluno(aluno), 200

    # Caso ocorra algum erro na adição
    except Exception as e:
        error_msg = "Não foi possível salvar novo aluno :/"
        logger.warning(
            f"Erro ao adicionar aluno '{aluno.id}', {error_msg}"
        )
        return {"message": error_msg}, 400


# Métodos baseados em id
# Rota de busca de aluno por id
@app.get(
    "/aluno",
    tags=[aluno_tag],
    responses={"200": AlunoViewSchema, "404": ErrorSchema},
)
def get_aluno(query: AlunoBuscaSchema):
    """Faz a busca por um aluno cadastrado na base a partir do ID

    Args:
        id (int): ID do aluno

    Returns:
        dict: representação do aluno e diagnóstico associado
    """

    aluno_id = query.id
    logger.debug(f"Coletando dados sobre aluno #{aluno_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    aluno = (
        session.query(Aluno).filter(Aluno.id == aluno_id).first()
    )

    if not aluno:
        # se o aluno não foi encontrado
        error_msg = f"Aluno {aluno_id} não encontrado na base :/"
        logger.warning(
            f"Erro ao buscar aluno '{aluno_id}', {error_msg}"
        )
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Aluno encontrado: '{aluno.name}'")
        # retorna a representação do aluno
        return apresenta_aluno(aluno), 200


# Rota de remoção de aluno por id
@app.delete(
    "/aluno",
    tags=[aluno_tag],
    responses={"200": AlunoViewSchema, "404": ErrorSchema},
)
def delete_aluno(query: AlunoBuscaSchema):
    """Remove um aluno cadastrado na base a partir do id

    Args:
        id (int): ID do aluno

    Returns:
        msg: Mensagem de sucesso ou erro
    """

    aluno_id = query.id
    logger.debug(f"Deletando dados sobre aluno #{aluno_id}")

    # Criando conexão com a base
    session = Session()

    # Buscando aluno
    aluno = (
        session.query(Aluno).filter(Aluno.id == aluno_id).first()
    )

    if not aluno:
        error_msg = "Aluno não encontrado na base :/"
        logger.warning(
            f"Erro ao deletar aluno '{aluno_id}', {error_msg}"
        )
        return {"message": error_msg}, 404
    else:
        session.delete(aluno)
        session.commit()
        logger.debug(f"Deletado aluno #{aluno.id}")
        return {
            "message": f"Aluno {aluno.id} removido com sucesso!"
        }, 200


if __name__ == "__main__":
    app.run(debug=True)
