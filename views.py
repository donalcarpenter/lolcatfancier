from flask import Blueprint, jsonify, request, render_template, flash
from models.LolCat import LolCat

lolcatbp = Blueprint('lolcat', __name__)

@lolcatbp.route('/')
def home():
    res = []
    for lc in LolCat.objects:
        res.append(lc)
    return render_template("list.html", cats=res)

@lolcatbp.route('/lolcat/<catid>')
def one(catid):
    puss = LolCat.objects.get_or_404(id=catid)
    return render_template("detail.html", cat=puss)

@lolcatbp.route("/lolcat/new")
def create_form():
    return render_template("/create.html", cat=None)

@lolcatbp.route('/lolcat/edit/<catid>')
def edit(catid):
    puss = LolCat.objects.get_or_404(id=catid)
    return render_template("/create.html", cat=puss)

@lolcatbp.route('/lolcat/save', methods=['POST'])
def create():
    cat_id = request.form.get('id')
    if(cat_id):
        #this is an edit so retrieve cat details from mongo
        flash_message ="Cat {} has been updated"
        cat = LolCat.objects.get_or_404(id=cat_id)
    else:
        #this is a new lolcat
        flash_message = "Cat {} has been created"
        cat = LolCat()
    cat.title = request.form.get('title')
    cat.blurb = request.form.get('blurb')
    cat.source = request.form.get('source')
    cat.image = request.form.get('image')
    cat.save()
    flash(flash_message.format(cat.title), "success")
    return render_template("detail.html", cat=cat)


