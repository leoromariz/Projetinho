from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, request
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model.pipeline import *
from model import Session
from model.preprocessador import *
from logger import logger
from schemas.error_schema import ErrorSchema
from schemas.aluno_schema import AlunoSchema, AlunoViewSchema, AlunoBuscaSchema, apresenta_aluno, apresenta_alunos
from model.aluno import Aluno 
from flask_cors import CORS


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
    name="Aluno",
    description="Adição, visualização, remoção e predição de alunos com base em seu uso de redes sociais",
)


# Rota home - redireciona para o frontend
@app.get("/", tags=[home_tag])
def home():
    """Redireciona para o index.html do frontend."""

    return redirect("/front/my_website/index.html") 


# Rota para documentação OpenAPI
@app.get("/docs", tags=[home_tag])
def docs():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect("/openapi")


# Rota de listagem de alunos
@app.get(
    "/alunos",
    tags=[aluno_tag],
    responses={"200": AlunoViewSchema, "404": ErrorSchema},
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
        print(alunos) # Isso pode imprimir objetos SQLAlchemy, não os dados formatados
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

# A função não recebe o 'form' diretamente na assinatura,
# pois os dados virão de request.form
def predict():
    """Adiciona um novo aluno à base de dados
    Retorna uma representação dos alunos e diagnósticos associados.
    """
    # Coleta os dados do formulário
    form_data = request.form.to_dict()
    logger.debug(f"Dados recebidos do formulário: {form_data}")

    # Valida os dados usando o AlunoSchema do Pydantic
    try:
        # Pydantic fará a validação dos tipos e campos obrigatórios
        form = AlunoSchema(**form_data)
    except Exception as e:
        error_msg = f"Dados de entrada inválidos. Detalhes: {e}"
        logger.warning(f"Erro de validação ao adicionar aluno: {error_msg}")
        return {"message": error_msg}, 400

    # Instanciando classes
    preprocessador = PreProcessador()
    pipeline = Pipeline()

    # Preparando os dados para o modelo
    X_input = preprocessador.preparar_form(form)
    logger.debug(f"Shape de X_input antes da predição: {X_input.shape}")
    
    # Carregando modelo
    model_path = "./MachineLearning/pipelines/rf_addicted_pipeline.pkl"
    try:
        modelo = pipeline.carrega_pipeline(model_path)
        logger.debug(f"Pipeline carregado com sucesso de: {model_path}")
        if hasattr(modelo, 'named_steps') and 'MinMaxScaler' in modelo.named_steps:
            scaler_in_pipeline = modelo.named_steps['MinMaxScaler']
            if hasattr(scaler_in_pipeline, 'n_features_in_'):
                logger.debug(f"MinMaxScaler no pipeline carregado espera {scaler_in_pipeline.n_features_in_} features.")
        elif hasattr(modelo, 'n_features_in_'):
            logger.debug(f"Modelo carregado (não pipeline) espera {modelo.n_features_in_} features.")

    except Exception as e:
        error_msg = f"Erro ao carregar o modelo de ML: {e}"
        logger.error(error_msg)
        return {"message": error_msg}, 500 # Erro interno do servidor se o modelo não carregar

    # Realizando a predição
    try:
        outcome = int(modelo.predict(X_input)[0])
        logger.debug(f"Predição realizada: {outcome}")
    except Exception as e:
        error_msg = f"Erro ao realizar a predição com o modelo: {e}"
        logger.error(error_msg)
        return {"message": error_msg}, 500 # Erro interno do servidor se a predição falhar


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

    try:
        # Criando conexão com a base
        session = Session()

        session.add(aluno)
        # Efetivando o comando de adição
        session.commit()
        logger.debug(f"Adicionado aluno de id: '{aluno.id}'")
        return apresenta_aluno(aluno), 200

    # Caso ocorra algum erro na adição (ex: IntegrityError para outras colunas)
    except IntegrityError as e: # Captura erro de integridade do DB
        error_msg = "Erro de integridade ao salvar novo aluno (possível duplicidade em campos únicos, se houver) :/"
        logger.warning(f"{error_msg}. Detalhes: {e}")
        return {"message": error_msg}, 409 # Conflito

    except Exception as e: # Captura outros erros gerais
        error_msg = f"Não foi possível salvar novo aluno :/. Detalhes: {e}"
        logger.warning(f"Erro geral ao adicionar aluno: {error_msg}")
        return {"message": error_msg}, 400


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
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Aluno encontrado: '{aluno.id}'") 
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