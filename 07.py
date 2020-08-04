import sys
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, Numeric, String, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import desc
from sqlalchemy import func
from sqlalchemy import cast
from sqlalchemy import and_, or_, not_

engine = create_engine('sqlite:///cookies.db')

Session = sessionmaker(bind=engine)

session = Session()

Base = declarative_base()


class Cookie(Base):
    __tablename__ = 'cookies'

    cookie_id = Column(Integer, primary_key=True)
    cookie_name = Column(String(50), index=True)
    cookie_recipe_url = Column(String(255))
    cookie_sku = Column(String(55))
    quantity = Column(Integer())
    unit_cost = Column(Numeric(12, 2))
    # line_item

    def __repr__(self):
        return "Cookie(cookie_name='{self.cookie_name}', " \
                       "cookie_recipe_url='{self.cookie_recipe_url}', " \
                       "cookie_sku='{self.cookie_sku}', " \
                       "quantity={self.quantity}, " \
                       "unit_cost={self.unit_cost})".format(self=self)


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer(), primary_key=True)
    username = Column(String(15), nullable=False, unique=True)
    email_address = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    password = Column(String(25), nullable=False)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    # orders

    def __repr__(self):
        return "User(username='{self.username}', " \
                     "email_address='{self.email_address}', " \
                     "phone='{self.phone}', " \
                     "password='{self.password}')".format(self=self)


class Order(Base):
    __tablename__ = 'orders'
    order_id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.user_id'))
    shipped = Column(Boolean(), default=False)

    user =  relationship("User", backref=backref('orders', order_by=order_id))
    # line_items

    def __repr__(self):
        return "Order(user_id={self.user_id}, " \
                      "shipped={self.shipped})".format(self=self)


class LineItem(Base):
    __tablename__ = 'line_items'
    line_item_id = Column(Integer(), primary_key=True)
    order_id = Column(Integer(), ForeignKey('orders.order_id'))
    cookie_id = Column(Integer(), ForeignKey('cookies.cookie_id'))
    quantity = Column(Integer())
    extended_cost = Column(Numeric(12, 2))

    order = relationship("Order", backref=backref('line_items', order_by=line_item_id))
    cookie = relationship(
        "Cookie",
        backref=('line_item', uselist=False))

    def __repr__(self):
        return "LineItems(order_id={self.order_id}, " \
                          "cookie_id={self.cookie_id}, " \
                          "quantity={self.quantity}, " \
                          "extended_cost={self.extended_cost})".format(
                    self=self)


Base.metadata.create_all(engine)

#################### 插入数据 ####################

cc_cookie = Cookie(
    cookie_name='chocolate chip',
    cookie_recipe_url='http://1',
    cookie_sku='CC01',
    quantity=12,
    unit_cost=0.50)

session.add(cc_cookie)
# print(cc_cookie.cookie_id)  # None
session.commit()
# print(cc_cookie.cookie_id)  # 1

dcc = Cookie(
    cookie_name='dark chocolate chip',
    cookie_recipe_url='http://2',
    cookie_sku='CC02',
    quantity=1,
    unit_cost=0.75)

mol = Cookie(
    cookie_name='molasses',
    cookie_recipe_url='http://3',
    cookie_sku='MOL01',
    quantity=1,
    unit_cost=0.80)

session.add(dcc)
session.add(mol)
# print(dcc.cookie_id)  # None
# print(mol.cookie_id)  # None
session.flush()  # 此时数据库中只有一条数据，flush() 操作并没有将数据写入数据库
# print(dcc.cookie_id)  # 2
# print(mol.cookie_id)  # 3

# 这时做一次提交，将数据写入数据库
session.commit()

c1 = Cookie(
    cookie_name='peanut butter',
    cookie_recipe_url='http://4',
    cookie_sku='PB01',
    quantity=24,
    unit_cost=0.25)

