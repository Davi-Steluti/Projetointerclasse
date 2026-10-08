from sqlalchemy import select, func
from database import Time, db_session, Jogador
from flask import flash, render_template
from sqlalchemy.exc import SQLAlchemyError

def select_todos():
    times_sql = (
        select(Time, func.count(Jogador.id).label('jogadores'))
        .outerjoin(Jogador, Jogador.time_id == Time.id)
        .group_by(Time.id)
    )
    times = db_session.execute(times_sql).all()
    return times

def select_quantidade_total():
    times_sql = select(func.count(Time.id))
    qtd_total = db_session.execute(times_sql).scalar()
    return qtd_total

# Só pa testa
# print(select_quantidade_total())

def salvar(nome, turma, responsavel):
    try:
        criar_time = Time(nome=nome, turma=turma, responsavel=responsavel)
        # inicializa a sessão com o banco de dados
        db_session.add(criar_time)
        db_session.commit()
        flash('Time criado com sucesso', 'success')
        return render_template('times.html')

    except SQLAlchemyError as e:
        db_session.rollback()
        print(f'erro ao salvar no banco: {e}')
        flash('Erro', 'error')
        return render_template('times.html')

    except Exception as e:
        db_session.rollback()
        print(f'erro inesperado: {e}')
        flash('Erro inesperado', 'error')
        return render_template('times.html')