import pytest
import numpy as np
from KNN import KNN, distancia_euclidiana

def test_distancia_euclidiana():
    print("Running test: test_distancia_euclidiana")
    assert distancia_euclidiana(np.array([1, 2]), np.array([4, 6])) == 7

@pytest.fixture
def knn():
    print("Running fixture: knn")
    return KNN(k=3)

def test_knn_fit(knn):
    print("Running test: test_knn_fit")
    X = np.array([[1, 2], [3, 4], [5, 6]])
    y = np.array(['Bom', 'Ruim', 'Bom'])
    knn.fit(X, y)
    assert (knn._treino_x == X).all()
    assert (knn._treino_y == y).all()

def test_knn_predict(knn):
    X = np.array([[1, 2], [3, 4], [5, 6]])
    y = np.array(['Bom', 'Ruim', 'Bom'])
    knn.fit(X, y)
    pred = knn.predict(X)
    assert len(pred) == len(X)

def test_knn_set_previsao_precisao(knn):
    X = np.array([[1, 2], [3, 4], [5, 6]])
    y = np.array(['Bom', 'Ruim', 'Bom'])
    knn.fit(X, y)
    knn.set_previsao_precisao(X, y)
    assert hasattr(knn, 'previsoes')
    assert hasattr(knn, 'precisao')
    assert isinstance(knn.precisao, str)
    assert 'Taxa de acertos' in knn.precisao
