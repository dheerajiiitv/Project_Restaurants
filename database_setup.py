from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

from sqlalchemy import Column, ForeignKey ,Integer,String

import sys
Base = declarative_base()







class Restaurant(Base):

	__tablename__='restaurant'

	id=Column(Integer,primary_key=True)
	name=Column(String(80),nullable=False)	

class MenuItem(Base):
	__tablename__='menu_item'
	id=Column(Integer,primary_key=True)
	name=Column(String(80),nullable=False)
	price=Column(String(20),nullable=False)
	description=Column(String(100),nullable=True)
	course=Column(String(80),nullable=True)
	restaurant_id=Column(Integer,ForeignKey('restaurant.id'))	
	restaurant = relationship(Restaurant)

	
	
	@property
	def serialize(self):
		return {
		'name':self.name,
		'description':self.description,
		'id':self.id,
		'price':self.price,
		'course':self.course,
		}




engine=create_engine('sqlite:///restaurant.db')
Base.metadata.create_all(engine)