import pandas as pd
import numpy as np
import os

class tratamento_de_dados:
    
    def concatena_atributos(self,experiencia,Pub,conexoes):
        X = [experiencia,Pub,conexoes]
        X = np.asmatrix(X)
        return X
    
    def get_dados_gerais(self):
        try:
            Pasta_Raiz = os.getcwd()
            Pasta_Raiz = os.path.join(Pasta_Raiz, 'dados')
            arquivo = "Dados_Python.xlsx"
            caminho = os.path.join(Pasta_Raiz, arquivo)

            if not os.path.exists(caminho):
                raise FileNotFoundError(f'O arquivo {arquivo} não foi encontrado no diretório {Pasta_Raiz}.')

            dados_gerais = pd.read_excel(caminho, sheet_name='Dados_Python')
            dados_gerais = dados_gerais.drop(['Profissão'], axis=1)
            dados_gerais = dados_gerais.dropna()
            dados_gerais['Experiência'] = dados_gerais['Salário'] / dados_gerais['Experiência']
            dados_gerais = dados_gerais.rename(columns={'Experiência': 'Razão de Experiência'})
            dados_gerais = dados_gerais.drop(['Salário'], axis=1)

            return dados_gerais

        except FileNotFoundError as e:
            print(f'Erro: {e}')
            return None
        
    def get_x(self,dados_gerais):
        x = dados_gerais.loc[:,['Razão de Experiência', 'Publicações', 'Conexões']]
        return x
    
    def get_y(self,dados_gerais):
        Y= dados_gerais.loc[:,'Qualidade']
        return Y

    def get_dados(self,x,y):
        x = pd.DataFrame(x,columns=['Razão de Experiência', 'Publicações', 'Conexões'])
        y = pd.DataFrame(y,columns=['Qualidade'])
        dados = pd.concat([x, y],axis=1, names=['Razão de Experiência', 'Publicações', 'Conexões', 'Qualidade'])
        return dados
    
    def get_dados_teste(self,dados,resposta):
        dados = pd.DataFrame(dados,columns=['Razão de Experiência', 'Publicações', 'Conexões','Qualidade'])
        resposta = pd.DataFrame(resposta,columns=['Valor gerado'])
        dados = pd.concat([dados,resposta],axis=1, names=['Razão de Experiência', 'Publicações', 'Conexões', 'Qualidade','Valor gerado'])
        return dados
