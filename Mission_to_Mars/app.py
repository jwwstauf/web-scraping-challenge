from flask import Flask, render_template, redirect, url_for
import pymongo
import WebScraping

app = Flask(__name__, template_folder='templates')

client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.mars_db
collection = db.mars

@app.route("/")
def index():
    mars = collection.find_one()
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scrape():
    WebScraping.scrape_all()
    return redirect('/', code = 302)


if __name__ == "__main__":
    app.run(debug=True)
