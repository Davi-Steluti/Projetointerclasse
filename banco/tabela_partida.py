from enum import nonmember

from sqlalchemy import select, func
from sqlalchemy.orm import aliased
from sqlalchemy.sql.elements import or_
from database import  Partida, db_session, Time
from flask import flash, render_template
from sqlalchemy.exc import SQLAlchemyError

def select_todos():

    TimeCasa = aliased(Time)
    TimeVisitante = aliased(Time)

    partidas_sql = (
        select(Partida, TimeCasa, TimeVisitante)
        .join(TimeCasa, Partida.time_casa_id == TimeCasa.id)
        .join(TimeVisitante, Partida.time_visitante_id == TimeVisitante.id)
    )

    partidas_casa = db_session.execute(partidas_sql).all()

    return partidas_casa

def select_quantidade_total():
    partidas_sql = select(func.count(Partida.id))
    qtd_total = db_session.execute(partidas_sql).scalar()
    return qtd_total

def salvar(time_casa_id, time_visitante_id, gols_casa, gols_visitante, data_partida):
    try:
        criar_partida = Partida(time_casa_id=int(time_casa_id), time_visitante_id=int(time_visitante_id), gols_casa=int(gols_casa), gols_visitante=int(gols_visitante), data_partida=data_partida)
        # inicializa a sessão com o banco de dados
        db_session.add(criar_partida)
        db_session.commit()
        flash('Partida criado com sucesso', 'success')
        return render_template('partidas.html')

    except SQLAlchemyError as e:
        db_session.rollback()
        print(f'erro ao salvar no banco: {e}')
        flash('Erro', 'error')
        return render_template('partidas.html')

    except Exception as e:
        db_session.rollback()
        print(f'erro inesperado: {e}')
        flash('Erro inesperado', 'error')
        return render_template('partidas.html')

def select_por_time(id_time):
    TimeCasa = aliased(Time)
    TimeVisitante = aliased(Time)


    partidas_sql = (
        select(Partida, TimeCasa, TimeVisitante)
        .join(TimeCasa, Partida.time_casa_id == TimeCasa.id)
        .join(TimeVisitante, Partida.time_visitante_id == TimeVisitante.id)
        .where(or_(Partida.time_casa_id == id_time, Partida.time_visitante_id == id_time))
    )

    partidas_time = db_session.execute(partidas_sql).all()

    return partidas_time
