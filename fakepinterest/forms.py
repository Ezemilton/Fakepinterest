# criar os formullarios do nosso site
# Instalar flask-wtf: pip install flask-wtf => estrutura de formulário
# Instalar validação de e-mail: pip install email-validator => verifica se e-mail é válido
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
#.. StringField é um campo de texto
#.. PasswordField é um campo de senha
#.. SubmitField e um botão de confirmação
#.. FileField é um campo de arquivo
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from fakepinterest.models import Usuario

class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    botao_confirmacao = SubmitField("Fazer Login")

    def validate_email(self, email): #valida a variável email e busca no BD para submeter
        usuario = Usuario.query.filter_by(email=email.data).first() #a 1ª (verm)) de pesquisa a (branca) é o campo do formuario
        #.. quando pesquisa por id usa get(), quando pesquisa por outra caracteristica usa filter_by()
        #.. o resultado da pesquisa retorna uma lista de email e com first seleciona a primeira da lista
        if not usuario:
            raise ValidationError("Usuário inexistente, crie uma conta")


class FormCriarConta(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    username = StringField("Nome de Usuário", validators=[DataRequired()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha =PasswordField("Confirmação de Senha", validators=[DataRequired(), EqualTo("senha")])
    botao_confirmacao = SubmitField("Criar Conta")

                             #aqui recebe a variavel email como padrao
    def validate_email(self, email): #valida a variável email e busca no BD para submeter
        usuario = Usuario.query.filter_by(email=email.data).first() #a 1ª (verm)) de pesquisa a (branca) é o campo do formuario
        #.. quando pesquisa por id usa get(), quando pesquisa por outra caracteristica usa filter_by()
        #.. o resultado da pesquisa retorna uma lista de email e com first seleciona a primeira da lista
        if usuario:
            raise ValidationError("e-mail já cadastrado, faça login")

#Formulário para mostrar as fotos
class FormFoto(FlaskForm):
    foto=FileField("Foto", validators=[DataRequired()])
    botao_confirmacao = SubmitField("Enviar")













