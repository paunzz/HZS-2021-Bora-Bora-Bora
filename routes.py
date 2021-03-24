import datetime
import re
from datetime import datetime

from flask import render_template, request, redirect, session as flask_session, url_for, Blueprint
from sqlalchemy.exc import IntegrityError

import utils
from base import session
from models import Event, Info
from scraper import *

dogadjaji = Blueprint('dogadjaji', __name__)


@dogadjaji.route('/', methods=['GET'])
def index():
    events = session.query(Event).all()
    flags = utils.get_flags(events)
    return render_template('index.html', list=[[n.name, n.date, flag] for (n, flag) in zip(events, flags)])

@dogadjaji.route('/fudbal', methods=['POST', 'GET'])
def fudbal():
    c = scrape_football()
    flags = utils.get_flags(['']*len(c.items()))
    return render_template('index.html', list=[[event, flag] for (event, flag) in zip(c.items(), flags)])

@dogadjaji.route('/kosarka', methods=['POST', 'GET'])
def kosarka():
    c = scrape_football()
    print(c)
    return render_template('index.html', list=[[]])

@dogadjaji.route('/tenis', methods=['POST', 'GET'])
def tenis():
    c = scrape_football()
    print(c)
    return render_template('index.html', list=[[]])

@dogadjaji.route('/moji', methods=['POST', 'GET'])
def moji():
    c = scrape_football()
    print(c)
    return render_template('index.html', list=[[]])

@dogadjaji.route('/', methods=['POST'])
def event():
    if request.method == 'POST':
        if request.form['submit_button'] == 'event':
            id1 = session.query(Event).count()
            event_name = request.form.get('event_name')
            event_date = request.form.get('event_date')
            if event_name != event_date != '':
                new_event = Event(id1=id1, name=event_name, date=event_date)
                session.add(new_event)
                session.flush()

                session.commit()
                events = session.query(Event).all()
                flags = utils.get_flags(events)
                return render_template('index.html',
                                       list=[[n.name, n.date, flag] for (n, flag) in zip(events, flags)])
            else:
                rroute = '/'
                err_code = 'Neispravni podaci dogadjaja!'
                return render_template('greska.html', error_code=err_code, redirect_route=rroute)


@dogadjaji.route('/dogadjaji/<id1>', methods=['POST', 'GET'])
def open(id1=None):
    if request.method == 'GET' or request.form['submit_button'] == 'open':
        flask_session['id1'] = id1
        return render_template('spisak.html')

    elif request.form['submit_button'] == 'delete':

        session.query(Event).filter(Event.id1 == id1).delete()

        session.commit()

        return redirect(url_for('dogadjaji.index'))


@dogadjaji.route('/radnik_dodat', methods=['POST'])
def new_worker():
    id1 = flask_session.get('id1')
    if request.method == 'POST':
        if request.form['new_worker'] == 'new_worker':
            worker_jmbg = request.form.get('jmbg')
            worker_full_name = request.form.get('full_name')
            start_date = request.form.get('start_date')
            termination_date = request.form.get('termination_date')

            if start_date:
                try:
                    start_date_object = datetime.strptime(start_date, '%d/%m/%Y')
                    worker_start_date = start_date_object.strftime('%Y-%m-%d')
                except ValueError:
                    session.rollback()
                    rroute = '/dogadjaji'
                    err_code = 'Neispravan datum prijave!'
                    return render_template('greska.html', error_code=err_code, redirect_route=rroute)
                if termination_date:
                    try:
                        termination_date_object = datetime.strptime(termination_date, '%d/%m/%Y')
                        worker_termination_date = termination_date_object.strftime('%Y-%m-%d')
                    except ValueError:
                        session.rollback()
                        rroute = '/dogadjaji'
                        err_code = 'Neispravan datum odjave!'
                        return render_template('greska.html', error_code=err_code, redirect_route=rroute)
                else:
                    worker_termination_date = None

            if worker_full_name and worker_start_date and \
                    re.match(r'\d{13}', worker_jmbg):
                try:
                    new_worker = Info(jmbg=worker_jmbg,
                                        full_name=worker_full_name,
                                        contract_termination_date=worker_termination_date,
                                        contract_start_date=worker_start_date,
                                        event_date=id1)
                    session.add(new_worker)
                    session.flush()
                except IntegrityError as e:
                    print(e._message())
                    session.rollback()
                    rroute = '/dogadjaji'
                    err_code = 'Radnik sa ovim JMBG-om vec postoji!'
                    return render_template('greska.html', error_code=err_code, redirect_route=rroute)

                session.commit()
                company = session.query(Event).filter(Event.id1 == id1).one()
                workers = session.query(Info).filter(Info.event_date == id1).all()
                flags = utils.get_worker_flags(workers)
                return render_template('spisak.html',
                                       workers=[[worker, flag] for (worker, flag) in zip(workers, flags)],
                                       company=company.name)
            else:
                rroute = '/dogadjaji'
                err_code = 'Neispravni podaci radnika!'
                return render_template('greska.html', error_code=err_code, redirect_route=rroute)


