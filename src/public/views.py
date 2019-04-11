"""
Logic for dashboard related routes
"""

from flask import Blueprint, render_template,jsonify
from .forms import LogUserForm, secti,masoform
from ..data.database import db
from ..data.models import LogUser,Data

blueprint = Blueprint('public', __name__)

@blueprint.route('/', methods=['GET'])
def index():
    return render_template('public/index.tmpl')


def wpjson():
    import os
    import random
    import json
    import urllib2
    from datetime import datetime
    os.environ['no_proxy'] = '*'
    r= urllib2.urlopen('http://127.0.0.1:5001/data.json')
    data=json.load(r)
    cas=datetime.fromtimestamp(float(data["data"]["cas"]))
    i=Data(typ=data["data"]["nadpis"],
           hodnota=float(data["data"]["CPU"]),
           cas=cas)
    db.session.add(i)
    db.session.commit()
    return data

@blueprint.route('/json')
def jsex():
    data=Data.poslednich10minut()
    return render_template("public/mojedata.tmpl",data=data)

@blueprint.route('/loguserinput',methods=['GET', 'POST'])
def InsertLogUser():
    form = LogUserForm()
    if form.validate_on_submit():
        LogUser.create(**form.data)
    return render_template("public/LogUser.tmpl", form=form)

@blueprint.route('/loguserlist',methods=['GET'])
def ListuserLog():
    pole = db.session.query(LogUser).all()
    return render_template("public/listuser.tmpl",data = pole)

@blueprint.route('/secti', methods=['GET','POST'])
def scitani():
    form = secti()
    if form.validate_on_submit():
        return render_template('public/vystup.tmpl',hod1=form.hodnota1.data,hod2=form.hodnota2.data,suma=form.hodnota1.data+form.hodnota2.data)
    return render_template('public/secti.tmpl', form=form)

@blueprint.route('/maso', methods=['GET','POST'])
def masof():
    form = masoform()
    if form.validate_on_submit():
        return render_template('public/masovystup.tmpl',hod1=form.hodnota1.data,hod2=form.hodnota2.data,suma=form.hodnota1.data+form.hodnota2.data)
    return render_template('public/maso.tmpl', form=form)
