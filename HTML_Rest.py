from flask import Flask
from flask import render_template
from flask import request, redirect
from flask import g
import sqlite3
import os
import glob

app = Flask(__name__)
app.config["IMAGE_UPLOADS"] = "C:\\Users\\rasha\\Desktop\\Job\\FDM_Challenge_Fall_2021\\static\\assets\\stored_images"

@app.before_request
def before_request():
    g.db = sqlite3.connect("FDMdatabase.db")

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/private')
def private():
    return render_template('private.html')

# method that handles POST operations to the database
@app.route('/submit.html', methods = ['POST'])
def submit():
    # get all the form submissions
    title = request.form['title']
    price = request.form['price']
    category = request.form['category']
    condition = request.form['condition']
    location = request.form['location']
    description = request.form['subject']
    email = request.form['email']
    phone = request.form['phone']

    # set the form submissions into the database
    g.db.execute("INSERT INTO Products(title,price,category,condition,location,description,email,phone) values(?,?,?,?,?,?,?,?)", 
            [title,
            price,
            category,
            condition,
            location,
            description,
            email,
            phone])
    g.db.commit()

    # get the rowid of the recently submitted data
    filename=g.db.execute("SELECT rowid FROM Products WHERE Products.title = ?",[title]).fetchone()

    # get and save the image
    image = request.files['item_image']
    file = str(filename[0]) + ".png"
    image.save(os.path.join(app.config["IMAGE_UPLOADS"], file))
    return redirect('/')

# methods that handle the GET operations from the database
@app.route('/shop.html')
def shop():
    # retrieve title from database and format
    title = g.db.execute("SELECT title FROM Products").fetchall()
    titles = []
    for t in title:
        titles.append(t[0])
    
    # retrieve price from database and format
    price = g.db.execute("SELECT price FROM Products").fetchall()
    prices = []
    for t in price:
        prices.append(t[0])
    
    # retrieve location from database and format
    location = g.db.execute("SELECT location FROM Products").fetchall()
    locations = []
    for t in location:
        locations.append(t[0])

    # retrieve description from database and format
    description = g.db.execute("SELECT description FROM Products").fetchall()
    descs = []
    for t in description:
        descs.append(t[0])

    # retrieve email from database and format
    email = g.db.execute("SELECT email FROM Products").fetchall()
    emails = []
    for t in email:
        emails.append(t[0])

    # retrieve the images stored locally
    images = glob.glob(app.config["IMAGE_UPLOADS"] + '**/*.png', recursive=True)
    files = []
    for i in images:
        files.append("assets/stored_images/" + i[79:])

    # create an array of arrays that stores all the important information
    height = len(titles)
    products = [[] for y in range(height)]
    for i in range(height):
        products[i].append(titles[i])
        products[i].append(locations[i])
        products[i].append(prices[i])    
        products[i].append(descs[i])
        products[i].append(emails[i])
        products[i].append(files[i])

    # display the shop page with all of the information from the database
    return render_template('shop.html', products = products)

if __name__ == '__main__':
	app.run(debug=True)