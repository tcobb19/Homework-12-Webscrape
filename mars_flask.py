from flask import Flask, render_template, redirect
from scrape_mars import scrape

import pymongo

app = Flask(__name__)

# setup mongo connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
# connect to mongo db and collection
db = client.mars
collection = db.data

db.collection.drop()
    
mars_dict = scrape()

db.collection.insert_one(mars_dict)

@app.route("/scrape")
def page():
    #clear existing data, if any
    db.collection.drop()
    
    mars_dict = scrape()
    db.collection.update({}, mars_data,upsert=True)
    return redirect('/', code=302)
    
@app.route("/")
def index():
    mars_db = dict(db.collection.find_one())
    
    return render_template('index.html', mars = mars_db, )
    print(mars_db)
if __name__ == "__main__":
    app.run(debug=True)