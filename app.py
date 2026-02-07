import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__, template_folder="templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True  # auto reload templates

db = SQLAlchemy(app)

class Opportunity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    opportunity_type = db.Column(db.String(50), nullable=False)
    field = db.Column(db.String(100), nullable=False)
    institution = db.Column(db.String(150))
    description = db.Column(db.Text)
    link = db.Column(db.String(300), nullable=False)
    paid = db.Column(db.Boolean, default=False)
    location = db.Column(db.String(100))
    start_term = db.Column(db.String(50))
    deadline = db.Column(db.Date)
    active = db.Column(db.Boolean, default=True)
    archived = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.route("/")
def home():
    template_path = "templates/home.html"
    print("Template path:", os.path.abspath(template_path))
    print("Last modified:", os.path.getmtime(template_path))
    
    opportunities = Opportunity.query.order_by(Opportunity.created_at.desc()).all()
    return render_template("home.html", opportunities=opportunities)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, use_reloader=True)  # ensure Flask auto-reloader is on
