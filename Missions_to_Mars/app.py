from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
from pymongo import MongoClient
import pymongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client.mars_db
col = db.mars_col

#Scrape route that calls the scrape function and stores the data into the MongoDB
@app.route("/scrape")
def scrape():   

    #Calling the function and storing the result in a variable
    data = scrape_mars.scrape()

    #Updating the scrapped data to the db
    col.update({}, data, upsert=True)

    #Redirecting the to the homepage
    return redirect("/")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    try:
        mars_data = col.find_one()
    except:
        print("No database found")

    # Return template and data
    #return render_template("index.html", mars=mars_data)
    return render_template('index.html', mars=mars_data)

if __name__ == "__main__":
    app.run(debug=True)


