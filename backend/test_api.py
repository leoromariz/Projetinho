import pytest
import json
from app import app
from model import Session, Aluno

# To run: pytest -v test_api.py

@pytest.fixture
def client():
    """Configura o cliente de teste para a aplicação Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def sample_student_data():
    """Dados de exemplo para teste de aluno"""
    return {
        "age": "22",
        "gender": "Masculino",
        "academic_level": "Superior",
        "country": "Brasil",
        "avg_daily_usage_hours": 5,
        "most_used_platform": "Instagram",
        "affects_academic_performance": "Sim",
        "sleep_hours_per_night": 7,
        "mental_health_score": 8,
        "relationship_status": "Solteiro",
        "conflicts_over_social_media": "Não"
    }


def test_home_redirect(client):
    """Testa se a rota home redireciona para o frontend"""
    response = client.get('/')
    assert response.status_code == 302
    assert '/front/index.html' in response.location

def test_docs_redirect(client):
    """Testa se a rota docs redireciona para openapi"""
    response = client.get('/docs')
    assert response.status_code == 302
    assert '/openapi' in response.location

def test_get_alunos_empty(client):
    """Testa a listagem de alunos quando não há nenhum"""
    response = client.get('/alunos')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'alunos' in data
    assert isinstance(data['alunos'], list)

def test_add_student_prediction(client, sample_student_data):
    """Testa a adição de um aluno com predição"""
    # Primeiro, vamos limpar qualquer aluno existente com o mesmo ID
    session = Session()
    existing_student = session.query(Aluno).filter(Aluno.id == sample_student_data['id']).first()
    if existing_student:
        session.delete(existing_student)
        session.commit()
    session.close()
    
    # Agora testamos a adição
    response = client.post('/aluno', 
                          data=json.dumps(sample_student_data),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    # Verifica se o aluno foi criado com todas as informações
    assert data['id'] == sample_student_data['id']
    assert data['age'] == sample_student_data['age']
    assert data['gender'] == sample_student_data['gender']
    assert data['academic_level'] == sample_student_data['academic_level']
    assert data['country'] == sample_student_data['country']
    assert data['avg_daily_usage_hours'] == sample_student_data['avg_daily_usage_hours']
    assert data['most_used_platform'] == sample_student_data['most_used_platform']
    assert data['affects_academic_performance'] == sample_student_data['affects_academic_performance']
    assert data['sleep_hours_per_night'] == sample_student_data['sleep_hours_per_night']
    assert data['mental_health_score'] == sample_student_data['mental_health_score']
    assert data['relationship_status'] == sample_student_data['relationship_status']
    assert data['conflicts_over_social_media'] == sample_student_data['conflicts_over_social_media']
    
    
    # Verifica se a predição foi feita (outcome deve estar presente)
    assert 'outcome' in data
    assert data['outcome'] in [0, 1]  # Deve ser 0 (não diabético) ou 1 (diabético)

def test_add_duplicate_student(client, sample_student_data):
    """Testa a adição de um aluno duplicado"""
    # Primeiro adiciona o aluno
    client.post('/aluno', 
                data=json.dumps(sample_student_data),
                content_type='application/json')
    
    # Tenta adicionar novamente
    response = client.post('/aluno', 
                          data=json.dumps(sample_student_data),
                          content_type='application/json')
    
    assert response.status_code == 409
    data = json.loads(response.data)
    assert 'message' in data
    assert 'já existente' in data['message']

def test_get_student_by_id(client, sample_student_data):
    """Testa a busca de um aluno por ID"""
    # Primeiro adiciona o aluno
    client.post('/aluno', 
                data=json.dumps(sample_student_data),
                content_type='application/json')

    # Busca o aluno por ID
    response = client.get(f'/aluno?id={sample_student_data["id"]}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id'] == sample_student_data['id']

def test_get_nonexistent_student(client):
    """Testa a busca de um aluno que não existe"""
    response = client.get('/aluno?id=AlunoInexistente')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'message' in data  # Corrigido o typo de "mesage" para "message"

def test_delete_student(client, sample_student_data):
    """Testa a remoção de um aluno"""
    # Primeiro adiciona o aluno
    client.post('/aluno', 
                data=json.dumps(sample_student_data),
                content_type='application/json')

    # Remove o aluno
    response = client.delete(f'/aluno?id={sample_student_data["id"]}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert 'removido com sucesso' in data['message']

def test_delete_nonexistent_student(client):
    """Testa a remoção de um aluno que não existe"""
    response = client.delete('/aluno?id=AlunoInexistente')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'message' in data

def test_prediction_edge_cases(client):
    """Testa casos extremos para predição"""
    # Teste com valores mínimos
    min_data = {
        "age": 0,
        "gender": "Male",
        "academic_level": "High School",
        "avg_daily_usage_hours": 0.0,
        "most_used_platform": "Instagram",
        "affects_academic_performance": "Yes",
        "sleep_hours_per_night": 0.0,
        "mental_health_score": 0,
        "relationship_status": "Solteiro(a)",
        "conflicts_over_social_media": 0
    }

   
    assert data['sleep_hours_per_night'] == sample_student_data['sleep_hours_per_night']
    assert data['mental_health_score'] == sample_student_data['mental_health_score']
    assert data['relationship_status'] == sample_student_data['relationship_status']
    assert data['conflicts_over_social_media'] == sample_student_data['conflicts_over_social_media']
    
    response = client.post('/aluno', 
                          data=json.dumps(min_data),
                          content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'outcome' in data
    
    # Teste com valores máximos típicos
    max_data = {
        "age": 100,
        "gender": "Male",
        "academic_level": "High School",
        "avg_daily_usage_hours": 24.0,
        "most_used_platform": "Instagram",
        "affects_academic_performance": "Yes",
        "sleep_hours_per_night": 24.0,
        "mental_health_score": 10,
        "relationship_status": "Solteiro(a)",
        "conflicts_over_social_media": 100
    }

    response = client.post('/aluno', 
                          data=json.dumps(max_data),
                          content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'outcome' in data

def cleanup_test_students():
    """Limpa alunos de teste do banco"""
    session = Session()
    test_students = session.query(Aluno).filter(
        Aluno.id.in_(['id', 'Aluno Minimo', 'Aluno Maximo'])
    ).all()

    for student in test_students:
        session.delete(student)
    session.commit()
    session.close()

# Executa limpeza após os testes
def test_cleanup():
    """Limpa dados de teste"""
    cleanup_test_students()
