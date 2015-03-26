from flask import Blueprint, jsonify, request, render_template, flash, Response, redirect, url_for
from models.LolCat import LolCat, Comment, CommentReply
from math import ceil
import forms

lol_cat_blueprint = Blueprint('lolcat', __name__)
items_per_page = 4


@lol_cat_blueprint.route('/')
@lol_cat_blueprint.route('/lolcats/<int:page>')
def home(page=0):
    """
    Gets the home page. This has a list of lolats

    :param page: the page to return
    :return: The rendered view for the landing page
    """
    res = []
    start_index = page * items_per_page
    results = LolCat.objects.order_by("-created_at")[start_index:start_index + items_per_page]
    total = results.count(with_limit_and_skip=False)
    for lc in results:
        res.append(lc)
    return render_template("list.html", cats=res, total=total, page=page, pages=ceil(total/items_per_page))


@lol_cat_blueprint.route('/lolcat/<catid>')
def one(catid):
    """
    This is the detail view for a single lolcat
    :param catid:
    :return:
    """
    if(not catid):
        # this needs to return a 400 Bad Request
        pass

    puss = LolCat.objects.get_or_404(id=catid)
    commentForm = forms.CommentForm()
    replyForm = forms.CommentReplyForm()
    return render_template("detail.html", cat=puss, form=commentForm, replyForms=(replyForm, ))


@lol_cat_blueprint.route('/lolcat/<catid>/comments', methods=['POST'])
def save_comment(catid):
    """
    This adds a comment to a lolcat

    :param catid: the lolcat to add the comment to
    :return:should redirect back to the lolcat detail view
    """
    puss = LolCat.objects.get_or_404(id=catid)
    form = forms.CommentForm()
    if(not form.validate_on_submit()):
        flash("There were some problems validating that comment, you can try again...", "warning")
        replyForm = forms.CommentReplyForm()
        return render_template("detail.html", cat=puss, form=form, replyForms=(replyForm, ))

    comment = Comment(author=form.author.data, comment=form.comment.data, lolcat=puss.id)
    comment.save()
    puss.update(push__comments=comment)
    puss.save()
    flash("your lovely new comment has been added to {}".format(puss.title), "success")
    return redirect(url_for('.one', catid=catid), code=302)


@lol_cat_blueprint.route("/lolcat/<catid>/comment/<commentid>/replies", methods=['POST'])
def save_comment_reply(catid, commentid):
    """
    This will save a single comment reply
    :param catid: the id of the lolcat
    :param commentid: the comment to add the reply to
    :return: redirects back to the single lolcat page
    """
    form = forms.CommentReplyForm()
    if(not form.validate_on_submit()):
        flash("there was an error adding your comment reply - try again", "warning")
        cat = LolCat.objects.get_or_404(id=catid)
        form.comment_id = commentid
        emptyForm = forms.CommentReplyForm()
        emptyForm.author.data = ""
        emptyForm.comment.data = ""
        return render_template("detail.html", cat=cat, form=forms.CommentForm(), replyForms=(emptyForm, form))

    comment = Comment.objects.get_or_404(id=commentid)
    reply = CommentReply(author=form.author.data, comment=form.comment.data)
    comment.replies.append(reply)
    comment.save()
    flash("your new comment reply has been saved", "success")
    return redirect(url_for('.one', catid=catid), code=302)


@lol_cat_blueprint.route("/lolcat/new")
@lol_cat_blueprint.route('/lolcat/edit/<catid>')
def edit(catid=None):
    """
    This is view displays the form to add a new lolcat or edit an existing lolcat
    :param catid:the id of the cat to edit, or None if this is a new lolcat
    :return: the view that has the lolcat form
    """
    if(catid):
        puss = LolCat.objects.get_or_404(id=catid)
    else:
        puss = None
    form = forms.LolCatUploadForm(obj=puss)
    return render_template("create.html", form=form)


@lol_cat_blueprint.route('/lolcat/save', methods=['POST'])
def save_lolcat():
    """
    This is where lolcats get saved to our db

    :return:goes to the detail view of the lolcat
    """
    try:
        form = forms.LolCatUploadForm()
        if(not form.validate_on_submit()):
            flash("There were some problems validating that lolcat, you can try again...", "warning")
            return render_template("create.html", form=form)

        cat_id = form.id.data
        if(cat_id):
            #this is an edit so retrieve cat details from mongo
            flash_message ="Cat {} has been updated"
            cat = LolCat.objects.get_or_404(id=cat_id)
        else:
            #this is a new lolcat
            flash_message = "Cat {} has been created"
            cat = LolCat()

        cat.title   = form.title.data
        cat.blurb   = form.blurb.data
        cat.source  = form.source.data

        if(form.image_data.has_file()):
            if(cat.image_data):
                cat.image_data.delete() #we need to this first. otherwise the new one will not save

            file = form.image_data.data
            cat.image_data.new_file()
            cat.image_data.content_type = file.content_type
            cat.image_data.write(file.stream)
            cat.image_data.close()

        cat.save()
        flash(flash_message.format(cat.title), "success")
        return render_template("detail.html", cat=cat, form=forms.CommentForm(), replyForms=(forms.CommentReplyForm(),))
    except Exception as e:
        return render_template("error.html", err=e)


@lol_cat_blueprint.route('/lolcat/delete/<catid>')
def delete(catid):
    """
    This will permanentley delete a lolcat
    :param catid: the id of the lolcat to delete
    :return: redirects to home
    """
    cat = LolCat.objects.get_or_404(id=catid)
    cat.delete()
    flash("Cat {} has been deleted".format(cat.title), "success")
    return home()


@lol_cat_blueprint.route('/lolcat/image/<catid>')
def image_data(catid):
    """
    This gets the bytes that constitute the lolcat image
    :param catid: the cat id that you want to see
    :return:a byte[] stream
    """
    cat = LolCat.objects.get_or_404(id=catid)
    data = cat.image_data.read()
    ct = cat.image_data.content_type

    return Response(response=data, content_type=ct)