from datetime import datetime
import sys

from sqlalchemy import (MetaData, Table, Column, Integer, Numeric, String,
                        DateTime, ForeignKey, Boolean, create_engine)
from sqlalchemy import insert
from sqlalchemy.sql import select
from sqlalchemy import desc
from sqlalchemy.sql import func
from sqlalchemy import cast
from sqlalchemy import and_, or_, not_
from sqlalchemy import update
from sqlalchemy import delete
from sqlalchemy import text


metadata = MetaData()

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
CREATE INDEX ix_cookies_cookie_name ON cookies (cookie_name)
"""
cookies = Table(
    'cookies',  # 数据库表名
    metadata,  # 元数据对象
    Column('cookie_id', Integer(), primary_key=True), # 数据库字段
    Column('cookie_name', String(50), index=True),
    Column('cookie_recipe_url', String(255)),
    Column('cookie_sku', String(55)),
    Column('quantity', Integer()),
    Column('unit_cost', Numeric(12, 2))
)

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
users = Table(
    'users',
    metadata,
    Column('user_id', Integer(), primary_key=True),
    Column('username', String(15), nullable=False, unique=True),
    Column('email_address', String(255), nullable=False),
    Column('phone', String(20), nullable=False),
    Column('password', String(25), nullable=False),
    Column('created_on', DateTime(), default=datetime.now),
    Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now)
)

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
orders = Table(
    'orders',
    metadata,
    Column('order_id', Integer(), primary_key=True),
    Column('user_id', ForeignKey('users.user_id')),
    Column('shipped', Boolean(), default=False)
)

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
line_items = Table(
    'line_items',
    metadata,
    Column('line_items_id', Integer(), primary_key=True),
    Column('order_id', ForeignKey('orders.order_id')),
    Column('cookie_id', ForeignKey('cookies.cookie_id')),
    Column('quantity', Integer()),
    Column('extended_cost', Numeric(12, 2))
)

# 实例化引擎
engine = create_engine('sqlite:///cookies.db')

# 将引擎对象注入元数据对象
metadata.create_all(engine)

# 从引擎获取连接
connection = engine.connect()

#################### 插入数据 ####################

# 第一种将数据写入数据库的方式，但是此时并没有将数据写入数据库
ins = cookies.insert().values(
    cookie_name="chocolate chip",
    cookie_recipe_url="http://some.aweso.me/cookie/recipe.html",
    cookie_sku="CC01",
    quantity="12",
    unit_cost="0.50"
)
# print(str(ins))
"""
INSERT INTO cookies (
    cookie_name,
    cookie_recipe_url,
    cookie_sku,
    quantity,
    unit_cost)
    VALUES (
        :cookie_name,
        :cookie_recipe_url,
        :cookie_sku,
        :quantity,
        :unit_cost)

"""

# print(ins.compile().params)
"""
{
    'cookie_name': 'chocolate chip',
    'cookie_recipe_url': 'http://some.aweso.me/cookie/recipe.html',
    'cookie_sku': 'CC01',
    'quantity': '12',
    'unit_cost': '0.50'
}
"""

# 将数据写入数据库
result = connection.execute(ins)
# print(result.inserted_primary_key)  # [1]

# 第二种将数据写入数据库的方式，但是此时并没有将数据写入数据库
ins = insert(cookies).values(
    cookie_name="chocolate chip",
    cookie_recipe_url="http://some.aweso.me/cookie/recipe.html",
    cookie_sku="CC01",
    quantity="12",
    unit_cost="0.50"
)
# print(str(ins))
"""
INSERT INTO cookies (cookie_name, cookie_recipe_url, cookie_sku, quantity, unit_cost)
    VALUES (:cookie_name, :cookie_recipe_url, :cookie_sku, :quantity, :unit_cost)
