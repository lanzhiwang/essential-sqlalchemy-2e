from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Numeric, String, DateTime, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine

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
"""
class Cookie(Base):
    __tablename__ = 'cookies'

    cookie_id = Column(Integer(), primary_key=True)
    cookie_name = Column(String(50), index=True)
    cookie_recipe_url = Column(String(255))
    cookie_sku = Column(String(55))
    quantity = Column(Integer())
    unit_cost = Column(Numeric(12, 2))

print(Cookie.__table__)
"""
Table(
    'cookies',
    MetaData(bind=None),
    Column('cookie_id', Integer(), table=<cookies>, primary_key=True, nullable=False),
    Column('cookie_name', String(length=50), table=<cookies>),
    Column('cookie_recipe_url', String(length=255), table=<cookies>),
    Column('cookie_sku', String(length=55), table=<cookies>),
    Column('quantity', Integer(), table=<cookies>),
    Column('unit_cost', Numeric(precision=12, scale=2), table=<cookies>),
    schema=None)
"""

"""
CREATE TABLE users (
	user_id INTEGER NOT NULL,
	username VARCHAR(15) NOT NULL,
	email_address VARCHAR(255) NOT NULL,
	phone VARCHAR(20) NOT NULL,
	password VARCHAR(25) NOT NULL,
	created_on DATETIME,
	updated_on DATETIME,
	PRIMARY KEY (user_id),
	UNIQUE (username)
)
"""
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


"""
CREATE TABLE orders (
	order_id INTEGER NOT NULL,
	user_id INTEGER,
	shipped BOOLEAN,
	PRIMARY KEY (order_id),
	FOREIGN KEY(user_id) REFERENCES users (user_id),
	CHECK (shipped IN (0, 1))
)
"""
class Order(Base):
    __tablename__ = 'orders'
    order_id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.user_id'))
    shipped = Column(Boolean(), default=False)
    user =  relationship("User", backref=backref('orders', order_by=id))
    # line_items


"""
CREATE TABLE line_items (
	line_items_id INTEGER NOT NULL,
	order_id INTEGER,
	cookie_id INTEGER,
	quantity INTEGER,
	extended_cost NUMERIC(12, 2),
	PRIMARY KEY (line_items_id),
	FOREIGN KEY(order_id) REFERENCES orders (order_id),
	FOREIGN KEY(cookie_id) REFERENCES cookies (cookie_id)
)
"""
class LineItems(Base):
    __tablename__ = 'line_items'
    line_items_id = Column(Integer(), primary_key=True)
    order_id = Column(Integer(), ForeignKey('orders.order_id'))
    cookie_id = Column(Integer(), ForeignKey('cookies.cookie_id'))
    quantity = Column(Integer())
    extended_cost = Column(Numeric(12, 2))
    order = relationship("Order", backref=backref('line_items', order_by=line_items_id))
    cookie = relationship("Cookie", uselist=False)


engine = create_engine('sqlite:///cookies.db')

Base.metadata.create_all(engine)
