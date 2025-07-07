import pytest
import json
from app import app
from model import Session
from model.aluno import Aluno

# To run: pytest -v test_api.py

@pytest.fixture
def client():
    """Configura o cliente de teste para a aplicação Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def sample_student_data_payload():
    """Dados de exemplo para teste de aluno (sem ID, pois é autoincrementado)"""
    return {
        # Removido 'id' pois é autoincrementado pelo DB
        "age": 22,
        "gender": 1,
        "academic_level": 1,
        "country": 7,
        "avg_daily_usage_hours": 5.0, # Float
        "most_used_platform": 1,
        "affects_academic_performance": 1,
        "sleep_hours_per_night": 7.0, # Float
        "mental_health_score": 8,
        "relationship_status": 0,
        "conflicts_over_social_media": 0
    }

@pytest.fixture
def added_student_id(client, sample_student_data_payload):
    """Adiciona um aluno e retorna o ID gerado para uso em outros testes."""
    # Envia como form-urlencoded
    response = client.post('/aluno',
                            data=sample_student_data_payload,
                            content_type='application/x-www-form-urlencoded')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'id' in data
    
    yield data['id'] # Retorna o ID do aluno recém-criado

    # Teardown: Limpa o aluno após o teste
    session = Session()
    student_to_delete = session.query(Aluno).filter(Aluno.id == data['id']).first()
    if student_to_delete:
        session.delete(student_to_delete)
        session.commit()
    session.close()


def test_home_redirect(client):
    """Testa se a rota home redireciona para o frontend"""
    response = client.get('/')
    assert response.status_code == 302
    # Atualizado para o caminho real de redirecionamento
    assert '/front/my_website/index.html' in response.location 

def test_docs_redirect(client):
    """Testa se a rota docs redireciona para openapi"""
    response = client.get('/docs')
    assert response.status_code == 302
    assert '/openapi' in response.location

def test_get_alunos_empty(client):
    """Testa a listagem de alunos quando não há nenhum"""
    # Limpa todos os alunos antes de testar a lista vazia
    session = Session()
    session.query(Aluno).delete()
    session.commit()
    session.close()

    response = client.get('/alunos')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'alunos' in data
    assert isinstance(data['alunos'], list)
    assert len(data['alunos']) == 0 # Garante que a lista esteja vazia

def test_add_student_prediction(client, sample_student_data_payload):
    """Testa a adição de um aluno com predição"""
    # Não precisamos limpar antes, pois added_student_id já lida com isso ou o DB é limpo por outro fixture
    # Apenas testamos a adição em si.
    response = client.post('/aluno',
                            data=sample_student_data_payload, # Envia como form-urlencoded
                            content_type='application/x-www-form-urlencoded')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    # Verifica se o aluno foi criado com todas as informações e ID gerado
    assert 'id' in data # O ID deve ser gerado e retornado
    assert isinstance(data['id'], int) # Deve ser um inteiro
    assert data['age'] == sample_student_data_payload['age']
    assert data['gender'] == sample_student_data_payload['gender']
    assert data['academic_level'] == sample_student_data_payload['academic_level']
    assert data['country'] == sample_student_data_payload['country']
    assert data['avg_daily_usage_hours'] == sample_student_data_payload['avg_daily_usage_hours']
    assert data['most_used_platform'] == sample_student_data_payload['most_used_platform']
    assert data['affects_academic_performance'] == sample_student_data_payload['affects_academic_performance']
    assert data['sleep_hours_per_night'] == sample_student_data_payload['sleep_hours_per_night']
    assert data['mental_health_score'] == sample_student_data_payload['mental_health_score']
    assert data['relationship_status'] == sample_student_data_payload['relationship_status']
    assert data['conflicts_over_social_media'] == sample_student_data_payload['conflicts_over_social_media']
    
    # Verifica se a predição foi feita (outcome deve estar presente)
    assert 'outcome' in data
    assert data['outcome'] in [0, 1] 

def test_add_duplicate_student(client, sample_student_data_payload):
    """Testa a adição de um aluno duplicado (por campos únicos, se houver)"""
    # Este teste é complicado com ID autoincrementado, pois cada POST cria um novo ID.
    # Para testar duplicidade, você precisaria de uma UniqueConstraint em outros campos (e.g., age+gender+country)
    # ou testar um cenário onde o ID é fornecido e duplicado.
    # Como o ID é autoincrementado, este teste como está não fará sentido para "duplicidade de ID".
    # Ele sempre adicionará um novo aluno com um novo ID.
    # Se você tem uma UniqueConstraint em outros campos, o teste deve ser ajustado para isso.
    # Por enquanto, vou ajustar para que ele adicione e espere 200, pois não há duplicidade de ID.
    # Se sua API retornar 409 para outros campos, ajuste a asserção.

    # Primeiro adiciona o aluno (será um novo ID)
    response_first = client.post('/aluno', 
                                 data=sample_student_data_payload,
                                 content_type='application/x-www-form-urlencoded')
    assert response_first.status_code == 200
    first_student_id = json.loads(response_first.data)['id']

    # Tenta adicionar novamente (será outro novo ID, a menos que haja UniqueConstraint em outros campos)
    response_second = client.post('/aluno', 
                                  data=sample_student_data_payload,
                                  content_type='application/x-www-form-urlencoded')
    
    # Se não há UniqueConstraint em outros campos, o status esperado é 200
    # Se houver UniqueConstraint em outros campos e a API retornar 409, mude para assert 409 == 409
    assert response_second.status_code == 200 
    second_student_id = json.loads(response_second.data)['id']
    assert first_student_id != second_student_id # Garante que são IDs diferentes

    # Limpeza dos alunos criados neste teste
    session = Session()
    session.delete(session.query(Aluno).filter(Aluno.id == first_student_id).first())
    session.delete(session.query(Aluno).filter(Aluno.id == second_student_id).first())
    session.commit()
    session.close()


def test_get_student_by_id(client, added_student_id):
    """Testa a busca de um aluno por ID gerado"""
    # Busca o aluno por ID gerado pelo fixture
    response = client.get(f'/aluno?id={added_student_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id'] == added_student_id

def test_get_nonexistent_student(client):
    """Testa a busca de um aluno que não existe (com ID inteiro válido)"""
    # Passa um ID inteiro que é muito improvável de existir
    non_existent_id = 999999999999999999 
    response = client.get(f'/aluno?id={non_existent_id}')
    assert response.status_code == 404 # Espera 404 para ID não encontrado
    data = json.loads(response.data)
    assert 'message' in data

def test_delete_student(client, added_student_id):
    """Testa a remoção de um aluno"""
    # Remove o aluno usando o ID gerado pelo fixture
    response = client.delete(f'/aluno?id={added_student_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert 'removido com sucesso' in data['message']

    # Verifica se o aluno realmente foi removido
    session = Session()
    deleted_student = session.query(Aluno).filter(Aluno.id == added_student_id).first()
    session.close()
    assert deleted_student is None


def test_delete_nonexistent_student(client):
    """Testa a remoção de um aluno que não existe (com ID inteiro válido)"""
    # Passa um ID inteiro que é muito improvável de existir
    non_existent_id = 999999999999999999 
    response = client.delete(f'/aluno?id={non_existent_id}')
    assert response.status_code == 404 # Espera 404 para ID não encontrado
    data = json.loads(response.data)
    assert 'message' in data

def test_prediction_edge_cases(client):
    """Testa casos extremos para predição"""
    # Teste com valores mínimos
    min_data = {
        # Removido 'id'
        "age": 0,
        "gender": 0,
        "country": 0,
        "academic_level": 0,
        "avg_daily_usage_hours": 0.0,
        "most_used_platform": 0,
        "affects_academic_performance": 0,
        "sleep_hours_per_night": 0.0,
        "mental_health_score": 0,
        "relationship_status": 0,
        "conflicts_over_social_media": 0
    }

    # REMOVIDAS AS LINHAS DE ASSERTION FORA DE LUGAR
    
    response = client.post('/aluno',
                            data=min_data, # Envia como form-urlencoded
                            content_type='application/x-www-form-urlencoded')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'outcome' in data
    min_student_id = data['id'] # Captura o ID para limpeza

    # Teste com valores máximos típicos
    max_data = {
        # Removido 'id'
        "age": 100,
        "gender": 2,
        "country": 110,
        "academic_level": 3,
        "avg_daily_usage_hours": 24.0,
        "most_used_platform": 12,
        "affects_academic_performance": 1,
        "sleep_hours_per_night": 24.0,
        "mental_health_score": 10,
        "relationship_status": 3,
        "conflicts_over_social_media": 100
    }

    response = client.post('/aluno',
                            data=max_data, # Envia como form-urlencoded
                            content_type='application/x-www-form-urlencoded')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'outcome' in data
    max_student_id = data['id'] # Captura o ID para limpeza

    # Limpeza dos alunos criados neste teste
    session = Session()
    session.delete(session.query(Aluno).filter(Aluno.id == min_student_id).first())
    session.delete(session.query(Aluno).filter(Aluno.id == max_student_id).first())
    session.commit()
    session.close()


# A função cleanup_test_students não é mais chamada diretamente como um teste
# e não é mais necessária como um teste separado, pois os fixtures de teste
# já cuidam da limpeza.
# Se você ainda quiser uma função de limpeza manual, ela pode ser chamada
# em um conftest.py ou diretamente no setup/teardown de um teste específico.

# Removido o test_cleanup, pois a limpeza é feita pelos fixtures ou manualmente.
# def test_cleanup():
#     """Limpa dados de teste"""
#     cleanup_test_students()

