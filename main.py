from flask import Flask, render_template, url_for, flash, request, redirect
from Services import tratamento_de_dados
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import numpy as np
from KNN import KNN

#inicializa o flask
app = Flask(__name__)
app.secret_key = 'Projeto_IA'

#inicializa o objeto de tratamento de dados
action = tratamento_de_dados()

#busca os dados do arquivo excel
dados_gerais = action.get_dados_gerais()
print(dados_gerais)
#converte os dados para tuplas x,y
X = action.get_x(dados_gerais)
Y = action.get_y(dados_gerais) 
#separa os casos de teste e treino
treino_x, teste_x, treino_y, teste_y =  train_test_split(X.to_numpy(),Y.to_numpy(), test_size= 0.2, random_state=1234) 


#inicializa o objeto AD
tree = DecisionTreeClassifier()
#insere os dados de treino
tree.fit(treino_x,treino_y)
#recupera os resultados do teste
prec = tree.predict(teste_x)
print (prec)
#% de acertos do modelo
prev = (np.sum(prec == teste_y)/len(teste_y))*100
prev = 'Taxa de acertos: '+str(prev) + '%'
print(prev)

#inicializa o objeto KNN
clf = KNN()
#insere os dados de treino
clf.fit(treino_x,treino_y)
#recupera os resultados do teste
clf.set_previsao_precisao(teste_x,teste_y)
previsoes = clf.previsoes
precisao = clf.precisao
#% de acertos do modelo
print(precisao)










########################################################
##################PAGINA PRINCIPAL######################
@app.route('/')
def inicio():
    
    return redirect(url_for('home'))

@app.route('/home')
def home():
    
    return render_template(
        'home.html',
        valor_k = 'Valor de K: '+str(clf.k)
    )

@app.route('/alterar_k',methods=['GET','POST'])
def alterar_k():
    try:
        k = request.form['K']
        
        X = clf.k = int (k)
        clf.fit(treino_x,treino_y)
        clf.set_previsao_precisao(teste_x,teste_y)
        print(clf.precisao)

        
        flash('Valor de K alterado para: ' + str(clf.k), 'SUCESSO_1')
        return redirect(url_for('home'))
    
    except Exception as e:
        print(e)
        flash('Erro ao formatar o texto', 'ERRO_1')
        return redirect(url_for('home'))

@app.route('/testar_curriculo',methods=['GET','POST'])
def testar_curriculo():
    try:
        exp = request.form['Razão de Experiência']
        pub = request.form['Publicações']
        con = request.form['Conexões']
        
        X = action.concatena_atributos(int(exp),int(pub),int(con))
        if 'AD' in request.form:
            X = tree.predict(np.asarray(X.flatten()))
            print('ad')
        else:
            X = clf.predict(X)
            print('knn')
        
        flash('A qualidade do currículo é: ' + X[0], 'SUCESSO_2')
        return redirect(url_for('home'))
    except Exception as e:
        print(e)
        flash('Erro ao formatar o texto', 'ERRO_2')
        return redirect(url_for('home'))
    


########################################################
##################PAGINAS DE DADOS######################
@app.route('/dados_treino')
def dados_treino():
    r_dados = action.get_dados(treino_x,treino_y)
    return render_template(
        'dados_treino.html',
        dados = r_dados,
        valor_k = 'Valor de K: '+str(clf.k)
    )

@app.route('/dados_teste')
def dados_teste():
    previsoes = clf.previsoes
    precisao = clf.precisao
    r_dados = action.get_dados_teste(action.get_dados(teste_x, teste_y),previsoes)
    return render_template(
        'dados_teste.html',
        dados = r_dados,
        precisao = precisao,
        valor_k = 'Valor de K: '+str(clf.k)
    )

@app.route('/dados_teste_AD')
def dados_teste_AD():
    r_dados = action.get_dados_teste(action.get_dados(teste_x,teste_y),prec)
    return render_template(
        'dados_teste_AD.html',
        dados = r_dados,
        precisao = prev,
        valor_k = 'Valor de K: '+str(clf.k)
    )



app.run()
