from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///cookies.db')
Session = sessionmaker(bind=engine)

session = Session()

"""
CREATE TABLE "left" (
	id INTEGER NOT NULL,
	PRIMARY KEY (id)
)

CREATE TABLE "right" (
	id INTEGER NOT NULL,
	PRIMARY KEY (id)
)

CREATE TABLE association (
	left_id INTEGER,
	right_id INTEGER,
	FOREIGN KEY(left_id) REFERENCES "left" (id),
	FOREIGN KEY(right_id) REFERENCES "right" (id)
)

"""

association_table = Table(
    'association',
    Base.metadata,
    Column('left_id', Integer, ForeignKey('left.id')),
    Column('right_id', Integer, ForeignKey('right.id'))
)

class Parent(Base):
    __tablename__ = 'left'
    id = Column(Integer, primary_key=True)
    children = relationship("Child", secondary=association_table, backref="parents")

class Child(Base):
    __tablename__ = 'right'
    id = Column(Integer, primary_key=True)


Base.metadata.create_all(engine)

p1 = Parent()
p2 = Parent()
c1 = Child()
c2 = Child()
print(dir(p1))  # ['children', 'id', 'metadata']
print(dir(c1))  # ['id', 'metadata', 'parents']

p1.children.append(c1)
p1.children.append(c2)

# p2.children.append(c1)
c1.parents.append(p2)
# p2.children.append(c2)
c2.parents.append(p2)

session.add(p1)
session.add(p2)
session.add(c1)
session.add(c2)
session.commit()
