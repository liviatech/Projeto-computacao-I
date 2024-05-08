from flask import Flask, request, render_template, redirect, jsonify, session
import mysql.connector

# A chave secreta é usada para assinar os cookies de sessão, garantindo que não possam ser falsificados ou manipulados por terceiros
app = Flask(__name__)

#
app.secret_key = 'teste'

# Conexão com o banco de dados MySQL
conn = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="teste50",
    database="projeto"
)
cursor = conn.cursor()

# Rota para a página de inical
@app.route('/')
def pagina_login():
    return render_template('index.html')

@app.route('/home')
def home_inicial():
    return render_template('index.html')

# Rota para a página de login
@app.route('/login')
def login():
    return render_template('login2.html')

# Rota para a página de cadastro responsável
@app.route('/cadastro')
def cadastro():
    return render_template('cadastro3.html')


@app.route('/salvar-dados', methods=['POST'])
def salvar_dados():
    data = request.json
    nome = data.get('nome')
    sobrenome = data.get('sobrenome')
    nick = data.get('nick')
    datanascimento = data.get('datanascimento')
    dependentes = data.get('dependentes')
    telefone = data.get('telefone')
    email = data.get('email')
    senha = data.get('senha')
    genero = data.get('genero')
    
  
    dados = (nome, sobrenome, nick, datanascimento, dependentes, telefone, email, senha, genero)
    print(dados)

    # Consulta SQL para inserir os dados no banco de dados
    cursor.execute("INSERT INTO responsavel (nome, sobrenome, nick, datanascimento, dependentes, telefone, email, senha, genero) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (nome, sobrenome, nick, datanascimento, dependentes, telefone, email, senha, genero))
       
    # cursor.execute("SELECT * FROM responsavel")
    # responsavel = cursor.fetchone()
    # responsavel_id = responsavel[0] 
    
    # cursor.execute("INSERT INTO dependente (id_resp, nomed, datanascimentod, emaild, senhad) VALUES (%s, %s, %s, %s, %s)", (responsavel_id, nomed, datanascimentod, emaild, senhad))
    conn.commit()
    
    return render_template('login2.html')

# Rota para verificar as credenciais de login e redirecionar para home de acesso
@app.route('/verificar-login', methods=['POST'])
def verificar_login():
    data = request.json
    login = data['login']
    senha = data['senha']
    

    # Consulta SQL para verificar o login no banco de dados
    cursor.execute("SELECT * FROM responsavel WHERE email = %s AND senha = %s", (login, senha))
    responsavel = cursor.fetchone()
    print(responsavel)
    
    cursor.execute("SELECT * FROM dependente WHERE emaild = %s AND senhad = %s", (login, senha))
    dependente = cursor.fetchone()
    
    if responsavel:
        resp_id = responsavel[0]
        session['resp_id'] = resp_id 
        return redirect(f'/home_resp')
    elif dependente:
        return redirect(f'/home_resp')
    else:
        return jsonify({'mensagem': 'Login inválido'}), 401

# Rota para a página de login
@app.route('/home_resp')
def home_resp():
    return render_template('e-home-resp.html')

# Rota para a página de login
@app.route('/cadastro_dependente')
def cadastro_dependente():
    return render_template('cadastro_dependente4.html')

@app.route('/dados-dependente', methods=['POST'])
def dados_dependente():
    data = request.json
    nome = data.get('nome')
    sobrenome = data.get('sobrenome')
    nick = data.get('nick')
    datanascimento = data.get('datanascimento')
    telefone = data.get('telefone')
    email = data.get('email')
    senha = data.get('senha')
    genero = data.get('genero')
    
    id_resp = session['resp_id']

    dados = (nome, sobrenome, nick, datanascimento, telefone, email, senha, genero)
    print(dados)

    cursor.execute("INSERT INTO dependente (nomed, sobrenomed, nickd, datanascimentod, telefoned, emaild, senhad, generod, id_resp_dep) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (nome, sobrenome, nick, datanascimento, telefone, email, senha, genero, id_resp))
    conn.commit()
    
    return render_template('e-home-resp.html')


# Rota para cadastro dependente
@app.route('/formulario')
def formulario():
    return render_template('cadastro3.html')



     # Redirecionar para a próxima página
    return redirect(f'/login')

  
if __name__ == '__main__':
    app.run(debug=True)    
