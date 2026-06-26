import os
from flask import Flask, render_template
import pandas as pd
from datetime import datetime

app = Flask(__name__, template_folder="templates")
app.config['TEMPLATES_AUTO_RELOAD'] = True  # auto reload templates

GOOGLE_SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQRB7nVD_m8mvJtWIVVRSz_BTePnq57xT6NcJxtDGsTYo-Rv_iFRhRr7WAUrxsaeEZp5_czOXxvXUd1/pub?output=csv"
EVENTS_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTQy57qnx2UuJkcKJ50h5E3sZKBCEc0n5CQNvRwFRp6wIAY9XskwAcXfE-VFVvG9kZpVRu09raHeWXn/pub?output=csv"

# ----------------------
# Helper function to read opportunities
# ----------------------
def read_opportunities(opp_type=None):
    df = pd.read_csv(GOOGLE_SHEET_CSV_URL)
    if opp_type:
        df = df[df['opportunity_type'].str.lower() == opp_type.lower()]
    return df.to_dict(orient="records")

# ----------------------
# Routes
# ----------------------
@app.route("/")
def root():
    try:
        df = pd.read_csv(EVENTS_SHEET_URL)

        # Convert expiration column to datetime
        df['expiration_date'] = pd.to_datetime(df['expiration_date'], errors='coerce')

        today = datetime.today()

        # Keep only non-expired events
        df = df[df['expiration_date'] >= today]

        events = df.to_dict(orient="records")

    except:
        events = []

    return render_template("landing.html", events=events)

@app.route("/opportunities")
@app.route("/opportunities/landing")
def opportunities_landing():
    return render_template("opportunities_landing.html")

@app.route("/opportunities/research")
def faculty_research():
    return render_template("faculty_research.html")

@app.route("/opportunities/student")
def jobs():
    return render_template("student.html")

@app.route("/opportunities/beyond")
def internships():
    return render_template("beyond.html")

@app.route("/opportunities/getinvolved")
def off_campus():
    return render_template("getinvolved.html")

@app.route("/internships")
@app.route("/internships/landing")
def internship_landing():
    return render_template("internship_landing.html")
@app.route("/internships/map")
def internship_map():
    # Only show internships from the sheet
    internships = read_opportunities("internship")
    return render_template("internships.html", opportunities=internships)

@app.route("/guides")
def guides():
    # Placeholder for career community guides page
    return render_template("guides.html")
@app.route("/guides/research101")
def research101():
    return render_template("research101.html")
@app.route("/guides/access")
def accessvisibility():
    return render_template("access.html")


@app.route("/landing")
def landing():
    return render_template("landing.html")


# ----------------------
# Run app
# ----------------------
if __name__ == "__main__":
    app.run(debug=False)