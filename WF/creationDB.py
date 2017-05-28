# -*- coding: UTF-8 -*-

from sqlalchemy.orm import relationship

from geoalchemy2 import Geometry

from ORMBase import District
from ORMBase import Address
from ORMBase import Flat
from ORMBase import Price_history
from ORMBase import Base
from ORMBase import engine


# class DBCreator:
#
#     def __init__(self):
#
#         self.host = 'localhost'
#         self.port = '5432'
#         self.user = 'postgres'
#         self.password = ''
#
# Base = declarative_base()
# engine = create_engine('postgresql+psycopg2://oj_gen:7FmDsD77@localhost/RealEstate', echo=True)
# Base = declarative_base()

# Address.distr = relationship('District',  order_by=District.id, back_populates="address")
# Flats.addr = relationship('Address',  order_by=Address.id, back_populates="flats")
# Price_history.flats = relationship('Flats',  order_by=Flat.id, back_populates="price")

# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)