"""
# print(ins.compile().params)
"""
{
    'cookie_name': 'chocolate chip',
    'cookie_recipe_url': 'http://some.aweso.me/cookie/recipe.html',
    'cookie_sku': 'CC01',
    'quantity': '12',
    'unit_cost': '0.50'
}
"""
# 将数据写入数据库
result = connection.execute(ins)
# print(result.inserted_primary_key)  # [2]

# 第三种将数据写入数据库的方式，但是此时并没有将数据写入数据库
ins = cookies.insert()
result = connection.execute(
    ins,
    cookie_name='dark chocolate chip',
    cookie_recipe_url='http://some.aweso.me/cookie/recipe_dark.html',
    cookie_sku='CC02',
    quantity='1',
    unit_cost='0.75')
# print(result.inserted_primary_key)  # [3]

# 批量增加数据
inventory_list = [
    {
        'cookie_name': 'peanut butter',
        'cookie_recipe_url': 'http://some.aweso.me/cookie/peanut.html',
        'cookie_sku': 'PB01',
        'quantity': '24',
        'unit_cost': '0.25'
    },
    {
        'cookie_name': 'oatmeal raisin',
        'cookie_recipe_url': 'http://some.okay.me/cookie/raisin.html',
        'cookie_sku': 'EWW01',
        'quantity': '100',
        'unit_cost': '1.00'
    }
]
result = connection.execute(ins, inventory_list)
# print(result.rowcount)  # 2

"""
INSERT INTO "main"."cookies" ("cookie_id", "cookie_name", "cookie_recipe_url", "cookie_sku", "quantity", "unit_cost") VALUES ('1', 'chocolate chip', 'http://some.aweso.me/cookie/recipe.html', 'CC01', '12', '0.5');
INSERT INTO "main"."cookies" ("cookie_id", "cookie_name", "cookie_recipe_url", "cookie_sku", "quantity", "unit_cost") VALUES ('2', 'chocolate chip', 'http://some.aweso.me/cookie/recipe.html', 'CC01', '12', '0.5');
INSERT INTO "main"."cookies" ("cookie_id", "cookie_name", "cookie_recipe_url", "cookie_sku", "quantity", "unit_cost") VALUES ('3', 'dark chocolate chip', 'http://some.aweso.me/cookie/recipe_dark.html', 'CC02', '1', '0.75');
INSERT INTO "main"."cookies" ("cookie_id", "cookie_name", "cookie_recipe_url", "cookie_sku", "quantity", "unit_cost") VALUES ('4', 'peanut butter', 'http://some.aweso.me/cookie/peanut.html', 'PB01', '24', '0.25');
INSERT INTO "main"."cookies" ("cookie_id", "cookie_name", "cookie_recipe_url", "cookie_sku", "quantity", "unit_cost") VALUES ('5', 'oatmeal raisin', 'http://some.okay.me/cookie/raisin.html', 'EWW01', '100', '1');
"""

#################### 查询数据 ####################

# 第一种查询的方法
s = select([cookies])
# print(str(s))
"""
SELECT cookies.cookie_id, cookies.cookie_name, cookies.cookie_recipe_url, cookies.cookie_sku, cookies.quantity, cookies.unit_cost
FROM cookies
"""
rp = connection.execute(s)
results = rp.fetchall()
first_row = results[0]
# print(first_row[1])  # chocolate chip
# print(first_row.cookie_name)  # chocolate chip
# print(first_row[cookies.c.cookie_name])  # chocolate chip

# 第二种查询的方法
s = cookies.select()
# print(str(s))
"""
SELECT cookies.cookie_id, cookies.cookie_name, cookies.cookie_recipe_url, cookies.cookie_sku, cookies.quantity, cookies.unit_cost
FROM cookies
"""
rp = connection.execute(s)
for record in rp:
    # print(record.cookie_name)
    pass
    """
    chocolate chip
    chocolate chip
    dark chocolate chip
    peanut butter
    oatmeal raisin
    """

# 第三种查询数据的方法
s = select([cookies.c.cookie_name, cookies.c.quantity])
# print(str(s))
"""
SELECT cookies.cookie_name, cookies.quantity
FROM cookies
"""
rp = connection.execute(s)
# print(rp.keys())  # ['cookie_name', 'quantity']
results = rp.fetchall()

# 排序
s = select([cookies.c.cookie_name, cookies.c.quantity])
s = s.order_by(cookies.c.quantity, cookies.c.cookie_name)
# print(str(s))
"""
SELECT cookies.cookie_name, cookies.quantity
FROM cookies ORDER BY cookies.quantity, cookies.cookie_name
"""
rp = connection.execute(s)
for cookie in rp:
    # print('{} - {}'.format(cookie.quantity, cookie.cookie_name))
    pass
    """
    1 - dark chocolate chip
    12 - chocolate chip
    12 - chocolate chip
    24 - peanut butter
    100 - oatmeal raisin
    """


s = select([cookies.c.cookie_name, cookies.c.quantity])
s = s.order_by(desc(cookies.c.quantity))
# print(str(s))
"""
SELECT cookies.cookie_name, cookies.quantity
FROM cookies ORDER BY cookies.quantity DESC
"""
rp = connection.execute(s)
for cookie in rp:
    # print('{} - {}'.format(cookie.quantity, cookie.cookie_name))
    pass
    """
    100 - oatmeal raisin
    24 - peanut butter
    12 - chocolate chip
    12 - chocolate chip
    1 - dark chocolate chip
    """

# limit
s = select([cookies.c.cookie_name, cookies.c.quantity])
s = s.order_by(cookies.c.quantity)
s = s.limit(2)
# print(str(s))
"""
SELECT cookies.cookie_name, cookies.quantity
FROM cookies ORDER BY cookies.quantity
 LIMIT :param_1
