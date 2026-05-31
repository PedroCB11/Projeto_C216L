
from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = "secret"

API_URL = "http://backend:8000/api/v1/professores"


def aluno_from_api(registro):
    aluno = dict(registro)
    aluno["curso"] = aluno.get("curso") or aluno.get("sala_de_atendimento", "")
    return aluno

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        data = {
            "nome": request.form["nome"],
            "email": request.form["email"],
            "sala_de_atendimento": request.form["curso"]
        }
        response = requests.post(API_URL + "/", json=data)
        if response.status_code == 201:
            flash("Aluno cadastrado com sucesso!", "success")
            return redirect(url_for("alunos"))
        else:
            flash(response.json().get("detail", "Erro ao cadastrar aluno."), "danger")
    return render_template("cadastro.html")

@app.route("/alunos")
def alunos():
    response = requests.get(API_URL + "/")
    alunos = [aluno_from_api(item) for item in response.json()] if response.ok else []
    return render_template("alunos.html", alunos=alunos)

@app.route("/professores")
def professores_redirect():
    return redirect(url_for("alunos"))

@app.route("/editar/<int:aluno_id>", methods=["GET", "POST"])
def editar(aluno_id):
    if request.method == "POST":
        data = {
            "nome": request.form["nome"],
            "email": request.form["email"],
            "sala_de_atendimento": request.form["curso"]
        }
        response = requests.patch(f"{API_URL}/{aluno_id}", json=data)
        if response.ok:
            flash("Aluno atualizado com sucesso!", "success")
        else:
            flash("Erro ao atualizar aluno.", "danger")
        return redirect(url_for("alunos"))
    else:
        aluno = aluno_from_api(requests.get(f"{API_URL}/{aluno_id}").json())
        return render_template("editar.html", aluno=aluno)

@app.route("/excluir/<int:aluno_id>")
def excluir(aluno_id):
    response = requests.delete(f"{API_URL}/{aluno_id}")
    if response.ok:
        flash("Aluno removido com sucesso!", "success")
    else:
        flash("Erro ao remover aluno.", "danger")
    return redirect(url_for("alunos"))

@app.route("/reset")
def reset():
    response = requests.delete(API_URL + "/")
    if response.ok:
        flash("Banco de dados resetado com sucesso!", "info")
    else:
        flash("Erro ao resetar banco.", "danger")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True, port=3000, host="0.0.0.0")
