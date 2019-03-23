# -*- coding: UTF-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Numeric, Date
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint
from geoalchemy2 import Geometry


Base = declarative_base()


class District(Base):

    __tablename__ = 'districts'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    addresses = relationship('Address', back_populates="district")

    def __repr__(self):
        return "<Type 'District' (id='{}', name='{}')>".format(self.id, self.name)


class Address(Base):

    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    district_id = Column(Integer, ForeignKey('districts.id'))
    ru_address = Column(String)
    en_address = Column(String, unique=True)
    geom = Column(Geometry("POINT", srid=4326))
    building_type = Column(String)
    floors = Column(Integer)

    district = relationship("District", back_populates='addresses')

    flats = relationship('Flat', back_populates="address")

    def __repr__(self):
        return "<Type 'Address' (id='{}', en_address='{}')>".format(self.id, self.en_address)


class Flat(Base):

    __tablename__ = 'flats'
    id = Column(Integer, primary_key=True)
    address_id = Column(Integer, ForeignKey('addresses.id'))
    qrooms = Column(Integer)
    floor = Column(Integer)
    area = Column(Numeric(10, 3))
    kitchen_area = Column(String)
    living_area = Column(String)
    bathroom = Column(String)
    abilities = Column(String)
    agency = Column(String)
    tel = Column(String)
    description = Column(String)
    bn_id = Column(Integer)
    ad_type = Column(Integer)
    link = Column(String, unique=True)

    __table_args__ = (UniqueConstraint('bn_id', 'ad_type', name='flats_bn_id_ad_type_key'), )

    address = relationship("Address", back_populates='flats')
    prices = relationship('PriceHistory', back_populates="flat")

    def __repr__(self):
        return "<Type 'Flat' (address_id='{}', area='{}')>".format(self.address_id, self.area)


class PriceHistory(Base):

    __tablename__ = 'price_history'
    flat_id = Column(Integer, ForeignKey('flats.id'), primary_key=True)
    observe_date = Column(Date,  primary_key=True)
    price = Column(Numeric(10, 3))
    _price_sqm = Column('price_sqm', Numeric(20, 15))

    flat = relationship("Flat", back_populates='prices')

    @hybrid_property
    def price_sqm(self):
        if self.price and self.flat.area:
            return float(self.price) / self.flat.area
        else:
            return None

    @price_sqm.setter
    def price_sqm(self, price_sqm):
        self._price_sqm = price_sqm

    def __repr__(self):
        data = (self.flat_id, self.price, self.observe_date)
        return "<Type 'PriceHistory' (flat_id='{}', price='{}', date='{}')>".format(*data)


__all__ = ['Base', 'Address', 'District', 'Flat', 'PriceHistory']