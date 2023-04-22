from sqlalchemy import Column, Integer, String, SmallInteger
from sqlalchemy.orm import relationship

from cakeshop.db.base_class import Base


class Cake(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30))
    comment = Column(String(200))
    imageUrl = Column(String(256))
    yumFactor = Column(SmallInteger)
