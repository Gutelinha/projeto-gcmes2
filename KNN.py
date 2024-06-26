import numpy as np
from collections import Counter

def distancia_euclidiana(x1,x2):
    dist = np.sqrt(np.sum(x1-x2)**2)
    return dist


class KNN:
    #inicializa a classe com o valor de k (default = 3)
    def __init__(self, k = 3):
        self.k = k

    def fit(self, x_data, y):
        self._treino_x = x_data
        self._treino_y = y

    def predict(self, x_data):
        previsoes = [self._predict(x) for x in x_data]
        return previsoes

    def _predict(self, x):
        # Calcula a distância euclidiana
        dist = [distancia_euclidiana(x, treino_x) for treino_x in self._treino_x]
        # Pega os k mais próximos
        k_indices = np.argsort(dist)[:self.k]
        k_classes_mais_proximas = [self._treino_y[i] for i in k_indices]
        # Classe majoritária
        majoritaria = Counter(k_classes_mais_proximas).most_common()
        return majoritaria[0][0]
    
    def set_previsao_precisao(self,x,y):
        self.previsoes = self.predict(x) 
        self.precisao = (np.sum(self.previsoes == y)/len(y))*100
        self.precisao = 'Taxa de acertos: '+str(self.precisao) + '%'

