from flask import Blueprint, jsonify, request, render_template, flash, Response
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
@lolcatbp.route('/lolcat/edit/<catid>')
def edit(catid=0):
    if(catid != 0):
        puss = LolCat.objects.get_or_404(id=catid)
    else:
        puss = None
    return render_template("/create.html", cat=puss)

@lolcatbp.route('/lolcat/save', methods=['POST'])
def create():
    #try:
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

        file = request.files['image']
        if(file):
            cat.image_data.content_type = file.content_type
            cat.image_data.new_file()
            cat.image_data.write(file.stream)
            cat.image_data.close()

        cat.save()
        flash(flash_message.format(cat.title), "success")
        return render_template("detail.html", cat=cat)
    #except Exception as e:
    #    return render_template("error.html", err=e)

@lolcatbp.route('/lolcat/delete/<catid>')
def delete(catid):
    cat = LolCat.objects.get_or_404(id=catid)
    cat.delete()
    flash("Cat {} has been deleted".format(cat.title))
    return home()


@lolcatbp.route('/lolcat/image/<catid>')
def image_data(catid):
    cat = LolCat.objects.get_or_404(id=catid)
    data = cat.image_data.read()
    ct = cat.image_data.content_type

    return Response(response=data, content_type=ct)