c2 = Cookie(
    cookie_name='oatmeal raisin',
    cookie_recipe_url='http://5',
    cookie_sku='EWW01',
    quantity=100,
    unit_cost=1.00)

session.bulk_save_objects([c1, c2])
# print(c1.cookie_id)  # None
# print(c2.cookie_id)  # None
session.commit()
# print(c1.cookie_id)  # None
# print(c2.cookie_id)  # None


#################### 查询数据 ####################

query = session.query(Cookie)
# print(query)
"""
SELECT
    cookies.cookie_id AS cookies_cookie_id,
    cookies.cookie_name AS cookies_cookie_name,
    cookies.cookie_recipe_url AS cookies_cookie_recipe_url,
    cookies.cookie_sku AS cookies_cookie_sku,
    cookies.quantity AS cookies_quantity,
    cookies.unit_cost AS cookies_unit_cost
FROM cookies
"""
cookies = query.all()
# print(cookies)
"""
[
    Cookie(cookie_name='chocolate chip', cookie_recipe_url='http://1', cookie_sku='CC01', quantity=12, unit_cost=0.50),
    Cookie(cookie_name='dark chocolate chip', cookie_recipe_url='http://2', cookie_sku='CC02', quantity=1, unit_cost=0.75),
    Cookie(cookie_name='molasses', cookie_recipe_url='http://3', cookie_sku='MOL01', quantity=1, unit_cost=0.80),
    Cookie(cookie_name='peanut butter', cookie_recipe_url='http://4', cookie_sku='PB01', quantity=24, unit_cost=0.25),
    Cookie(cookie_name='oatmeal raisin', cookie_recipe_url='http://5', cookie_sku='EWW01', quantity=100, unit_cost=1.00)
]
"""

for cookie in session.query(Cookie):
    # print(cookie)
    pass
    """
    Cookie(cookie_name='chocolate chip', cookie_recipe_url='http://1', cookie_sku='CC01', quantity=12, unit_cost=0.50)
    Cookie(cookie_name='dark chocolate chip', cookie_recipe_url='http://2', cookie_sku='CC02', quantity=1, unit_cost=0.75)
    Cookie(cookie_name='molasses', cookie_recipe_url='http://3', cookie_sku='MOL01', quantity=1, unit_cost=0.80)
    Cookie(cookie_name='peanut butter', cookie_recipe_url='http://4', cookie_sku='PB01', quantity=24, unit_cost=0.25)
    Cookie(cookie_name='oatmeal raisin', cookie_recipe_url='http://5', cookie_sku='EWW01', quantity=100, unit_cost=1.00)
    """

query = session.query(Cookie.cookie_name, Cookie.cookie_recipe_url, Cookie.quantity)
cookie = query.first()
# print(cookie)  # ('chocolate chip', 'http://1', 12)

for cookie in session.query(Cookie).order_by(Cookie.quantity):
    # print('{:3} - {} - {}'.format(cookie.quantity, cookie.cookie_name, cookie.cookie_recipe_url))
    pass
    """
      1 - dark chocolate chip - http://2
      1 - molasses - http://3
     12 - chocolate chip - http://1
     24 - peanut butter - http://4
    100 - oatmeal raisin - http://5
    """

for cookie in session.query(Cookie).order_by(desc(Cookie.quantity)):
    # print('{:3} - {}'.format(cookie.quantity, cookie.cookie_name, cookie.cookie_recipe_url))
    pass
    """
    100 - oatmeal raisin
     24 - peanut butter
     12 - chocolate chip
      1 - dark chocolate chip
      1 - molasses
    """

query = session.query(Cookie).order_by(Cookie.quantity)[:2]
# print([result.cookie_name for result in query])  # ['dark chocolate chip', 'molasses']

query = session.query(Cookie).order_by(Cookie.quantity).limit(2)
# print([result.cookie_name for result in query])  # ['dark chocolate chip', 'molasses']

