from datetime import datetime

from database.db import Base

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime


class HeaderModel(Base):

    __tablename__ = "t_header"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(29), nullable=False, unique=True)
    date = Column(String(8), nullable=False)
    batch_name = Column(String(8), nullable=False)
    registers = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())


class ItemModel(Base):

    __tablename__ = "t_item"
    id = Column(Integer, primary_key=True, autoincrement=True)
    header_id = Column(Integer, ForeignKey("t_header.id"), nullable=False)
    line = Column(Integer, nullable=False)
    batch_number = Column(Integer, nullable=False)
    credit_card_number = Column(String(19), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())
