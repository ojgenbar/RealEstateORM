from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry

from orm_main import Base


class SpatialBase(Base):
    __abstract__ = True
    __table_args__ = {"schema": "spatial_data"}
    id = Column(Integer, primary_key=True)
    name = Column(String)
    geom = Column(Geometry(srid=32636))

    def __repr__(self):
        return "<Type '{}' (id='{}', name='{}')>".format(type(self).__name__, self.id, self.name)


class Metro(SpatialBase):
    __tablename__ = 'metro'


class Kad(SpatialBase):
    __tablename__ = 'kad'


class Park(SpatialBase):
    __tablename__ = 'parks'


class School(SpatialBase):
    __tablename__ = 'schools'


class Kindergarten(SpatialBase):
    __tablename__ = 'kindergartens'


__all__ = ['Kad', 'Kindergarten', 'Metro', 'Park', 'School']
