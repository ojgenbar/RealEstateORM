from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Numeric, Date, Enum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
import enum


Base = declarative_base()

# noinspection PyArgumentList
MaterialTypeEnum = enum.Enum('MaterialTypeEnum', 'brick monolith panel block wood stalin monolithBrick old')


class Address(Base):

    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    ru_address = Column(String)
    geom = Column(Geometry("POINT", srid=4326))
    material_type = Column(Enum(MaterialTypeEnum))
    floors = Column(Integer)
    cian_id = Column(Integer)
    year = Column(Integer)

    flats = relationship('Flat', back_populates="address")

    def __repr__(self):
        return "<Type 'Address' (id='{}')>".format(self.id)


class AddressView(Base):
    __tablename__ = 'addresses_view'
    id = Column(Integer, primary_key=True)
    ru_address = Column(String)
    geom = Column(Geometry("POINT", srid=4326))
    material_type = Column(Enum(MaterialTypeEnum))
    floors = Column(Integer)
    cian_id = Column(Integer)
    year = Column(Integer)

    address_id = Column(Integer, nullable=False)
    parks = Column(Integer, nullable=False)
    kad = Column(Integer, nullable=False)
    metro = Column(Integer, nullable=False)
    school = Column(Integer, nullable=False)
    kindergarten = Column(Integer, nullable=False)

    def __repr__(self):
        return "<Type 'AddressView' (id='{}')>".format(self.id)


class Flat(Base):

    __tablename__ = 'flats'
    id = Column(Integer, primary_key=True)
    address_id = Column(Integer, ForeignKey('addresses.id'))
    qrooms = Column(Integer)
    floor = Column(Integer)
    area = Column(Numeric)
    kitchen_area = Column(Numeric)
    living_area = Column(Numeric)
    separate_wc_count = Column(Integer)
    combined_wc_count = Column(Integer)
    description = Column(String)
    cian_id = Column(Integer, unique=True, nullable=False)
    link = Column(String)

    address = relationship("Address", back_populates='flats')
    prices = relationship('PriceHistory', back_populates="flat")

    def __repr__(self):
        return "<Type 'Flat' (address_id='{}', area='{}')>".format(self.address_id, self.area)


class PriceHistory(Base):

    __tablename__ = 'price_history'
    flat_id = Column(Integer, ForeignKey('flats.id'), primary_key=True)
    observe_date = Column(Date,  primary_key=True)
    price = Column(Numeric)

    flat = relationship("Flat", back_populates='prices')

    def __repr__(self):
        data = (self.flat_id, self.price, self.observe_date)
        return "<Type 'PriceHistory' (flat_id='{}', price='{}', date='{}')>".format(*data)


__all__ = ['Base', 'Address', 'AddressView', 'Flat', 'PriceHistory', 'MaterialTypeEnum']