rec_count = session.query(func.count(Cookie.cookie_name)).first()
# print(rec_count)  # (5,)
rec_count = session.query(func.count(Cookie.cookie_name)).scalar()
# print(rec_count)  # 5

inv_count = session.query(func.sum(Cookie.quantity)).scalar()
# print(inv_count)  # 138

rec_count = session.query(func.count(Cookie.cookie_name).label('inventory_count')).first()
# print(rec_count.keys())  # ['inventory_count']
# print(rec_count.inventory_count)  # 5

record = session.query(Cookie).filter(Cookie.cookie_name == 'chocolate chip').first()
# print(record)  # Cookie(cookie_name='chocolate chip', cookie_recipe_url='http://1', cookie_sku='CC01', quantity=12, unit_cost=0.50)

record = session.query(Cookie).filter_by(cookie_name='chocolate chip').first()
# print(record)  # Cookie(cookie_name='chocolate chip', cookie_recipe_url='http://1', cookie_sku='CC01', quantity=12, unit_cost=0.50)

query = session.query(Cookie).filter(Cookie.cookie_name.like('%chocolate%'))
for record in query:
    # print(record.cookie_name)
    pass
    """
    chocolate chip
    dark chocolate chip
    """

results = session.query(Cookie.cookie_name, 'SKU-' + Cookie.cookie_sku).all()
for row in results:
    # print(row)
    pass
    """
    ('chocolate chip', 'SKU-CC01')
    ('dark chocolate chip', 'SKU-CC02')
    ('molasses', 'SKU-MOL01')
    ('peanut butter', 'SKU-PB01')
    ('oatmeal raisin', 'SKU-EWW01')
    """

query = session.query(
    Cookie.cookie_name,
    cast(
        (Cookie.quantity * Cookie.unit_cost),
        Numeric(12,2)).label('inv_cost'))
for result in query:
    # print('{} - {}'.format(result.cookie_name, result.inv_cost))
    pass
    """
    chocolate chip - 6.00
    dark chocolate chip - 0.75
    molasses - 0.80
    peanut butter - 6.00
    oatmeal raisin - 100.00
    """

query = session.query(Cookie).filter(
    Cookie.quantity > 23,
    Cookie.unit_cost < 0.40
)
for result in query:
    # print(result.cookie_name)
    pass
    # peanut butter

query = session.query(Cookie).filter(
    or_(
        Cookie.quantity.between(10, 50),
        Cookie.cookie_name.contains('chip')
    )
)
for result in query:
    # print(result.cookie_name)
    pass
    """
    chocolate chip
    dark chocolate chip
    peanut butter
    """


#################### 更新数据 ####################

"""
INSERT INTO "main"."cookies" ("cookie_id", "cookie_name", "cookie_recipe_url", "cookie_sku", "quantity", "unit_cost") VALUES ('1', 'chocolate chip', 'http://1', 'CC01', '12', '0.5');
INSERT INTO "main"."cookies" ("cookie_id", "cookie_name", "cookie_recipe_url", "cookie_sku", "quantity", "unit_cost") VALUES ('2', 'dark chocolate chip', 'http://2', 'CC02', '1', '0.75');
INSERT INTO "main"."cookies" ("cookie_id", "cookie_name", "cookie_recipe_url", "cookie_sku", "quantity", "unit_cost") VALUES ('3', 'molasses', 'http://3', 'MOL01', '1', '0.8');
INSERT INTO "main"."cookies" ("cookie_id", "cookie_name", "cookie_recipe_url", "cookie_sku", "quantity", "unit_cost") VALUES ('4', 'peanut butter', 'http://4', 'PB01', '24', '0.25');
INSERT INTO "main"."cookies" ("cookie_id", "cookie_name", "cookie_recipe_url", "cookie_sku", "quantity", "unit_cost") VALUES ('5', 'oatmeal raisin', 'http://5', 'EWW01', '100', '1');
"""

