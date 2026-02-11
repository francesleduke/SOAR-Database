import os
from flask import Flask, render_template
import pandas as pd
from datetime import datetime

# ----------------------
# Flask setup
# ----------------------
app = Flask(__name__, template_folder="templates")
app.config['TEMPLATES_AUTO_RELOAD'] = True  # auto reload templates

# ----------------------
# CSV reading function
# ----------------------
def read_opportunities():
    if not os.path.exists("opportunities.csv"):
        return []
    
    df = pd.read_csv("opportunities.csv")
    # convert deadline column to date
    if 'deadline' in df.columns:
        df['deadline'] = pd.to_datetime(df['deadline'], errors='coerce').dt.date
    # ensure 'paid' is boolean
    if 'paid' in df.columns:
        df['paid'] = df['paid'].astype(bool)
    return df.to_dict(orient="records")

# ----------------------
# Routes
# ----------------------
@app.route("/")
def root():
    # redirect to landing page
    return render_template("landing.html")

@app.route("/opportunities")
def all_opportunities():
    opportunities = read_opportunities()
    return render_template("home.html", opportunities=opportunities)

@app.route("/opportunities/<opp_type>")
def opportunities_by_type(opp_type):
    opp_type = opp_type.lower()
    if opp_type not in ["internship", "job", "research"]:
        return "Invalid opportunity type", 404

    opportunities = read_opportunities()
    filtered = [opp for opp in opportunities if opp['opportunity_type'].lower() == opp_type]
    return render_template("home.html", opportunities=filtered, opp_type=opp_type)

@app.route("/internships/map")
def internship_map():
    return render_template("internships.html")

# ----------------------
# Run app
# ----------------------
if __name__ == "__main__":
    app.run(debug=True)
