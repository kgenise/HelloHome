# coding: utf-8
from sqlalchemy import CHAR, Column, ForeignKey, Integer, LargeBinary, String, text
from sqlalchemy.dialects.postgresql import MONEY
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Agent(Base):
    __tablename__ = 'agents'

    agent_id = Column(Integer, primary_key=True, server_default=text("nextval('agents_agent_id_seq'::regclass)"))
    first_name = Column(String(20))
    last_name = Column(String(20))
    company = Column(String(100))
    phone_number = Column(String(22))
    email_address = Column(String(100))


class Buyer(Base):
    __tablename__ = 'buyers'

    buyer_id = Column(Integer, primary_key=True, server_default=text("nextval('buyers_buyer_id_seq'::regclass)"))
    first_name = Column(String(20))
    last_name = Column(String(20))
    email_address = Column(String(100))


class Property(Base):
    __tablename__ = 'properties'

    listing_id = Column(Integer, primary_key=True, server_default=text("nextval('properties_listing_id_seq'::regclass)"))
    sale_type = Column(CHAR(4))
    property_type = Column(String(100))
    price = Column(MONEY)
    num_bed = Column(Integer)
    num_bath = Column(Integer)
    building_size = Column(Integer)
    land_size = Column(Integer)
    address = Column(String(100))
    image = Column(LargeBinary)
    agent_id = Column(ForeignKey('agents.agent_id', ondelete='CASCADE', onupdate='CASCADE', match='FULL'), nullable=False)

    agent = relationship('Agent')
