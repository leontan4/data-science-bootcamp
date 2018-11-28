from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_data = mongo.db.data.find_one()

    # Return template and data
    return render_template("index.html", mars_testing=mars_data)


@app.route("/scrape")
def scraper():
    mars_data = mongo.db.data
    data_data = scrape_mars.scrape()
    mars_data.update({}, data_data, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
