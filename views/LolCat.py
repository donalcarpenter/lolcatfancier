from flask import Blueprint, jsonify, request, render_template, flash
from models.LolCat import LolCat

lcb = Blueprint('lolcat', __name__)

@lcb.route('/')
def home():
    res = {}
    for lc in LolCat.objects:
        res[lc.id] = lc
    return render_template("list.html", cats=res)

@lcb.route('/lolcat/<catid>')
def one(catid):
    puss = LolCat.objects.get_or_404(id=catid)
    return render_template("detail.html", cat=[puss])

@lcb.route("/lolcat/new")
def create_form():
    return render_template("/create.html")

@lcb.route('/lolcat/edit/<catid>')
def edit(catid):
    puss = LolCat.objects.get_or_404(id=catid)
    return render_template("/create.html", cat=puss)

@lcb.route('/lolcat/edit/<catid>', methods=['POST', 'PUT'])
def save_edit(catid):
    cat = LolCat.objects.get_or_404(id=catid)
    cat.title = request.form.get('title')
    cat.blurb = request.form.get('blurb')
    cat.source = request.form.get('source')
    cat.image = request.form.get('image')
    cat.save()

    flash("Cat {} has been updated".format(cat.title), "success")

    return render_template("detail.html", cat=cat)

@lcb.route('/', methods=['POST'])
def create():
    cat = LolCat()
    cat.title = request.form.get('title')
    cat.blurb = request.form.get('blurb')
    cat.source = request.form.get('source')
    cat.image = request.form.get('image')
    cat.save()
    flash("Cat {} has been created".format(cat.title), "success")
    return render_template("detail.html", cat=cat)


