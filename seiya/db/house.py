from sqlalchemy import Column, String, Integer, Float

from seiya.db.base import Base


class HouseModel(Base):
    """租房 Model

    """
    __tablename__ = 'house'

    id = Column(Integer, primary_key=True)
    area = Column(String(64))
    name = Column(String(128))
    xiaoqu = Column(String(64))
    huxing = Column(String(32))
    mianji = Column(Float)
    chaoxiang = Column(String(16))
    quan = Column(String(32))
    louceng = Column(String(16))
    years = Column(String(16))
    labels = Column(String(128))
    price = Column(Integer)
