#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Flask, request, render_template, redirect, flash, g, session  # , url_for, abort

import pymysql.cursors

app = Flask(__name__)
app.secret_key = 'une cle(token) : grain de sel(any random string)'


def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host="localhost",
            user="tbertome",
            password="0404",
            database="BDD_Activite_Localisation",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db


@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


@app.route('/')
def show_accueil():
    mycursor = get_db().cursor()

    sql = "SELECT * FROM activite;"
    mycursor.execute(sql)
    activite = mycursor.fetchall()

    return render_template('layout.html', activite=activite)


# ----- ACTIVITE ----- #

@app.route('/activite/show')
def show_activite():
    mycursor = get_db().cursor()

    sql = "SELECT * FROM activite ORDER BY id_activite;"
    mycursor.execute(sql)
    activite = mycursor.fetchall()

    sql = "SELECT SUM(cout_inscription*nb_participants) AS recettes FROM activite;"
    mycursor.execute(sql)
    recettes = mycursor.fetchone()

    sql = "SELECT SUM(nb_participants) AS total_participants FROM activite;"
    mycursor.execute(sql)
    total_participants = mycursor.fetchone()

    sql = "SELECT * FROM localisation;"
    mycursor.execute(sql)
    localisation = mycursor.fetchall()

    return render_template('activite/show_activite.html',
                           activite=activite,
                           recettes=recettes,
                           total_participants=total_participants,
                           localisation=localisation)


@app.route('/activite/add', methods=['GET'])
def add_activite():
    mycursor = get_db().cursor()

    sql = "SELECT * FROM localisation ORDER BY id_localisation;"
    mycursor.execute(sql)
    localisation = mycursor.fetchall()

    return render_template('activite/add_activite.html', localisation=localisation)


@app.route('/activite/add', methods=['POST'])
def valid_add_activite():
    mycursor = get_db().cursor()

    nom_activite = request.form['nom_activite']
    date_creation = request.form['date_creation']
    cout_inscription = request.form['cout_inscription']
    type_activite = request.form['type_activite']
    nb_participants = request.form['nb_participants']
    localisation_id = request.form['localisation_id']
    image = request.form['image']
    tuple_insert = (nom_activite,
                    date_creation,
                    cout_inscription,
                    type_activite,
                    nb_participants,
                    localisation_id,
                    image)

    sql = "INSERT INTO activite(" \
          "nom_activite," \
          "date_creation," \
          "cout_inscription," \
          "type_activite," \
          "nb_participants," \
          "localisation_id," \
          "image" \
          ") VALUES (%s,%s,%s,%s,%s,%s,%s);"
    mycursor.execute(sql, tuple_insert)
    get_db().commit()

    print(u'activité ajoutée: '
          u'nom =', nom_activite,
          ', date de création =', date_creation,
          ', coût d\'inscription =', cout_inscription,
          ', type d\'activité =', type_activite,
          ', nombre de participants =', nb_participants,
          ', lieu =', localisation_id, ', image =', image)
    message = u'activité ajoutée: nom = ' + nom_activite + \
              ', date de création = ' + date_creation + \
              ', coût d\'inscription = ' + cout_inscription + \
              ', coût d\'inscription = ' + cout_inscription + \
              ', type d\'activité = ' + type_activite + \
              ', nombre de participants = ' + nb_participants + \
              ', lieu = ' + localisation_id + \
              ', image = ' + image
    flash(message, 'alert-danger')

    return redirect('/activite/show')


@app.route('/activite/delete', methods=['GET'])
def delete_activite():
    mycursor = get_db().cursor()

    id_activite = request.args.get('id', '')
    tuple_delete = (id_activite,)
    sql = "DELETE FROM activite WHERE id_activite = %s;"
    mycursor.execute(sql, tuple_delete)
    get_db().commit()

    print(u'activité supprimée: id =', id_activite)
    message = u'activité supprimée: id = ' + id_activite
    flash(message, 'alert-danger')

    return redirect('/activite/show')


@app.route('/activite/edit', methods=['GET'])
def edit_activite():
    mycursor = get_db().cursor()

    id_activite = request.args.get('id', '')
    sql = "SELECT * FROM activite WHERE id_activite=%s;"
    mycursor.execute(sql, (id_activite,))
    activite = mycursor.fetchone()
    sql = "SELECT * FROM localisation;"
    mycursor.execute(sql)
    localisation = mycursor.fetchall()

    return render_template('activite/edit_activite.html', activite=activite, localisation=localisation)


@app.route('/activite/edit', methods=['POST'])
def valid_edit_activite():
    mycursor = get_db().cursor()

    id_activite = request.form['id_activite']
    nom_activite = request.form['nom_activite']
    date_creation = request.form['date_creation']
    cout_inscription = request.form['cout_inscription']
    type_activite = request.form['type_activite']
    nb_participants = request.form['nb_participants']
    localisation_id = request.form['localisation_id']
    tuple_update = (nom_activite,
                    date_creation,
                    cout_inscription,
                    type_activite,
                    nb_participants,
                    localisation_id,
                    id_activite)

    sql = "UPDATE activite SET " \
          "nom_activite=%s," \
          "date_creation=%s," \
          "cout_inscription=%s," \
          "type_activite=%s," \
          "nb_participants=%s," \
          "localisation_id=%s " \
          "WHERE id_activite = %s;"
    mycursor.execute(sql, tuple_update)
    get_db().commit()

    print(u'Activité modifiée: '
          u'id =', id_activite,
          ', nom =', nom_activite,
          ', date de création =', date_creation,
          ', coût d\'inscription =', cout_inscription,
          ', type d\'activité =', type_activite,
          ', participants =', nb_participants,
          ', lieu =', localisation_id)
    message = u'Activité modifiée: ' \
              u'id = ' + id_activite + \
              ', nom = ' + nom_activite + \
              ', date de création = ' + date_creation + \
              ', coût d\'inscription = ' + cout_inscription + \
              ', type d\'activité = ' + type_activite + \
              ', participants = ' + nb_participants + \
              ', lieu = ' + localisation_id
    flash(message, 'alert-success')

    return redirect('/activite/show')


