from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, desc
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime

engine = create_engine('postgresql://ubuntu:thinkful@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Float

class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)
    
    #Item to User relationship
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("Users", backref="items")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)

class Bid(Base):
    __tablename__ = "bid"
    
    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)
    
    # Item to Bid relationship
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    item = relationship("Item", backref="bids")
    
    # Bid to User relationship
    bidder_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    bidder = relationship("User", backref="bids")

Base.metadata.create_all(engine)

if __name__ == '__main__':
    peter = User(username="pgriffin", password="hyahya")
    chris = User(username="cgriffin", password="cgriffin")
    luis = User(username="lgriffin", password="whatarush")
    meg = User(username="mgriffin", password="imbeautiful")
    
    baseball = Item(name="KGJ's baseball", 
                    description="Ken Griffey Jr's Signed Baseball",
                    owner=meg)
    
    bids = [
        Bid(price=100.0, bidder=chris, item=baseball),
        Bid(price=150.0, bidder=luis, item=baseball),
        Bid(price=250.0, bidder=peter, item=baseball),
        Bid(price=300.0, bidder=luis, item=baseball),
        Bid(price=500.0, bidder=peter, item=baseball)
        ]
    
    session.add_all([peter, chris, luis, meg, baseball] + bids)
    session.commit()
    
    highest_bid = session.query(Bid).order_by(desc(Bid.price)).first()
    
    print("{} bought it for {}").format(highest_bid.bidder.username, highest_bid.price)