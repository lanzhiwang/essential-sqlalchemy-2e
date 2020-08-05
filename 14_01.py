from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, Numeric, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy import desc

engine = create_engine('sqlite:///cookies.db')

Session = sessionmaker(bind=engine)

Base = declarative_base()


class Cookie(Base):
    __tablename__ = 'cookies'

    cookie_id = Column(Integer, primary_key=True)
    cookie_name = Column(String(50), index=True)
    cookie_recipe_url = Column(String(255))
    cookie_sku = Column(String(55))
    quantity = Column(Integer())
    unit_cost = Column(Numeric(12, 2))

    @hybrid_property
    def inventory_value(self):
        return self.unit_cost * self.quantity

    @hybrid_method
    def bake_more(self, min_quantity):
        return self.quantity < min_quantity

    def __repr__(self):
        return "Cookie(cookie_name='{self.cookie_name}', " \
                       "cookie_recipe_url='{self.cookie_recipe_url}', " \
                       "cookie_sku='{self.cookie_sku}', " \
                       "quantity={self.quantity}, " \
                       "unit_cost={self.unit_cost})".format(self=self)

Base.metadata.create_all(engine)

print(Cookie.inventory_value < 10.00)  # cookies.unit_cost * cookies.quantity < :param_1
print(Cookie.bake_more(12))  # cookies.quantity < :quantity_1

session = Session()
cc_cookie = Cookie(
    cookie_name='chocolate chip',
    cookie_recipe_url='http://some.aweso.me/cookie/recipe.html',
    cookie_sku='CC01',
    quantity=12,
    unit_cost=0.50)
dcc = Cookie(
    cookie_name='dark chocolate chip',
    cookie_recipe_url='http://some.aweso.me/cookie/recipe_dark.html',
    cookie_sku='CC02',
    quantity=1,
    unit_cost=0.75)
mol = Cookie(
    cookie_name='molasses',
    cookie_recipe_url='http://some.aweso.me/cookie/recipe_molasses.html',
    cookie_sku='MOL01',
    quantity=1,
    unit_cost=0.80)

session.add(cc_cookie)
session.add(dcc)
session.add(mol)
session.flush()

print(dcc.inventory_value)
print(dcc.bake_more(12))

query = session.query(Cookie).order_by(desc(Cookie.inventory_value))
print(query)
"""
SELECT cookies.cookie_id AS cookies_cookie_id, cookies.cookie_name AS cookies_cookie_name, cookies.cookie_recipe_url AS cookies_cookie_recipe_url, cookies.cookie_sku AS cookies_cookie_sku, cookies.quantity AS cookies_quantity, cookies.unit_cost AS cookies_unit_cost
FROM cookies
ORDER BY cookies.unit_cost * cookies.quantity DESC
"""
for cookie in query:
    print('{:>20} - {:.2f}'.format(cookie.cookie_name, cookie.inventory_value))
"""
      chocolate chip - 6.00
            molasses - 0.80
 dark chocolate chip - 0.75
"""

query = session.query(Cookie).filter(Cookie.bake_more(12))
print(query)
"""
SELECT cookies.cookie_id AS cookies_cookie_id, cookies.cookie_name AS cookies_cookie_name, cookies.cookie_recipe_url AS cookies_cookie_recipe_url, cookies.cookie_sku AS cookies_cookie_sku, cookies.quantity AS cookies_quantity, cookies.unit_cost AS cookies_unit_cost
FROM cookies
WHERE cookies.quantity < ?
"""
for cookie in query:
    print('{:>20} - {}'.format(cookie.cookie_name, cookie.quantity))
"""
 dark chocolate chip - 1
            molasses - 1
"""