"""
# print(s.compile().params)  # {'param_1': 2}
rp = connection.execute(s)
# print([result.cookie_name for result in rp])  # ['dark chocolate chip', 'chocolate chip']

s = cookies.select(limit=1)
# print(str(s))
"""
SELECT cookies.cookie_id, cookies.cookie_name, cookies.cookie_recipe_url, cookies.cookie_sku, cookies.quantity, cookies.unit_cost
FROM cookies
 LIMIT :param_1
"""
# print(s.compile().params)  # {'param_1': 1}
for row in connection.execute(s):
    # print(row)
    """
    (1, 'chocolate chip', 'http://some.aweso.me/cookie/recipe.html', 'CC01', 12, Decimal('0.50'))
    """

# 使用数据库函数
s = select([func.count(cookies.c.cookie_name)])
# print(str(s))
"""
SELECT count(cookies.cookie_name) AS count_1
FROM cookies
"""
rp = connection.execute(s)
record = rp.first()
# print(record.keys())  # ['count_1']
# print(record.count_1)  # 5

s = select([func.count(cookies.c.cookie_name).label('inventory_count')])
# print(str(s))
"""
SELECT count(cookies.cookie_name) AS inventory_count
FROM cookies
"""
rp = connection.execute(s)
record = rp.first()
# print(record.keys())  # ['inventory_count']
# print(record.inventory_count)  # 5

# where
s = select([cookies]).where(cookies.c.cookie_name == 'chocolate chip')
# print(str(s))
# print(s.compile().params)
rp = connection.execute(s)
record = rp.first()
# print(record.items())
"""
SELECT cookies.cookie_id, cookies.cookie_name, cookies.cookie_recipe_url, cookies.cookie_sku, cookies.quantity, cookies.unit_cost
FROM cookies
WHERE cookies.cookie_name = :cookie_name_1
{'cookie_name_1': 'chocolate chip'}
[('cookie_id', 1), ('cookie_name', 'chocolate chip'), ('cookie_recipe_url', 'http://some.aweso.me/cookie/recipe.html'), ('cookie_sku', 'CC01'), ('quantity', 12), ('unit_cost', Decimal('0.50'))]
"""

s = select([cookies]).where(cookies.c.cookie_name.like('%chocolate%')).where(cookies.c.quantity == 12)
# print(str(s))
# print(s.compile().params)
rp = connection.execute(s)
for record in rp.fetchall():
    # print(record.cookie_name)
    pass

"""
SELECT cookies.cookie_id, cookies.cookie_name, cookies.cookie_recipe_url, cookies.cookie_sku, cookies.quantity, cookies.unit_cost
FROM cookies
WHERE cookies.cookie_name LIKE :cookie_name_1 AND cookies.quantity = :quantity_1
{'cookie_name_1': '%chocolate%', 'quantity_1': 12}
chocolate chip
chocolate chip
"""

# 不常见用法
s = select([cookies.c.cookie_name, 'SKU-' + cookies.c.cookie_sku])
# print(str(s))
# print(s.compile().params)
for row in connection.execute(s):
    # print(row)
    pass

"""
SELECT cookies.cookie_name, :cookie_sku_1 || cookies.cookie_sku AS anon_1
FROM cookies
{'cookie_sku_1': 'SKU-'}
('chocolate chip', 'SKU-CC01')
('chocolate chip', 'SKU-CC01')
('dark chocolate chip', 'SKU-CC02')
('peanut butter', 'SKU-PB01')
('oatmeal raisin', 'SKU-EWW01')
"""

s = select([cookies.c.cookie_name, cookies.c.quantity * cookies.c.unit_cost])
# print(str(s))
for row in connection.execute(s):
    # print('{} - {}'.format(row.cookie_name, row.anon_1))
    pass

"""
SELECT cookies.cookie_name, cookies.quantity * cookies.unit_cost AS anon_1
FROM cookies
chocolate chip - 6.00
chocolate chip - 6.00
dark chocolate chip - 0.75
peanut butter - 6.00
oatmeal raisin - 100.00
"""

s = select([cookies.c.cookie_name, cast((cookies.c.quantity * cookies.c.unit_cost), Numeric(12,2)).label('inv_cost')])
# print(str(s))
for row in connection.execute(s):
    # print('{} - {}'.format(row.cookie_name, row.inv_cost))
    pass

"""
SELECT cookies.cookie_name, CAST(cookies.quantity * cookies.unit_cost AS NUMERIC(12, 2)) AS inv_cost
FROM cookies
chocolate chip - 6.00
chocolate chip - 6.00
dark chocolate chip - 0.75
peanut butter - 6.00
oatmeal raisin - 100.00
"""

s = select([cookies.c.cookie_name, (cookies.c.quantity * cookies.c.unit_cost).label('inv_cost')])
# print(str(s))
for row in connection.execute(s):
    # print('{:<25} {:.2f}'.format(row.cookie_name, row.inv_cost))
    pass

"""
SELECT cookies.cookie_name, cookies.quantity * cookies.unit_cost AS inv_cost
FROM cookies
chocolate chip            6.00
chocolate chip            6.00
dark chocolate chip       0.75
peanut butter             6.00
oatmeal raisin            100.00
"""

# and or not
s = select([cookies]).where(and_(
    cookies.c.quantity > 23,
    cookies.c.unit_cost < 0.40
))
# print(str(s))
# print(s.compile().params)
for row in connection.execute(s):
    # print(row.cookie_name)
    pass

"""
SELECT cookies.cookie_id, cookies.cookie_name, cookies.cookie_recipe_url, cookies.cookie_sku, cookies.quantity, cookies.unit_cost
FROM cookies
WHERE cookies.quantity > :quantity_1 AND cookies.unit_cost < :unit_cost_1
{'quantity_1': 23, 'unit_cost_1': 0.4}
peanut butter
"""

s = select([cookies]).where(or_(
    cookies.c.quantity.between(10, 50),
    cookies.c.cookie_name.contains('chip')
))
# print(str(s))
# print(s.compile().params)
for row in connection.execute(s):
    # print(row.cookie_name)
    pass

"""
SELECT cookies.cookie_id, cookies.cookie_name, cookies.cookie_recipe_url, cookies.cookie_sku, cookies.quantity, cookies.unit_cost
FROM cookies
WHERE cookies.quantity BETWEEN :quantity_1 AND :quantity_2 OR (cookies.cookie_name LIKE '%' || :cookie_name_1 || '%')
{'quantity_1': 10, 'quantity_2': 50, 'cookie_name_1': 'chip'}
chocolate chip
chocolate chip
dark chocolate chip
peanut butter
"""

#################### 更新数据 ####################

# update
u = update(cookies).where(cookies.c.cookie_name == "chocolate chip")
# print(str(u))
# print(u.compile().params)
u = u.values(quantity=(cookies.c.quantity + 120))
# print(str(u))
# print(u.compile().params)
result = connection.execute(u)
# print(result.rowcount)
"""
UPDATE
    cookies SET cookie_id=:cookie_id, cookie_name=:cookie_name, cookie_recipe_url=:cookie_recipe_url,
    cookie_sku=:cookie_sku, quantity=:quantity, unit_cost=:unit_cost
