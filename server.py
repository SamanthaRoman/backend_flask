from flask import Flask, request
# add request to allow us to request data 
# opposit as java we say from then import. 
from config import me 
# this is how you import other files in your project
import json
from mock_data import catalog


# flask is a class thats why it is capital F
# this is how we use classes

app = Flask(__name__)


# the root page has no text after the slash
@app.get("/")
def index():
    return "Hello from Flask"

@app.get("/test")
def anything():
    return "This is another page"




#####################################################
###############        API        ###################
#####################################################


@app.get("/api/version")
def version():
    v = {
        "version": "1.0.0",
        "name": "Quartz"
    }
    return json.dumps(v)
# dumps variable converts everyting into json


# get /api/about 
# return the me dictionary as json 

@app.get("/api/about")
def about():
    return json.dumps(me)

# End point to allow the clients to request what is the store and then the store and products displayed in the catalog
@app.get('/api/catalog')
def get_catalog():
    return json.dumps(catalog)



# end point to allow the user to add products to their cart For this END POINT we must add request to the top import for flask. 
    # product is the variable we store it in only because we know its products. We choose the variable name. 
@app.post('/api/catalog')
def save_product():
    # this is reading the payload that we are calling product 
    product = request.get_json()

    product["_id"] = len(catalog)
    # len is a global function in python to show the length of objects or characters in a string. 
    catalog.append(product)

    return json.dumps(product)

# create a get /ai/report/total
# that sends total value of your catalong (sum of all prices)

@app.get('/api/report/total')
def report_total():
    total = 0
    for prod in catalog:
        # total = total + prod["price"] 
        # above line and below line are same lower one is just shorter 
        total += prod["price"]

    result = { # here we return the result but wrap it in a fancier way.
        "report": "total",
        "value": total
    }

    return json.dumps(result) # must return json dumps or it wont work


# get all products for a given category

@app.get("/api/product/<cat>")
# <cat> is a category variable 
# the cat is a variable you can call what ever you want but make sure to pass the same name below
def get_by_category(cat):
    results = []
    for prod in catalog:
        if prod["category"] == cat:
            results.append(prod)
    
    return json.dumps(results)


# use app.run to run it and use the script in the terminal command: python3 filename
app.run(debug=True)