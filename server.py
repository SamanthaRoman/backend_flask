from flask import Flask, request, abort
# add request to allow us to request data 
# opposit as java we say from then import. 
from config import me, db
# this is how you import other files in your project
import json
from mock_data import catalog, coupon_codes


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


def fix_id(record):
    record["_id"] = str(record["_id"])
    return record



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

# Read the database
@app.get('/api/catalog')
def get_catalog():
    #products is the colection. filter inside find empty means no filter
    # cursor is a dumbed down list. Only travel with for loop.
    cursor = db.products.find({})
    results = []

    for product in cursor:
        results.append(fix_id(product))

    return json.dumps(results)



# write into the database
@app.post('/api/catalog')
def save_product():
    # this is reading the payload that we are calling product 
    product = request.get_json()

    #this is saving to the database
    db.products.insert_one(product)

    return json.dumps(fix_id(product)) 

# create a get /ai/report/total
# that sends total value of your catalong (sum of all prices)

@app.get('/api/report/total')
def report_total():
    cursor = db.products.find({})
    total = 0
    for prod in cursor:
        # total = total + prod["price"] 
        # above line and below line are same lower one is just shorter 
        total += prod["price"]

    result = { # here we return the result but wrap it in a fancier way.
        "report": "total",
        "value": total
    }

    return json.dumps(result) # must return json dumps or it wont work


# get all products for a given category

@app.get("/api/products/<cat>")
# <cat> is a category variable 
# the cat is a variable you can call what ever you want but make sure to pass the same name below
# categories are scented and unscented and organic
def get_by_category(cat):
    cursor = db.products.find({ "category": cat }) #travel cursor/aka list 
    results = []                   #filter on database because its faster
    # for prod in cursor:
    #     # if prod["category"] == cat: # strict comparison
    #     #     fix_id(prod)
    #     #     results.append(prod)
    
    return json.dumps(results)


# get search simple variable can add variable <term>
@app.get("/api/products/search/<term>") # decorate your function - create any path you like
def product_search(term): #define your function and pass it the variable 
    results = []
    for prod in catalog:
        if term.lower() in prod['title'].lower(): # if term contains not case sensative by parsing both to lowers
            results.append(prod)

    return json.dumps(results)



# create an endpoint to get all the products with a price then a lower given number 100 or less
@app.get("/api/products/lower/<price>")
def products_lower(price):
    results = []
    real_price = float(price) # turn your number into a string.
    cursor = db.products.find({ 'price': {'$lte': real_price} })

    for prod in catalog:
        fix_id(prod)
        results.append(prod)

    return json.dumps(results)

# get price greater or equal
@app.get("/api/products/greater/<price>")
def products_greater(price):
    results = []
    real_price = float(price)
    cursor = db.products.find({'price': {'$lte': real_price}})

    for prod in cursor:
        fix_id(prod)
        results.append(prod)

    return json.dumps(results)




#####################################################
###########        Coupons        ###################
#####################################################



# get all coupons (get)
@app.get("/api/coupons")
def get_coupons():
    cursor = db.coupons.find({})
    results = []
    for coupon in cursor:
        fix_id(coupon)
        results.append(coupon)

    return json.dumps(results)


# save a coupon (post)
@app.post("/api/coupons")
def save_coupons():
    coupon = request.get_json()
    
    db.coupons.insert_one(coupon)
    fix_id(coupon)

    return json.dumps(coupon)

# get coupon and serach coupong with the code and return object/dictionary if exists
@app.get("/api/coupons/<code>")
def search_coupon(code):
    coupon = db.coupons.find_one({"code": {'$regex': f"^{code}$", '$options': "i"}})
    if not coupon:
        return abort(404, "Invalid Coupon Code") #return a not found 404 code 

    fix_id(coupon)
    return json.dumps(coupon)




# # use app.run to run it and use the script in the terminal command: python3 filename
# app.run(debug=True)