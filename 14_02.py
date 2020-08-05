from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, Numeric, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///cookies.db')

Session = sessionmaker(bind=engine)

Base = declarative_base()


"""
CREATE TABLE cookies (
	cookie_id INTEGER NOT NULL,
	cookie_name VARCHAR(50),
	cookie_recipe_url VARCHAR(255),
	cookie_sku VARCHAR(55),
	quantity INTEGER,
	unit_cost NUMERIC(12, 2),
	PRIMARY KEY (cookie_id)
)

CREATE TABLE ingredients (
	ingredient_id INTEGER NOT NULL,
	name VARCHAR(255),
	PRIMARY KEY (ingredient_id)
)

CREATE TABLE cookieingredients (
	cookie_id INTEGER NOT NULL,
	ingredient_id INTEGER NOT NULL,
	PRIMARY KEY (cookie_id, ingredient_id),
	FOREIGN KEY(cookie_id) REFERENCES cookies (cookie_id),
	FOREIGN KEY(ingredient_id) REFERENCES ingredients (ingredient_id)
)

"""
cookieingredients_table = Table(
    'cookieingredients',
    Base.metadata,
    Column('cookie_id', Integer, ForeignKey("cookies.cookie_id"), primary_key=True),
    Column('ingredient_id', Integer, ForeignKey("ingredients.ingredient_id"), primary_key=True)
)

class Ingredient(Base):
    __tablename__ = 'ingredients'

    ingredient_id = Column(Integer, primary_key=True)
    name = Column(String(255), index=True)

    def __repr__(self):
        return "Ingredient(name='{self.name}')".format(self=self)


class Cookie(Base):
    __tablename__ = 'cookies'

    cookie_id = Column(Integer, primary_key=True)
    cookie_name = Column(String(50), index=True)
    cookie_recipe_url = Column(String(255))
    cookie_sku = Column(String(55))
    quantity = Column(Integer())
    unit_cost = Column(Numeric(12, 2))

    ingredients = relationship("Ingredient", secondary=cookieingredients_table)

    def __repr__(self):
        return "Cookie(cookie_name='{self.cookie_name}', " \
                       "cookie_recipe_url='{self.cookie_recipe_url}', " \
                       "cookie_sku='{self.cookie_sku}', " \
                       "quantity={self.quantity}, " \
                       "unit_cost={self.unit_cost})".format(self=self)


Base.metadata.create_all(engine)

session = Session()
cc_cookie = Cookie(
    cookie_name='chocolate chip',
    cookie_recipe_url='http://some.aweso.me/cookie/recipe.html',
    cookie_sku='CC01',
    quantity=12,
    unit_cost=0.50)
flour = Ingredient(name='Flour')
sugar = Ingredient(name='Sugar')
egg = Ingredient(name='Egg')
cc = Ingredient(name='Chocolate Chips')
cc_cookie.ingredients.extend([flour, sugar, egg, cc])
session.add(cc_cookie)
session.commit()

print([ingredient.name for ingredient in cc_cookie.ingredients])
# ['Flour', 'Sugar', 'Egg', 'Chocolate Chips']