query = session.query(Cookie)
cc_cookie = query.filter(Cookie.cookie_name == "chocolate chip").first()
# print(cc_cookie)
# Cookie(cookie_name='chocolate chip', cookie_recipe_url='http://1', cookie_sku='CC01', quantity=12, unit_cost=0.50)
cc_cookie.quantity = cc_cookie.quantity + 120
# print(cc_cookie)
# Cookie(cookie_name='chocolate chip', cookie_recipe_url='http://1', cookie_sku='CC01', quantity=132, unit_cost=0.50)
session.commit()
# print(cc_cookie.quantity)  # 132

query = session.query(Cookie)
query = query.filter(Cookie.cookie_name == "chocolate chip")
cc_cookie = query.first()
# print(cc_cookie)  # Cookie(cookie_name='chocolate chip', cookie_recipe_url='http://1', cookie_sku='CC01', quantity=132, unit_cost=0.50)
query.update({Cookie.quantity: Cookie.quantity - 20})
cc_cookie = query.first()
# print(cc_cookie)  # Cookie(cookie_name='chocolate chip', cookie_recipe_url='http://1', cookie_sku='CC01', quantity=112, unit_cost=0.50)
# print(cc_cookie.quantity)  # 112
# 此时没有提交，所以数据库中的数据没有被修改，只是对象被修改了

#################### 删除数据 ####################

"""
INSERT INTO "main"."cookies" ("cookie_id", "cookie_name", "cookie_recipe_url", "cookie_sku", "quantity", "unit_cost") VALUES ('1', 'chocolate chip', 'http://1', 'CC01', '132', '0.5');
INSERT INTO "main"."cookies" ("cookie_id", "cookie_name", "cookie_recipe_url", "cookie_sku", "quantity", "unit_cost") VALUES ('2', 'dark chocolate chip', 'http://2', 'CC02', '1', '0.75');
INSERT INTO "main"."cookies" ("cookie_id", "cookie_name", "cookie_recipe_url", "cookie_sku", "quantity", "unit_cost") VALUES ('3', 'molasses', 'http://3', 'MOL01', '1', '0.8');
INSERT INTO "main"."cookies" ("cookie_id", "cookie_name", "cookie_recipe_url", "cookie_sku", "quantity", "unit_cost") VALUES ('4', 'peanut butter', 'http://4', 'PB01', '24', '0.25');
INSERT INTO "main"."cookies" ("cookie_id", "cookie_name", "cookie_recipe_url", "cookie_sku", "quantity", "unit_cost") VALUES ('5', 'oatmeal raisin', 'http://5', 'EWW01', '100', '1');
"""

query = session.query(Cookie)
query = query.filter(Cookie.cookie_name == "dark chocolate chip")
dcc_cookie = query.one()
# print(dcc_cookie)  # Cookie(cookie_name='dark chocolate chip', cookie_recipe_url='http://2', cookie_sku='CC02', quantity=1, unit_cost=0.75)
session.delete(dcc_cookie)
session.commit()
dcc_cookie = query.first()
# print(dcc_cookie)  # None

"""
INSERT INTO "main"."cookies" ("cookie_id", "cookie_name", "cookie_recipe_url", "cookie_sku", "quantity", "unit_cost") VALUES ('1', 'chocolate chip', 'http://1', 'CC01', '112', '0.5');
INSERT INTO "main"."cookies" ("cookie_id", "cookie_name", "cookie_recipe_url", "cookie_sku", "quantity", "unit_cost") VALUES ('3', 'molasses', 'http://3', 'MOL01', '1', '0.8');
INSERT INTO "main"."cookies" ("cookie_id", "cookie_name", "cookie_recipe_url", "cookie_sku", "quantity", "unit_cost") VALUES ('4', 'peanut butter', 'http://4', 'PB01', '24', '0.25');
INSERT INTO "main"."cookies" ("cookie_id", "cookie_name", "cookie_recipe_url", "cookie_sku", "quantity", "unit_cost") VALUES ('5', 'oatmeal raisin', 'http://5', 'EWW01', '100', '1');
"""

