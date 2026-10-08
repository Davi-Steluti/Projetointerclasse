from flask import Flask, render_template, request, redirect, url_for, flash
# from sqlalchemy import select

from banco import tabela_time, tabela_jogador, tabela_partida
# from database import Time, Jogador, Partida, db_session
# from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.secret_key = "chave-secreta-interclasse-2026"


@app.route("/")
def dashboard():
    jogadores = tabela_jogador.select_quantidade_total()
    times = tabela_time.select_quantidade_total()
    partidas = tabela_partida.select_quantidade_total()

    return render_template(
        "dashboard.html",
        total_jogadores=jogadores,
        total_times=times,
        total_partidas=partidas,
    )


@app.route("/jogadores")
def listar_jogadores():
    jogadores = tabela_jogador.select_todos()
    times = tabela_time.select_todos()


    return render_template("jogadores.html", jogadores=jogadores, times=times)


@app.route("/jogadores/novo", methods=["GET", "POST"])
def novo_jogador():

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        numero_camisa = request.form.get("numero_camisa") or None
        posicao = request.form.get("posicao", "").strip()
        time_id = request.form.get("time_id") or None

        if not nome:
            flash('Preencha o nome', 'error')
            return render_template('jogadores.html')

        if not numero_camisa:
            flash('Preencha o numero da camisa', 'error')
            return render_template('jogadores.html')

        if not posicao:
            flash('Preencha a posição', 'error')
            return render_template('jogadores.html')

        if not time_id:
            flash('Preencha o time', 'error')
            return render_template('jogadores.html')

        #Salvar no banco
        tabela_jogador.salvar(nome=nome, numero_camisa=numero_camisa, posicao=posicao, time_id=time_id)

    times = tabela_time.select_todos()
    jogadores = tabela_jogador.select_todos()
    return render_template("jogadores.html", jogadores=jogadores, times=times)


@app.route("/times")
def listar_times():
    #Buscar todos os times
    times = tabela_time.select_todos()
    return render_template("times.html", times=times)


@app.route("/times/novo", methods=["GET", "POST"])
def novo_time():

    if request.method == "POST":
        #1- Pegar os valores digitados no form
        nome = request.form.get("nome", "").strip()
        turma = request.form.get("turma", "").strip()
        responsavel = request.form.get("responsavel", "").strip()

        #2- Verificar se foi digitado
        if not nome:
            flash('Preencha o nome', 'error')
            return render_template('times.html')

        if not turma:
            flash('Preencha a turma', 'error')
            return render_template('times.html')

        if not responsavel:
            flash('Preencha o responsavel', 'error')
            return render_template('times.html')

        #3- Salvar no banco
        tabela_time.salvar(nome=nome, turma=turma, responsavel=responsavel)

    times = tabela_time.select_todos()
    return render_template("times.html", times=times)


@app.route("/partidas")
def listar_partidas():
    partidas = tabela_partida.select_todos()
    times = tabela_time.select_todos()

    return render_template("partidas.html", partidas=partidas, times=times)


@app.route("/partidas/nova", methods=["GET", "POST"])
def nova_partida():

    if request.method == "POST":
        time_casa_id = request.form.get("time_casa_id")
        time_visitante_id = request.form.get("time_visitante_id")
        gols_casa = request.form.get("gols_casa") or 0
        gols_visitante = request.form.get("gols_visitante") or 0
        data_partida = request.form.get("data_partida", "").strip()

        if not time_casa_id:
            flash('Preencha o time da casa', 'error')
            return render_template('partidas.html')

        if not time_visitante_id:
            flash('Preencha o time visitante', 'error')
            return render_template('partidas.html')

        if not gols_casa:
            flash('Preencha os gols da casa', 'error')
            return render_template('partidas.html')

        if not gols_visitante:
            flash('Preencha os gols do visitante', 'error')
            return render_template('partidas.html')

        if not data_partida:
            flash('Preencha a data', 'error')
            return render_template('partidas.html')

        if time_casa_id == time_visitante_id:
            flash('Preencha de times diferentes', 'error')
            return render_template('partidas.html')


        # 3- Salvar no banco
        tabela_partida.salvar(time_casa_id=time_casa_id, time_visitante_id=time_visitante_id, gols_casa=gols_casa, gols_visitante=gols_visitante, data_partida=data_partida)

    partidas = tabela_partida.select_todos()
    times = tabela_time.select_todos()
    return render_template("partidas.html", partidas=partidas, times=times)


if __name__ == "__main__":
    app.run(debug=True)