@dogadjaji.route('/dogadjaji', methods=['GET'])
def update():
    id1 = flask_session.get('id1')
    company = session.query(Event).filter(Event.id1 == id1).one()
    workers = session.query(Info).filter(Info.event_date == id1).all()
    flags = utils.get_worker_flags(workers)
    return render_template('spisak.html',
                           workers=[[worker, flag] for (worker, flag) in zip(workers, flags)],
                           company=company.name)


@dogadjaji.route('/dogadjaji/delete/<worker_jmbg>', methods=['POST'])
def delete(worker_jmbg=None):
    if request.method == "POST":
        worker_row_to_delete = session.query(Info).filter(Info.jmbg == worker_jmbg).one()
        session.delete(worker_row_to_delete)
        session.commit()
        return redirect(url_for('dogadjaji.update'))


@dogadjaji.route('/dogadjaji/edit_company/<id1>', methods=['POST'])
def edit_company(id1=None):
    print('edit company')
    company = session.query(Event).filter(Event.id1 == id1).one()
    return render_template('edit_company.html', id11=company.id1, name=company.name)

@dogadjaji.route('/dogadjaji/save_company/<id1>', methods=['POST', 'GET'])
def company_save(id1=None):
    print(f'change {id1}')

    new_name = request.form.get('new_name')
    new_id1 = request.form.get('new_id1')

    company_row_to_change = session.query(Event).filter(Event.id1 == id1).one()
    workers = session.query(Info).filter(Info.event_date == id1).all()
    for worker in workers:
        print(worker.event_date, new_id1)
        print(worker.event_date)

    if new_name:
        company_row_to_change.name = new_name

    if new_id1:
        company_row_to_change.id1 = new_id1

    try:

        session.add(company_row_to_change, workers)
        session.flush()

    except IntegrityError as e:
        print(e.__cause__)
        session.rollback()
        rroute = '/'
        err_code = 'Firma sa ovim PIB-om vec postoji!'

        return render_template('greska.html', error_code=err_code, redirect_route=rroute)

    session.commit()

    return redirect(url_for('dogadjaji.index'))

@dogadjaji.route('/dogadjaji/edit/<worker_jmbg>', methods=['POST'])
def edit(worker_jmbg=None):
    worker = session.query(Info).filter(Info.jmbg == worker_jmbg).one()
    return render_template('edit.html', worker_jmbg=worker_jmbg, worker=worker, id1=flask_session['id1'])


@dogadjaji.route('/dogadjaji/save/<worker_jmbg>', methods=['POST', 'GET'])
def save(worker_jmbg=None):

    new_jmbg = request.form.get('new_jmbg')
    new_name = request.form.get('new_name')
    subm_date = request.form.get('subm_date')
    term_date = request.form.get('term_date')

    worker_row_to_change = session.query(Info).filter(Info.jmbg == worker_jmbg).one()

    if new_jmbg:
        worker_row_to_change.jmbg = new_jmbg

    if new_name:
        worker_row_to_change.full_name = new_name

    if subm_date:
        start_date_object = datetime.strptime(subm_date, '%d/%m/%Y')
        worker_start_date = start_date_object.strftime('%Y-%m-%d')
        worker_row_to_change.contract_start_date = worker_start_date

    if term_date == '' or term_date == "Neodređeno":
        term_date = None

    if term_date:
        term_date = datetime.strptime(term_date, '%d/%m/%Y')

    worker_row_to_change.contract_termination_date = term_date

    try:
        session.add(worker_row_to_change)
        session.flush()

    except IntegrityError:
        session.rollback()
        rroute = '/dogadjaji'
        err_code = 'Radnik sa ovim JMBG-om vec postoji!'

        return render_template('greska.html', error_code=err_code, redirect_route=rroute)

    session.commit()

    return redirect(url_for('dogadjaji.update'))