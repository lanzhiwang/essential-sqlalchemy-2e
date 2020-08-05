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

class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('parent.id'))
    parent = relationship("Parent", backref="children")


Base.metadata.create_all(engine)

p = Parent()
c1 = Child()
c2 = Child()
print(dir(p))  # ['children', 'id', 'metadata']
print(dir(c1))  # ['id', 'metadata', 'parent', 'parent_id']

p.children.append(c1)
c2.parent = p
session.add(p)
session.add(c1)
session.add(c2)
session.commit()
