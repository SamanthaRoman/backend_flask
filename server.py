from flask import Flask
# opposit as java we say from then import. 
from config import me 
# this is how you import other files in your project
import json


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

# use app.run to run it and use the script in the terminal command: python3 filename
app.run(debug=True)