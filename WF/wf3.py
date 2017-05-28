# -*- coding: UTF-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Numeric, Date
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
import datetime


Base = declarative_base()
engine = create_engine('postgresql+psycopg2://oj_gen:7FmDsD77@localhost/RealEstate', echo=True)
Base = declarative_base()


class District(Base):

    __tablename__ = 'district'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "<Type(name='%s')>" % self.name


class Address(Base):

    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    district_id = Column(Integer, ForeignKey('district.id'))
    ruAddress = Column(String)
    enAddress = Column(String)
    geom = Column(Geometry("POINT", srid=3395))
    building_type = Column(String)
    floors = Column(Integer)

    district = relationship("District", back_populates='addresses')

    def __repr__(self):
        return "<Type(enAddress='%s')>" % self.enAddress


class Flat(Base):

    __tablename__ = 'flat'
    id = Column(Integer, primary_key=True)
    address_id = Column(Integer, ForeignKey('address.id'))
    floor = Column(Integer)
    area = Column(Numeric(10, 3))
    kitchen_area = Column(String)
    living_area = Column(String)
    bathroom = Column(String)

    address = relationship("Address", back_populates='flats')

    def __repr__(self):
        return "<Type(address_id='%s', area='%s')>" % self.address_id, self.area


class Price_history(Base):

    __tablename__ = 'price_history'
    flat_id = Column(Integer, ForeignKey('flat.id'), primary_key=True)
    date = Column(Date,  primary_key=True)
    price = Column(Numeric(10, 3))
    _price_sqm = Column('price_sqm', Numeric(20, 15))

    flats = relationship("Flat", back_populates='prices')

    @hybrid_property
    def price_sqm(self):
        return self._price_sqm

    @price_sqm.setter
    def price_sqm(self, price_sqm):
        self._price_sqm = price_sqm

    def __repr__(self):
        return "<Type(flat_id='%s', area='%s', date='%s')>" % self.flat_id, self.price, self.date

District.addresses = relationship('Address', back_populates="district")
Address.flats = relationship('Flat', back_populates="address")
Flat.prices = relationship('Price_history', back_populates="flat")
# Price_history.flat = relationship('Flats',  order_by=Flats.id, back_populates="price")
# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)

dis = District(name=u'Адмиралтейский район')
dis.addresses = [Address(geom='SRID=3395; POINT(400000, 500000)', ruAddress=u'А я день рождения не буду справлять!')]
dis.addresses[0].flats = [Flat(area=89)]
dis.addresses[0][0].prices = [Price_history(date=datetime.datetime(2016, 05, 17), price=6541)]



# dis = District('Адмиралтейский район')
# dis.adres = Address(dis, )


# sup = Price_history(date=datetime.datetime(2016, 05, 17), price=6541)
# sup.flat = Flats(area=89)
# sup.flat.addr = Address(geom='SRID=3395; POINT(400000, 500000)', ruAddress=u'А я день рождения не буду справлять!')
# sup.flat.addr.distr = District(u'Адмиралтейский район')



# Base.metadata.drop_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

session.commit()

