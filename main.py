from flask import Flask, render_template, redirect, request, flash
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = 'potygrass'

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.getenv("EMAIL"),
    "MAIL_PASSWORD": os.getenv("SENHA")
}

app.config.update(mail_settings)
mail = Mail(app)


class Contato:
    def __init__(self, nome, email, fone, estado, cidade, quantidade):
        self.nome = nome
        self.email = email
        self.fone = fone
        self.estado = estado
        self.cidade = cidade
        self.quantidade = quantidade


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        formContato = Contato(
            request.form["nome"],
            request.form["email"],
            request.form["fone"],
            request.form["estado"],
            request.form["cidade"],
            request.form["quantidade"]
        )

        msg = Message(
            subject=f'{formContato.nome} Solicitou um orçamento',
            sender=app.config.get("MAIL_USERNAME"),
            recipients=['docencia.thiago@gmail.com', app.config.get("MAIL_USERNAME")],
            body=f'''
            
            NOME:{formContato.nome}  
            E-MAIL:{formContato.email}
            TELEFONE:{formContato.fone}
            ESTADO:{formContato.estado}
            CIDADE:{formContato.cidade}
            QUANTIDADE em M²:{formContato.quantidade}

            '''
        )
        mail.send(msg)
        flash('Mensagem enviada com sucesso!')
    return redirect('/')


@app.route('/contato')
def contato():
    return render_template('contato.html')


@app.route('/potygrass')
def potygrass():
    return render_template('potygrass.html')

if __name__ == '__main__':
    app.run(debug=True)
