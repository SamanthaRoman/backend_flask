import pymongo
import certifi

# below is a dictionary 
me = {
    "first_name": "Samantha",
    "last_name": "Roman",
    "email": "samantharaeroman@gmail.com",
    "github_url": "https://github.com/SamanthaRoman"
}

con_str = "mongodb+srv://fsdi:test123@cluster0.ohuujef.mongodb.net/?retryWrites=true&w=majority"


client = pymongo.MongoClient(con_str, tlsCAFile=certifi.where())
db = client.get_database("store") #db variable storing our database at