query = session.query(Cookie)
query = query.filter(Cookie.cookie_name == "molasses")
mol_cookie = query.one()
# print(mol_cookie)  # Cookie(cookie_name='molasses', cookie_recipe_url='http://3', cookie_sku='MOL01', quantity=1, unit_cost=0.80)
query.delete()
mol_cookie = query.first()
# print(mol_cookie)  # None
# 此时没有提交，所以数据库中的数据没有被删除，只是对象置为 None

session.commit()
# 提交之后数据被删除

#################### 多表关联处理数据 ####################

cookiemon = User(
    username='cookiemon',
    email_address='mon@cookie.com',
    phone='111-111-1111',
    password='password')
cakeeater = User(
    username='cakeeater',
    email_address='cakeeater@cake.com',
    phone='222-222-2222',
    password='password')
pieperson = User(
    username='pieperson',
    email_address='person@pie.com',
    phone='333-333-3333',
    password='password')
session.add(cookiemon)
session.add(cakeeater)
session.add(pieperson)
session.commit()

"""
INSERT INTO "main"."cookies" ("cookie_id", "cookie_name", "cookie_recipe_url", "cookie_sku", "quantity", "unit_cost") VALUES ('1', 'chocolate chip', 'http://1', 'CC01', '112', '0.5');
INSERT INTO "main"."cookies" ("cookie_id", "cookie_name", "cookie_recipe_url", "cookie_sku", "quantity", "unit_cost") VALUES ('4', 'peanut butter', 'http://4', 'PB01', '24', '0.25');
INSERT INTO "main"."cookies" ("cookie_id", "cookie_name", "cookie_recipe_url", "cookie_sku", "quantity", "unit_cost") VALUES ('5', 'oatmeal raisin', 'http://5', 'EWW01', '100', '1');

INSERT INTO "main"."users" ("user_id", "username", "email_address", "phone", "password", "created_on", "updated_on") VALUES ('1', 'cookiemon', 'mon@cookie.com', '111-111-1111', 'password', '2020-08-04 18:04:43.066498', '2020-08-04 18:04:43.066507');
INSERT INTO "main"."users" ("user_id", "username", "email_address", "phone", "password", "created_on", "updated_on") VALUES ('2', 'cakeeater', 'cakeeater@cake.com', '222-222-2222', 'password', '2020-08-04 18:04:43.066904', '2020-08-04 18:04:43.066907');
INSERT INTO "main"."users" ("user_id", "username", "email_address", "phone", "password", "created_on", "updated_on") VALUES ('3', 'pieperson', 'person@pie.com', '333-333-3333', 'password', '2020-08-04 18:04:43.066980', '2020-08-04 18:04:43.066983');
"""

o1 = Order()
# o1.user = cookiemon
cookiemon.orders.append(o1)
session.add(o1)
session.commit()
"""
INSERT INTO "main"."orders" ("order_id", "user_id", "shipped") VALUES ('1', '1', '0');
"""

cc = session.query(Cookie).filter(Cookie.cookie_name == "chocolate chip").one()
# print(cc)  # Cookie(cookie_name='chocolate chip', cookie_recipe_url='http://1', cookie_sku='CC01', quantity=112, unit_cost=0.50)
line1 = LineItem(quantity=2, extended_cost=1.00)
# line1.cookie = cc
# line1.order = o1
cc.line_item = line1

pb = session.query(Cookie).filter(Cookie.cookie_name == "peanut butter").one()
# print(pb)  # Cookie(cookie_name='peanut butter', cookie_recipe_url='http://4', cookie_sku='PB01', quantity=24, unit_cost=0.25)
line2 = LineItem(quantity=12, extended_cost=3.00)
# line2.cookie = pb
# line2.order = o1
pb.line_item = line2

o1.line_items.append(line1)
o1.line_items.append(line2)
session.commit()





