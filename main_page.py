from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurant.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()
#restaurant=session.query(Restaurant).all()
#menu_item=session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
app=Flask(__name__)

@app.route('/restaurants')
def showRestaurantNames():
	return "This will Show all Restaurants name"

@app.route('/restaurants/create/')
def editRestaurantName():
	return "This will Create Restaurant Name"


@app.route('/restaurants/edit/<int:restaurant_id>')
def editRestaurantName(restaurant_id):
	return "This will Edit Restaurant Name"


@app.route('/restaurants/delete/<int:restaurant_id>')
def deleteRestaurantName(restaurant_id):
	return "This will delete Restaurant Name"	


@app.route('/restaurants/menu-items/<int:restaurant_id>/')
def showMenuItem(restaurant_id):
	return "Show Menu of a restaurant"



@app.route('/restaurants/<int:restaurant_id>/create-menu-item/<int:menu_id>/')
def createMenuItem(restaurant_id,menu_id):
	return "Create  Menu Item here"



@app.route('/restaurants/<int:restaurant_id>/delete-menu-item/<int:menu_id>/')
def deleteMenuItem(restaurant_id,menu_id):
	return "Delete Menu Item here"


@app.route('/restaurants/<int:restaurant_id>/edit-menu-item/<int:menu_id>/')
def editMenuItem(restaurant_id,menu_id):
	return "edit Menu Item here"
				


if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0',port=8000)