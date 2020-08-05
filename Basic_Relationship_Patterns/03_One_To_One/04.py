"""One To Many"""

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
CREATE TABLE parent (
	id INTEGER NOT NULL,
	PRIMARY KEY (id)
)

CREATE TABLE child (
	id INTEGER NOT NULL,
	parent_id INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(parent_id) REFERENCES parent (id)
)
"""

class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    child = relationship("Child", backref="parent", uselist=False)

class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('parent.id'))


Base.metadata.create_all(engine)

p1 = Parent()
p2 = Parent()
c1 = Child()
c2 = Child()
print(dir(p1))  # ['child', 'id', 'metadata']
print(dir(c1))  # ['id', 'metadata', 'parent', 'parent_id']

p1.child = c1
c2.parent = p2
session.add(p1)
session.add(p2)
session.add(c1)
session.add(c2)
session.commit()
