from flask import Flask, render_template
from leetcode_scraper import fetch_full_leetcode_overview

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

#  NEW: LEETCODE PAGE
@app.route("/leetcode")
def leetcode():
    data = fetch_full_leetcode_overview()   # function from scraper
    return render_template("leetcode.html", data=data)

@app.route('/projects')
def projects():
    return render_template('project.html')

@app.route("/skills")
def skills():
    return render_template("skills.html")

@app.route("/about")
def about():
    return render_template("aboutme.html")

@app.route("/achievements")
def achievements():
    return render_template("achievements.html")

@app.route("/certificates")
def certificates():
    return render_template("certificates.html")





if __name__ == "__main__":
    app.run(debug=True)
