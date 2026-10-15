from sqlalchemy import select, func
from database import  Jogador, db_session, Time
from flask import flash, render_template
from sqlalchemy.exc import SQLAlchemyError

def select_todos():
    #1 Montar o select
    # join(Tabela que eu quero juntar, condição = chave estrangeira igual chave primaria)
    jogadores_sql = select(Jogador, Time).join(Time, Jogador.time_id == Time.id)
    #2 Executar o select
    # usar scalars quando tiver somente uma tabela
    jogadores = db_session.execute(jogadores_sql).all()
    return jogadores

def select_quantidade_total():
    jogadores_sql = select(func.count(Jogador.id))
    qtd_total = db_session.execute(jogadores_sql).scalar()
    return qtd_total

def salvar(nome, numero_camisa, posicao, time_id):
    try:
        # cria uma pessoa e adiciona na base de dados
        criar_jogador = Jogador(nome=nome, numero_camisa=int(numero_camisa), posicao=posicao, time_id=int(time_id))
        # inicializa a sessão com o banco de dados
        db_session.add(criar_jogador)
        db_session.commit()
        flash('Jogador criado com sucesso', 'success')

        return render_template('jogadores.html')  # ou render_template adequado

    except SQLAlchemyError as e:
        db_session.rollback()
        print(f'erro ao salvar no banco: {e}')
        flash('Erro ao salvar no banco', 'error')
        return render_template('jogadores.html')

    except Exception as e:
        db_session.rollback()
        print(f'erro inesperado: {e}')
        flash('Erro inesperado', 'error')
        return render_template('jogadores.html')

def select_um(id_jogador):
    jogador_sql = select(Jogador).where(Jogador.id == id_jogador)
    jogador = db_session.execute(jogador_sql).scalar_one_or_none()
    return jogador

#trazer os jogadores de um time
def select_por_time(id_time):
    jogadores_sql = select(Jogador).where(Jogador.time_id == id_time)
    jogadores = db_session.execute(jogadores_sql).scalars().all()
    return jogadores

print(select_por_time(2))
