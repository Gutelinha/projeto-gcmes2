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
    assert response.headers['Location'] == 'http://localhost/home'


def test_home(client):
    response = client.get('/home')
    assert response.status_code == 200
    assert b'Valor de K' in response.data


def test_alterar_k(client):
    response = client.post('/alterar_k', data={'K': '5'})
    assert response.status_code == 302
    assert b'Valor de K alterado para: 5' in response.data


def test_testar_curriculo_ad(client):
    response = client.post('/testar_curriculo', data={
        'Razão de Experiência': '2',
        'Publicações': '10',
        'Conexões': '100',
        'AD': 'on'
    })
    assert response.status_code == 302
    assert 'A qualidade do currículo é' in response.get_data(as_text=True)


def test_testar_curriculo_knn(client):
    response = client.post('/testar_curriculo', data={
        'Razão de Experiência': '2',
        'Publicações': '10',
        'Conexões': '100'
    })
    assert response.status_code == 302
    assert 'A qualidade do currículo é' in response.get_data(as_text=True)

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
