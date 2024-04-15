# criar as rotas do nosso site (os links)
from flask import Flask, render_template, url_for, redirect
#.. redirect redireciona o para um link específico
from fakepinterest import app, database, bcrypt
from fakepinterest.models import Usuario, Foto
from flask_login import login_required, login_user, logout_user, current_user
#.. login_required função para exigir um login do usuario
#.. login_user função para fazer o ligin de um usuário
#.. current_user é o usuario que já está logado
from fakepinterest.forms import FormLogin, FormCriarConta, FormFoto
import os
from werkzeug.utils import secure_filename
#.. Werkzeug da biblioteca "os", checa e modifica o nome de um arquivo para nome seguro

@app.route("/", methods=["GET", "POST"])
def homepage():
    formlogin = FormLogin()
    if formlogin.validate_on_submit():
        #Procurar o usuario
        usuario = Usuario.query.filter_by(email=formlogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, formlogin.senha.data):
        #.. no bcrypt passar 2 parametro: a senha criptografada e a senha que o usuario preencheo no form
            login_user(usuario)
            return redirect(url_for("perfil", id_usuario=usuario.id))
            bcrypt.check_password_hash(usuario.senha, formlogin.senha.data)
    return render_template("homepage.html", form=formlogin)

@app.route("/criarconta", methods=["GET", "POST"])
def criarconta():
    formcriarconta = FormCriarConta()
    if formcriarconta.validate_on_submit():
        senha = bcrypt.generate_password_hash(formcriarconta.senha.data)
        #para visualizar a senha deve usar bcrypt.check.password.hash(senha)
        usuario = Usuario(username=formcriarconta.username.data,
                          senha=senha, email=formcriarconta.email.data)
        #.. instalar: pip install email_validator

        #Aqui o database adiciona os dados temporariamente mas não grava
        database.session.add(usuario)
        #O Commit grava todas as informações adicionada na seção
        database.session.commit()
        #fazer o login do usuario antes de ser redirecionaldo para o seu perfil
        login_user(usuario, remember=True)
        #.. remember: para o sistema lembrar que o usuario já está logado

        #será redirecionado para o link "perfil" com os dados do "usuario"
        return redirect(url_for("perfil", id_usuario=usuario.id))
        #passar o id_usuario para o perfil pq é unico para cada usuario
    return render_template("criarconta.html", form=formcriarconta)

#O parametro aqui deve ser um campo que seja único
@app.route("/perfil/<id_usuario>", methods=["GET", "POST"])
@login_required #só permite se o usuario estiver logado
def perfil(id_usuario):
    if int(id_usuario) == int(current_user.id):
        #o usuario está vendo o perfil dele
        form_foto = FormFoto()
        if form_foto.validate_on_submit():
            #1) Pegar o arquivo
            arquivo = form_foto.foto.data
            #2) Mudar o nome de arquivo para um nome seguro
            nome_seguro = secure_filename(arquivo.filename)
            #3) Salvar o arquivo na pastas de destino (foto_post)
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                              app.config["UPLOAD_FOLDER"], nome_seguro)
            #.. os.path.join concatena os dados do parâmetro
            #.. os.path.abspath é o caminho absoluto do os.path.dirname
            #.. __file__ é o próprio arquivo em que está escrito, nesse caso, Routes.py
            # app.config é uma variável definida no __init__.py

            arquivo.save(caminho)
            #4) Registrar o arquivo no banco de dados
            foto = Foto(imagem=nome_seguro, id_usuario=current_user.id)
            #.. Foto() deve ser importado do fakepinterest.models
            #.. Aqui tanto pode ser usado int(id_usuario) como o current_user.id
            database.session.add(foto)
            database.session.commit()
        return render_template("perfil.html", usuario=current_user, form=form_foto)
        #.. Aqui o form_foto será repassado pq será o próprio usuário
    else:
        #procura o id do usuario
        usuario = Usuario.query.get(int(id_usuario))
        return render_template("perfil.html", usuario=usuario, form=None)
        #.. Aqui o form_foto não será repassado pq será outro usuário

@app.route("/logout")
@login_required  #só permite se o usuario estiver logado
def logout(): #aqui poderia colocar o current_user como parametro
    login_user(current_user)
    return redirect(url_for("homepage"))

@app.route("/feed")
@login_required #só permite se o usuario estiver logado
def feed():
    fotos = Foto.query.order_by(Foto.data_criacao).all()
    #.. Perquisa por ordem da data de criação e será todas as fotos
    #.. Se precisa limitar a quantidade, deve preencher .all().[:100], neste
    # exemplo, até 100
    #.. Se precisar ordenar inversamente, (Foto.data_criacao).desc().all()
    return render_template("feed.html", fotos=fotos)
