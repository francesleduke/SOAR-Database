# ======================
# Import necessary libaries and initialize Flask app
# ======================

import os # interact with the operating system, e.g. file paths, last modified times, etc.
from flask import Flask, render_template # import Flask and tools: Flask is the main web framework class
                                         # render_template renders HTML templates 
from flask_sqlalchemy import SQLAlchemy  # import SQLAlchemy, a library to manage databases in Python with with ORM (object relational mapping)
                                         # lets you interact with a database using Python classes instead of raw SQL
from datetime import datetime # imports classes to work with dates and times
from datetime import date  # imports classes to work with dates and times
from flask import redirect # redirect sends user from one URL to another (e.g. landing page to opportunities page)

# ======================
# Flask app and database setup
# ======================

app = Flask(__name__, template_folder="templates") # _name_ tells Flask where the app is located 
                                                   # template_folder = "templates" tells Flask to look for HTML templates in the templates/ folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db' # tells SQLAlchemy where the database is 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # turns off a feature that tracks changes in SQLAlchemy objects to reduce warnings and memory use
app.config['TEMPLATES_AUTO_RELOAD'] = True # tells Flask to automatically reload templates when they change 

db = SQLAlchemy(app) # Creates the db object 

# ======================
# Database model for opportunities
# ======================

class Opportunity(db.Model): # define Opportunity table in the database 
    id = db.Column(db.Integer, primary_key=True) # unique number for each opportunity
    title = db.Column(db.String(200), nullable=False) # name of the opportunity
    opportunity_type = db.Column(db.String(50), nullable=False) # internship, job, or research
    field = db.Column(db.String(100), nullable=False) # subject area (biology, comp sci, etc.)
    institution = db.Column(db.String(150)) # company or school offering the opportunity
    description = db.Column(db.Text) # long text description 
    link = db.Column(db.String(300), nullable=False) # link to more info about the opportunity
    paid = db.Column(db.Boolean, default=False) # is it paid or not 
    location = db.Column(db.String(100)) # physical location or remote
    start_term = db.Column(db.String(50)) # when it starts
    deadline = db.Column(db.Date) # application deadline
    active = db.Column(db.Boolean, default=True) # whether it's currently active 
    archived = db.Column(db.Boolean, default=False) # whether it's archived
    created_at = db.Column(db.DateTime, default=datetime.utcnow) # timestamp for when the opportunity was added to the database

# ======================
# Views for the web app 
# ======================

# Only run this once to add example data
with app.app_context(): # SQLAlchemy operations need the Flask app context to know which app/database you are talking about
    # Check if the table is empty, if yes, seed some example opportunities
    if Opportunity.query.count() == 0:
        example_opps = [
            Opportunity(
                title="Summer Research Internship",
                opportunity_type="Internship",
                field="Biology",
                institution="State University",
                description="A 10-week research internship in molecular biology.",
                link="https://example.com/biology-internship",
                paid=True,
                location="Denver, CO",
                start_term="Summer 2026",
                deadline=date(2026, 4, 15)
            ),
            Opportunity(
                title="Data Science Job",
                opportunity_type="Job",
                field="Computer Science",
                institution="TechCorp",
                description="Entry-level data analyst position focusing on Python and SQL.",
                link="https://example.com/data-job",
                paid=True,
                location="Remote",
                start_term="Immediate",
                deadline=date(2026, 3, 1)
            ),
            Opportunity(
                title="Marine Biology Research",
                opportunity_type="Research",
                field="Environmental Science",
                institution="Oceanic Institute",
                description="Assist with field research on coastal ecosystems.",
                link="https://example.com/marine-research",
                paid=False,
                location="Bar Harbor, ME",
                start_term="Fall 2026",
                deadline=date(2026, 8, 31)
            ),
        ]

        # Add to the database
        db.session.add_all(example_opps) # adds the list of example opportunities to the database session
        db.session.commit() # saves changes to the database 
        print("Seeded example opportunities!")
    else:
        print("Opportunities already exist, skipping seeding.")

# ======================
# Flask routes 
# ======================

@app.route("/") # root URL of the website, redirects user to the landing page
def root():
    return redirect("/landing")


@app.route("/landing") # renders the landing page template 
def landing():
    return render_template("landing.html")

@app.route("/opportunities/<opp_type>") # dynamic route that takes in the type of opportunity
def opportunities_by_type(opp_type):
    # make sure type is valid
    if opp_type not in ["internship", "job", "research"]:
        return "Invalid opportunity type", 404
    
    opportunities = Opportunity.query.filter_by(opportunity_type=opp_type).order_by(Opportunity.created_at.desc()).all()
    return render_template("home.html", opportunities=opportunities, opp_type=opp_type)



if __name__ == "__main__": # ensures the code only runs when you start python app.py (in Terminal) and not when you import the file into another Python script 
    with app.app_context():
        db.create_all() # creates the database and tables if they don't already exist
    app.run(debug=True, use_reloader=True)  # run the Flask server, shows errors in the browser and reloads automatically when code changes 
