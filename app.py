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
@app.route("/opportunities/<opp_type>")
def opportunities(opp_type=None):
    opportunities_list = read_opportunities(opp_type)
    return render_template("home.html", opportunities=opportunities_list, opp_type=opp_type)

@app.route("/internships/map")
def internship_map():
    # Only show internships from the sheet
    internships = read_opportunities("internship")
    return render_template("internships.html", opportunities=internships)

@app.route("/guides")
def guides():
    # Placeholder for career community guides page
    return render_template("guides.html")

@app.route("/landing")
def landing():
    return render_template("landing.html")


# ----------------------
# Run app
# ----------------------
if __name__ == "__main__":
    app.run(debug=True)
