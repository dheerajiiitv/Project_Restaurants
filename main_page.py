from flask import Flask,render_template,url_for,request,redirect,jsonify
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
@app.route('/')
@app.route('/restaurants')
def showRestaurantNames():
	restaurants=session.query(Restaurant).all()
	return render_template("restaurants.html",restaurants=restaurants)

@app.route('/restaurants/create/',methods=['POST','GET'])
def createRestaurantName():
	if request.method == 'POST':
		if request.form['rest_name']:
			new_rest=Restaurant(name=request.form['rest_name'])
			session.add(new_rest)
			session.commit()
			return redirect(url_for('showRestaurantNames'))
		else:
			return "please Input name"	
	else:
		return render_template("newrestaurants.html")


@app.route('/restaurants/edit/<int:restaurant_id>',methods=['POST','GET'])
def editRestaurantName(restaurant_id):
	restaurants=session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'POST':
		if request.form['edit_rest_name']:
			restaurants.name=request.form['edit_rest_name']
			session.add(restaurants)
			session.commit()
			return redirect(url_for('showRestaurantNames'))
		else:
			return "Please Input name"	
	else:
		return render_template("editrestaurant.html",restaurants=restaurants)


@app.route('/restaurants/delete/<int:restaurant_id>',methods=['POST','GET'])
def deleteRestaurantName(restaurant_id):
	if request.method == 'POST':
		rest=session.query(Restaurant).filter_by(id=restaurant_id).one()
		session.delete(rest)
		session.commit()
		return redirect(url_for('showRestaurantNames'))
	else:	
		return render_template("deleterestaurant.html",restaurant_id=restaurant_id)


@app.route('/restaurants/<int:restaurant_id>/menu/')
def showMenuItem(restaurant_id):
	restaurants=session.query(Restaurant).filter_by(id=restaurant_id).one()
	items=session.query(MenuItem).filter_by(restaurant_id=restaurants.id)
	return render_template("menu.html",restaurants=restaurants,items=items)

@app.route('/restaurants/<int:restaurant_id>/menu/create/',methods=['POST','GET'])
def createMenuItem(restaurant_id):
	restaurant=session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'POST':
		newItem = MenuItem(name=request.form['name'], description=request.form['description'], price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)
		session.add(newItem)
		session.commit()
		return redirect(url_for('showMenuItem', restaurant_id=restaurant_id))
	else:
		return render_template("newmenuitem.html",restaurant=restaurant)   


	 
@app.route('/restaurants/<int:restaurant_id>/menu/edit/<int:menu_id>/',methods=['POST','GET'])
def editMenuItem(restaurant_id,menu_id):
	restaurant=session.query(Restaurant).filter_by(id=restaurant_id).one()
	editedItem=session.query(MenuItem).filter_by(id=menu_id).one()
	if restaurant_id == editedItem.restaurant_id:
		if request.method == 'POST':
			if request.form['name'] and request.form['price'] and request.form['description'] and request.form['course'] :
				editedItem.name = request.form['name']
				editedItem.price = request.form['price']
				editedItem.description = request.form['description']
				editedItem.course = request.form['course']
				session.add(editedItem)
				session.commit()
				return redirect(url_for('showMenuItem', restaurant_id=restaurant_id))
			else:
				return "Please give all input"	


		else:	
			return render_template("editmenuitem.html",restaurant=restaurant,item=editedItem) 

	else:
		return "Item is not available for this particular restaurant"
	


@app.route('/restaurants/<int:restaurant_id>/menu/delete/<int:menu_id>/',methods=['POST','GET'])
def deleteMenuItem(restaurant_id,menu_id):
	if request.method == 'POST':
		deleteItem=session.query(MenuItem).filter_by(id=menu_id).one()
		session.delete(deleteItem)
		session.commit()
		return redirect(url_for('showMenuItem', restaurant_id=restaurant_id))
	else:    
		return render_template("deletemenuitem.html",restaurant_id=restaurant_id,menu_id=menu_id)

@app.route('/restaurants/<int:restaurant_id>/menu/JSON/')
def restaurantMenuJSON(restaurant_id):
	
	Menu=session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
	try:
		for i in Menu:
			for r in Menu:
					return jsonify(MenuItems=[i.serialize for i in Menu])
	except:
		return "No Menu item"	    		
if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0',port=8000)