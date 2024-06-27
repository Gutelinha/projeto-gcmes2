import pytest
from flask import url_for

from main import app


@pytest.fixture
def client():
    print("Running fixture: client")
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_redirect(client):
    response = client.get('/')
    assert response.status_code == 302
    assert response.headers['Location'] == url_for('home')


def test_home(client):
    response = client.get('/home')
    assert response.status_code == 200
    assert b'Valor de K' in response.data


def test_alterar_k(client):
    response = client.post('/alterar_k', data={'K': '5'}, follow_redirects=True)
    
    assert response.status_code == 200  # Verifica se o redirecionamento foi seguido com sucesso
    assert b'Valor de K alterado para: 5' in response.data  # Verifica se a mensagem flash está presente na página inicial



def test_testar_curriculo_ad(client):
    response = client.post('/testar_curriculo', data={
        'Razão de Experiência': '2',
        'Publicações': '10',
        'Conexões': '100',
        'AD': 'on'
    })
    assert response.status_code == 302
    follow_redirects = client.get('/home')  # Seguir o redirecionamento para /home
    assert 'A qualidade do currículo é' in follow_redirects.get_data(as_text=True)



def test_testar_curriculo_knn(client):
    response = client.post('/testar_curriculo', data={
        'Razão de Experiência': '2',
        'Publicações': '10',
        'Conexões': '100'
    })
    assert response.status_code == 302
    follow_redirects = client.get('/home')  # Seguir o redirecionamento para /home
    assert 'A qualidade do currículo é' in follow_redirects.get_data(as_text=True)


def test_dados_treino(client):
    response = client.get('/dados_treino')
    assert response.status_code == 200
    assert b'Valor de K' in response.data


def test_dados_teste(client):
    response = client.get('/dados_teste')
    assert response.status_code == 200
    assert b'Valor de K' in response.data


def test_dados_teste_ad(client):
    response = client.get('/dados_teste_AD')
    assert response.status_code == 200
    assert b'Valor de K' in response.data
    
def test_dados_teste_sem_dados(client):
    response = client.get('/dados_teste')
    assert response.status_code == 200
    assert b'Valor de K' in response.data
    assert b'Taxa de acertos' in response.data

def test_testar_curriculo_valores_invalidos(client):
    response = client.post('/testar_curriculo', data={
        'Razão de Experiência': 'abc',
        'Publicações': '10',
        'Conexões': '100',
        'AD': 'on'
    })
    assert response.status_code == 302
    follow_redirects = client.get('/home')
    assert 'Erro ao formatar o texto' in follow_redirects.get_data(as_text=True)

def test_testar_curriculo_valores_vazios(client):
    response = client.post('/testar_curriculo', data={
        'Razão de Experiência': '',
        'Publicações': '',
        'Conexões': '',
        'AD': 'on'
    })
    assert response.status_code == 302
    follow_redirects = client.get('/home')
    assert 'Erro ao formatar o texto' in follow_redirects.get_data(as_text=True)
