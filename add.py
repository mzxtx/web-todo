from flask import Blueprint, request, render_template, url_for, redirect, flash
import wtforms
from wtforms.validators import length, data_required, regexp
from model import Module, Assessment
from extension import db
from sqlalchemy import or_

bp = Blueprint("add", __name__, url_prefix="/")


# Verifying assessment Information
class Add_Assessment(wtforms.Form):
    Module_Code = wtforms.StringField(validators=[length(min=1, max=10)])
    Assessment_Title = wtforms.StringField(validators=[length(min=1, max=50)])
    Description = wtforms.StringField(validators=[length(max=200)])
    Deadline = wtforms.DateField(validators=[data_required()])
    Status = wtforms.StringField(validators=[data_required(),regexp('To-do|Completed',0,'Invalid status')])

    def validate_assessment(self, field):
        assessment_title = field.data
        assessment = Assessment.query.filter_by(assessment_title=assessment_title).first()
        if assessment:
            raise wtforms.ValidationError("The assessment already exists!")


# Verifying module Information
class Add_Module(wtforms.Form):
    Code = wtforms.StringField(validators=[length(min=1, max=10)])
    Title = wtforms.StringField(validators=[length(min=1, max=50)])

    def validate_code(self, field):
        code = field.data
        module = Module.query.filter_by(code=code).first()
        if module:
            raise wtforms.ValidationError("The module already exists!")


# Receive data from the add module and store it in the database
@bp.route('/add_module', methods=['GET', 'POST'])
def add_module():
    if request.method == "GET":
        return render_template("add_module.html")
    else:
        form = Add_Module(request.form)
        if form.validate():
            code = form.Code.data
            title = form.Title.data

            module = Module(Code=code, Title=title)
            db.session.add(module)
            db.session.commit()
            return redirect("/")
        else:
            flash("Incorrect code or title length. Please re-enter.")
            return redirect("/add_module")


#Add data to the assessment table
@bp.route('/add_assessment', methods=['GET', 'POST'])
def add_assessment():
    if request.method == 'GET':
        return render_template("add_assessment.html")
    else:
        form = Add_Assessment(request.form)
        if form.validate():
            module_code = form.Module_Code.data
            deadline = form.Deadline.data
            assessment_title = form.Assessment_Title.data
            description = form.Description.data
            status = form.Status.data

            assessment = Assessment(Module_Code=module_code, Deadline=deadline, Assessment_Title=assessment_title,
                                    Description=description, Status=status)
            db.session.add(assessment)
            db.session.commit()
            return redirect("/")
        else:
            flash("The information is incorrect.Please try again.")
            return redirect(url_for("add.add_assessment"))


#List the table data on the home page
@bp.route('/')
def index():
    #Sort by deadline
    assessments = Assessment.query.order_by(db.text("-Deadline")).all()
    modules = Module.query.all()
    return render_template("index.html", assessments=assessments, modules=modules)


# The search view
@bp.route('/search')
def search():
    query = request.args.get("query")
    assessments = Assessment.query.filter(or_(Assessment.Assessment_Title.contains(query),
                                              Assessment.Description.contains(query),
                                              Assessment.Module_Code.contains(query),
                                              Assessment.Status.contains(query),
                                              Assessment.Deadline.contains(query),))

    modules = Module.query.all()
    return render_template("index.html", assessments=assessments,modules=modules)


#change the status
@bp.route("/status/<int:id>")
def status(id):
    assessment = Assessment.query.filter_by(id=id)[0]
    if assessment.Status == "To-do":
        assessment.Status = "Completed"
    else:
        assessment.Status = "To-do"
    db.session.commit()
    return redirect("/")


