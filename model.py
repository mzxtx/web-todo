import app
from extension import db


# Create the module table
class Module(db.Model):
    __tablename__ = "module"
    Code = db.Column(db.String(10),primary_key=True,nullable=False)
    Title = db.Column(db.String(50),nullable=False)


# Create the assessment table
class Assessment(db.Model):
    __tablename__ = "assessment"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    #Module_Code = db.Column(db.String(10),nullable=False)
    Module_Code = db.Column(db.String(10),db.ForeignKey("module.Code"))
    #Module_Title = db.Column(db.String(50),nullable=False)
    Deadline = db.Column(db.Date,nullable=False)
    Assessment_Title = db.Column(db.String(50),nullable=False)
    Description = db.Column(db.String(20), nullable=True)
    Status = db.Column(db.String(10),nullable=False)

    Module = db.relationship("Module",backref="assessments")


# with app.app.app_context():
#     db.drop_all()
#     db.create_all()