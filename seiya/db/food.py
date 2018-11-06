from sqlalchemy import Column, String, Integer, Float

from seiya.db.base import Base


class FoodModel(Base):
    """大众点评美食 Model

    """
    __tablename__ = 'food'
    id = Column(Integer, primary_key=True)
    label = Column(String(128))
    name = Column(String(64))
    score = Column(Float)
    reviewNum = Column(Integer)
    agvExp = Column(Float)
    addr = Column(String(64))
    fenlei = Column(String(32))
    quan = Column(String(32))
    kouwei = Column(Float)
    huanjin = Column(Float)
    fuwu = Column(Float)
