from flask import Flask,render_template
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
	restaurants=session.query(Restaurant).all()
	return render_template("restaurants.html",restaurants=restaurants)

@app.route('/restaurants/create/')
def createRestaurantName():
	return render_template("newrestaurants.html")


@app.route('/restaurants/edit/<int:restaurant_id>')
def editRestaurantName(restaurant_id):
	restaurants=session.query(Restaurant).filter_by(id=restaurant_id).one()
	return render_template("editrestaurant.html",restaurants=restaurants)


@app.route('/restaurants/delete/<int:restaurant_id>')
def deleteRestaurantName(restaurant_id):
	return render_template("deleterestaurant.html")


@app.route('/restaurants/<int:restaurant_id>/menu/')
def showMenuItem(restaurant_id):
	restaurants=session.query(Restaurant).filter_by(id=restaurant_id).one()
	items=session.query(MenuItem).filter_by(restaurant_id=restaurants.id)
	return render_template("menu.html",restaurants=restaurants,items=items)



@app.route('/restaurants/<int:restaurant_id>/menu/create/<int:menu_id>/')
def createMenuItem(restaurant_id,menu_id):
	return render_template("newmenuitem.html")



@app.route('/restaurants/<int:restaurant_id>/menu/delete/<int:menu_id>/')
def deleteMenuItem(restaurant_id,menu_id):
	return render_template("editmenuitem.html")


@app.route('/restaurants/<int:restaurant_id>/menu/edit/<int:menu_id>/')
def editMenuItem(restaurant_id,menu_id):
	return render_template("deletemenuitem.html")
				


if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0',port=8000)