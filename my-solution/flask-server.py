from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem 
app = Flask(__name__)


engine = create_engine("sqlite:///restaurantmenu.db")
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
@app.route('/welcome/')
def welcome():
    output = "<h1>Welcome to the Yummy Restaurants!</h1><br>"
    restaurants = session.query(Restaurant).all()
    for restaurant in restaurants:
        output += "<a href='/restaurants/{}'>{}</a>".format(restaurant.id, restaurant.name)
        output += "<br>"
    return output

@app.route('/restaurants/<int:restaurant_id>/')
def restaurants(restaurant_id):
    output = ""
    items = session.query(MenuItem).filter(MenuItem.restaurant_id == restaurant_id).all()
    for item in items:
        output += item.name
        output += "<br>"
        output += item.price
        output += "<br>"
        output += item.description
        output += "<br><br>"
    return output

if __name__ == '__main__':
    app_debug = True
    app.run(host='0.0.0.0', port=8080)