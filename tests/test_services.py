import pytest
import pandas as pd
import numpy as np
from Services import tratamento_de_dados

@pytest.fixture
def dados():
    print("Running fixture: dados")
    return {
        "Profissão": ['Engenheiro', 'Médico', 'Advogado'],
        "Salário": [5000, 7000, 6000],
        "Experiência": [5, 7, 6],
        "Publicações": [10, 20, 30],
        "Conexões": [100, 200, 300],
        "Qualidade": ['Bom', 'Ruim', 'Bom']
    }

@pytest.fixture
def tratamento():
    print("Running fixture: tratamento")
    return tratamento_de_dados()

def test_concatena_atributos(tratamento):
    print("Running test: test_concatena_atributos")
    X = tratamento.concatena_atributos(1, 2, 3)
    assert X.shape == (1, 3)
    assert (X == np.asmatrix([1, 2, 3])).all()

def test_get_dados_gerais(mocker, tratamento, dados):
    print("Running test: test_get_dados_gerais")
    mocker.patch('os.getcwd', return_value='.')
    mocker.patch('pandas.read_excel', return_value=pd.DataFrame(dados))
    
    result = tratamento.get_dados_gerais()
    assert isinstance(result, pd.DataFrame)
    assert 'Razão de Experiência' in result.columns
    assert 'Publicações' in result.columns
    assert 'Conexões' in result.columns

def test_get_x(tratamento, dados):
    print("Running test: test_get_x")
    dados_df = pd.DataFrame(dados)
    dados_df['Razão de Experiência'] = dados_df['Salário'] / dados_df['Experiência']
    x = tratamento.get_x(dados_df)
    assert isinstance(x, pd.DataFrame)
    assert list(x.columns) == ['Razão de Experiência', 'Publicações', 'Conexões']

def test_get_y(tratamento, dados):
    print("Running test: test_get_y")
    dados_df = pd.DataFrame(dados)
    y = tratamento.get_y(dados_df)
    assert isinstance(y, pd.Series)
    assert y.name == 'Qualidade'

def test_get_dados(tratamento, dados):
    print("Running test: test_get_dados")
    x = pd.DataFrame(dados).drop(columns=['Qualidade'])
    x['Razão de Experiência'] = x['Salário'] / x['Experiência']
    x = x.drop(columns=['Profissão', 'Salário'])
    y = pd.Series(dados['Qualidade'])
    dados_concat = tratamento.get_dados(x, y)
    assert isinstance(dados_concat, pd.DataFrame)
    assert list(dados_concat.columns) == ['Razão de Experiência', 'Publicações', 'Conexões', 'Qualidade']

def test_get_dados_teste(tratamento, dados):
    print("Running test: test_get_dados_teste")
    dados_df = pd.DataFrame(dados)
    dados_df['Razão de Experiência'] = dados_df['Salário'] / dados_df['Experiência']
    dados_df = dados_df.drop(columns=['Profissão', 'Salário'])
    resposta = ['Bom', 'Ruim', 'Bom']
    dados_teste = tratamento.get_dados_teste(dados_df, resposta)
    assert isinstance(dados_teste, pd.DataFrame)
    assert list(dados_teste.columns) == ['Razão de Experiência', 'Publicações', 'Conexões', 'Qualidade', 'Valor gerado']