@app.route('/activite/toDelete', methods=['GET'])
def to_delete_activite():
    mycursor = get_db().cursor()

    id_activite = request.args.get('id', '')
    tuple_delete = (id_activite,)
    localisation_id = request.args.get('idLocalisation', '')

    sql = "DELETE FROM activite WHERE id_activite = %s;"
    mycursor.execute(sql, tuple_delete)
    get_db().commit()

    print(u'activité supprimée: id =', id_activite)
    message = u'activité supprimée: id = ' + id_activite
    flash(message, 'alert-danger')

    return redirect('/localisation/toDelete?id=' + localisation_id)


# ----- LOCALISATION ----- #

@app.route('/localisation/show')
def show_localisation():
    mycursor = get_db().cursor()

    sql = "SELECT id_localisation,nom_lieu,COUNT(id_activite) as NBR " \
          "FROM localisation " \
          "LEFT JOIN activite " \
          "ON localisation.id_localisation = activite.localisation_id " \
          "GROUP BY id_localisation;"
    mycursor.execute(sql)
    localisation = mycursor.fetchall()

    sql = "SELECT * FROM activite;"
    mycursor.execute(sql)
    activite = mycursor.fetchall()

    return render_template('localisation/show_localisation.html', localisation=localisation, activite=activite)


@app.route('/localisation/add', methods=['GET'])
def add_localisation():
    return render_template('localisation/add_localisation.html')


@app.route('/localisation/add', methods=['POST'])
def valid_add_localisation():
    mycursor = get_db().cursor()

    nom_lieu = request.form['nom_lieu']
    tuple_insert = nom_lieu

    sql = "INSERT INTO localisation (nom_lieu) VALUES (%s);"
    mycursor.execute(sql, tuple_insert)
    get_db().commit()

    print(u'localisation ajoutée: nom =', nom_lieu)
    message = u'localisation ajoutée: nom = ' + nom_lieu
    flash(message, 'alert-danger')

    return redirect('/localisation/show')


@app.route('/localisation/delete', methods=['GET'])
def delete_localisation():
    mycursor = get_db().cursor()

    id_localisation = request.args.get('id', '')
    tuple_delete = (id_localisation,)

    sql = "DELETE FROM localisation WHERE id_localisation = %s;"
    mycursor.execute(sql, tuple_delete)
    get_db().commit()

    print(u'localisation supprimée: id =', id_localisation)
    message = u'localisation supprimée: id = ' + id_localisation
    flash(message, 'alert-danger')

    return redirect('/localisation/show')


@app.route('/localisation/toDelete', methods=['GET'])
def to_delete_localisation():
    mycursor = get_db().cursor()

    id_localisation = request.args.get('id', '')
    tuple_delete = (id_localisation,)

    sql = "SELECT id_activite,nom_activite,date_creation,cout_inscription,type_activite,nb_participants " \
          "FROM activite " \
          "WHERE localisation_id = %s " \
          "ORDER BY id_activite;"
    mycursor.execute(sql, tuple_delete)
    activites = mycursor.fetchall()
    if len(activites) == 0:
        print(u'localisation supprimable: id =', id_localisation, 'est maintenant supprimable')
        message = u'localisation supprimable: id = ' + id_localisation + ' est maintenant supprimable'
        flash(message, 'alert-success')
        return redirect('/localisation/show')

    sql = "SELECT id_localisation,nom_lieu " \
          "FROM localisation " \
          "ORDER BY id_localisation;"
    mycursor.execute(sql)
    localisations = mycursor.fetchall()

    return render_template('activite/delete_activite.html',
                           activites=activites,
                           localisations=localisations,
                           id_localisation=id_localisation)


@app.route('/localisation/edit', methods=['GET'])
def edit_localisation():
    mycursor = get_db().cursor()

    id_localisation = request.args.get('id', '')

    sql = "SELECT * FROM localisation WHERE id_localisation=%s;"
    mycursor.execute(sql, (id_localisation,))
    localisation = mycursor.fetchone()

    return render_template('localisation/edit_localisation.html',
                           localisation=localisation,
                           id_localisation=id_localisation)


@app.route('/localisation/edit', methods=['POST'])
def valid_edit_localisation():
    mycursor = get_db().cursor()

    id_localisation = request.form['id_localisation']
    nom_lieu = request.form['nom_lieu']
    tuple_update = (nom_lieu, id_localisation)

    sql = "UPDATE localisation SET nom_lieu = %s WHERE id_localisation = %s;"
    mycursor.execute(sql, tuple_update)
    get_db().commit()

    print(u'localisation modifiée: id =', id_localisation, ', nom =', nom_lieu)
    message = u'localisation modifiée: id = ' + id_localisation + ', nom = ' + nom_lieu
    flash(message, 'alert-success')

    return redirect('/localisation/show')
