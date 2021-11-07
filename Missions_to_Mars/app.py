from pprint import pprint
from flask import Flask
from flask.templating import render_template
from pymongo import MongoClient
from werkzeug.utils import redirect
import scrape_mars
from pprint import pprint

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017')
mars = client.mars_db.mars

mars.drop()

@app.route('/')
def home():
    mars_data = mars.find_one()
    print("HOME")
    return render_template("index.html", data = mars_data)

@app.route('/scrape')
def scrape():
    item = scrape_mars.scrape()
    print('*_*_*_*_*_*_*_*_*_*_*_*_*')
    pprint(item)
    print('*_*_*_*_*_*_*_*_*_*_*_*_*')
    mars.insert_one(item)

    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)