WHERE cookies.cookie_name = :cookie_name_1
{
    'cookie_id': None,
    'cookie_name': None,
    'cookie_recipe_url': None,
    'cookie_sku': None,
    'quantity': None,
    'unit_cost': None,
    'cookie_name_1': 'chocolate chip'
}
UPDATE cookies SET quantity=(cookies.quantity + :quantity_1) WHERE cookies.cookie_name = :cookie_name_1
{'quantity_1': 120, 'cookie_name_1': 'chocolate chip'}
2
"""

s = select([cookies]).where(cookies.c.cookie_name == "chocolate chip")
result = connection.execute(s).first()
for key in result.keys():
    # print('{:>20}: {}'.format(key, result[key]))
    pass

#################### 删除数据 ####################

# delete
u = delete(cookies).where(cookies.c.cookie_name == "dark chocolate chip")
# print(str(u))
# print(u.compile().params)
# result = connection.execute(u)
# print(result.rowcount)
s = select([cookies]).where(cookies.c.cookie_name == "dark chocolate chip")
result = connection.execute(s).fetchall()
# print(len(result))
# print(result)
"""
DELETE FROM cookies WHERE cookies.cookie_name = :cookie_name_1
{'cookie_name_1': 'dark chocolate chip'}
1
0
[]
"""

#################### 连接查询 ####################

"""
INSERT INTO "main"."cookies" ("cookie_id", "cookie_name", "cookie_recipe_url", "cookie_sku", "quantity", "unit_cost") VALUES ('1', 'chocolate chip', 'http://some.aweso.me/cookie/recipe.html', 'CC01', '132', '0.5');
INSERT INTO "main"."cookies" ("cookie_id", "cookie_name", "cookie_recipe_url", "cookie_sku", "quantity", "unit_cost") VALUES ('2', 'chocolate chip', 'http://some.aweso.me/cookie/recipe.html', 'CC01', '132', '0.5');
INSERT INTO "main"."cookies" ("cookie_id", "cookie_name", "cookie_recipe_url", "cookie_sku", "quantity", "unit_cost") VALUES ('3', 'dark chocolate chip', 'http://some.aweso.me/cookie/recipe_dark.html', 'CC02', '1', '0.75');
INSERT INTO "main"."cookies" ("cookie_id", "cookie_name", "cookie_recipe_url", "cookie_sku", "quantity", "unit_cost") VALUES ('4', 'peanut butter', 'http://some.aweso.me/cookie/peanut.html', 'PB01', '24', '0.25');
INSERT INTO "main"."cookies" ("cookie_id", "cookie_name", "cookie_recipe_url", "cookie_sku", "quantity", "unit_cost") VALUES ('5', 'oatmeal raisin', 'http://some.okay.me/cookie/raisin.html', 'EWW01', '100', '1');
"""

customer_list = [
    {
        'username': "cookiemon",
        'email_address': "mon@cookie.com",
        'phone': "111-111-1111",
        'password': "password"
    },
    {
        'username': "cakeeater",
        'email_address': "cakeeater@cake.com",
        'phone': "222-222-2222",
        'password': "password"
    },
    {
        'username': "pieguy",
        'email_address': "guy@pie.com",
        'phone': "333-333-3333",
        'password': "password"
    }
]
ins = users.insert()
result = connection.execute(ins, customer_list)
"""
INSERT INTO "main"."users" ("user_id", "username", "email_address", "phone", "password", "created_on", "updated_on") VALUES ('1', 'cookiemon', 'mon@cookie.com', '111-111-1111', 'password', '2020-08-04 12:37:24.670238', '2020-08-04 12:37:24.670248');
INSERT INTO "main"."users" ("user_id", "username", "email_address", "phone", "password", "created_on", "updated_on") VALUES ('2', 'cakeeater', 'cakeeater@cake.com', '222-222-2222', 'password', '2020-08-04 12:37:24.670250', '2020-08-04 12:37:24.670251');
INSERT INTO "main"."users" ("user_id", "username", "email_address", "phone", "password", "created_on", "updated_on") VALUES ('3', 'pieguy', 'guy@pie.com', '333-333-3333', 'password', '2020-08-04 12:37:24.670253', '2020-08-04 12:37:24.670254');
"""


ins = insert(orders).values(user_id=1, order_id=1)
result = connection.execute(ins)

ins = insert(orders).values(user_id=2, order_id=2)
result = connection.execute(ins)
"""
INSERT INTO "main"."orders" ("order_id", "user_id", "shipped") VALUES ('1', '1', '0');
INSERT INTO "main"."orders" ("order_id", "user_id", "shipped") VALUES ('2', '2', '0');
"""

ins = insert(line_items)
order_items = [
    {
        'order_id': 1,
        'cookie_id': 1,
        'quantity': 2,
        'extended_cost': 1.00
    },
    {
        'order_id': 1,
        'cookie_id': 3,
        'quantity': 12,
        'extended_cost': 3.00
    }
]
result = connection.execute(ins, order_items)

ins = insert(line_items)
order_items = [
    {
        'order_id': 2,
        'cookie_id': 1,
        'quantity': 24,
        'extended_cost': 12.00
    },
    {
        'order_id': 2,
        'cookie_id': 4,
        'quantity': 6,
        'extended_cost': 6.00
    }
]
result = connection.execute(ins, order_items)
"""
INSERT INTO "main"."line_items" ("line_items_id", "order_id", "cookie_id", "quantity", "extended_cost") VALUES ('1', '1', '1', '2', '1');
INSERT INTO "main"."line_items" ("line_items_id", "order_id", "cookie_id", "quantity", "extended_cost") VALUES ('2', '1', '3', '12', '3');
INSERT INTO "main"."line_items" ("line_items_id", "order_id", "cookie_id", "quantity", "extended_cost") VALUES ('3', '2', '1', '24', '12');
INSERT INTO "main"."line_items" ("line_items_id", "order_id", "cookie_id", "quantity", "extended_cost") VALUES ('4', '2', '4', '6', '6');
"""


columns = [
    orders.c.order_id,
    users.c.username,
    users.c.phone,
    cookies.c.cookie_name,
    line_items.c.quantity,
    line_items.c.extended_cost]
cookiemon_orders = select(columns)
cookiemon_orders = cookiemon_orders.select_from(users.join(orders).join(line_items).join(cookies)).where(users.c.username == 'cookiemon')
# print(str(cookiemon_orders))
# print(cookiemon_orders.compile().params)
result = connection.execute(cookiemon_orders).fetchall()
for row in result:
    # print(row)
    pass

"""
SELECT orders.order_id, users.username, users.phone, cookies.cookie_name, line_items.quantity, line_items.extended_cost
FROM users
JOIN orders ON users.user_id = orders.user_id
JOIN line_items ON orders.order_id = line_items.order_id
JOIN cookies ON cookies.cookie_id = line_items.cookie_id
WHERE users.username = :username_1
{'username_1': 'cookiemon'}
(1, 'cookiemon', '111-111-1111', 'chocolate chip', 2, Decimal('1.00'))
(1, 'cookiemon', '111-111-1111', 'dark chocolate chip', 12, Decimal('3.00'))
"""

columns = [users.c.username, orders.c.order_id]
all_orders = select(columns)
all_orders = all_orders.select_from(users.outerjoin(orders))
# print(str(all_orders))
result = connection.execute(all_orders).fetchall()
for row in result:
    # print(row)
    pass

"""
SELECT users.username, orders.order_id
FROM users LEFT OUTER JOIN orders ON users.user_id = orders.user_id
('cakeeater', 2)
('cookiemon', 1)
('pieguy', None)
"""

columns = [users.c.username, func.count(orders.c.order_id)]
all_orders = select(columns)
all_orders = all_orders.select_from(users.outerjoin(orders)).group_by(users.c.username)
# print(str(all_orders))
result = connection.execute(all_orders).fetchall()
for row in result:
    # print(row)
    pass

"""
SELECT users.username, count(orders.order_id) AS count_1
FROM users LEFT OUTER JOIN orders ON users.user_id = orders.user_id GROUP BY users.username
('cakeeater', 1)
('cookiemon', 1)
('pieguy', 0)
"""

def get_orders_by_customer(cust_name):
    columns = [orders.c.order_id, users.c.username, users.c.phone, cookies.c.cookie_name, line_items.c.quantity, line_items.c.extended_cost]
    cust_orders = select(columns)
    cust_orders = cust_orders.select_from(users.join(orders).join(line_items).join(cookies)).where(users.c.username == cust_name)
    print(str(cust_orders))
    print(cust_orders.compile().params)
    result = connection.execute(cust_orders).fetchall()
    return result

print(get_orders_by_customer('cakeeater'))
"""
SELECT orders.order_id, users.username, users.phone, cookies.cookie_name, line_items.quantity, line_items.extended_cost
FROM users
JOIN orders ON users.user_id = orders.user_id
JOIN line_items ON orders.order_id = line_items.order_id
JOIN cookies ON cookies.cookie_id = line_items.cookie_id
WHERE users.username = :username_1
{'username_1': 'cakeeater'}
[(2, 'cakeeater', '222-222-2222', 'chocolate chip', 24, Decimal('12.00')), (2, 'cakeeater', '222-222-2222', 'peanut butter', 6, Decimal('6.00'))]
"""

def get_orders_by_customer(cust_name, shipped=None, details=False):
    columns = [orders.c.order_id, users.c.username, users.c.phone]
    joins = users.join(orders)
    if details:
        columns.extend([cookies.c.cookie_name,line_items.c.quantity, line_items.c.extended_cost])
        joins=joins.join(line_items).join(cookies)
    cust_orders = select(columns)
    cust_orders = cust_orders.select_from(joins).where(users.c.username == cust_name)
    if shipped is not None:
        cust_orders = cust_orders.where(orders.c.shipped == shipped)
    result = connection.execute(cust_orders).fetchall()
    return result

get_orders_by_customer('cakeeater')
get_orders_by_customer('cakeeater', details=True)
get_orders_by_customer('cakeeater', shipped=True)
get_orders_by_customer('cakeeater', shipped=False)
get_orders_by_customer('cakeeater', shipped=False, details=True)

result = connection.execute("select * from orders").fetchall()
print(result)

stmt = select([users]).where(text('username="cookiemon"'))
print(connection.execute(stmt).fetchall())