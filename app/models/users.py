from sqlalchemy import Boolean, Column, ForeignKey, String, Table
from sqlalchemy.orm import relationship

from app.db.base_class import Base


followingTable = Table(
    "followers",
    Base.metadata,
    Column("uid", ForeignKey("users.uid"), primary_key=True),
    Column("following_uid", ForeignKey("users.uid"), primary_key=True),
)


class User(Base):
    __tablename__ = 'users'

    uid = Column(String, primary_key=True, index=True)
    email = Column(String, unique=False, index=True)
    name = Column(String, unique=False)
    disabled = Column(Boolean, default=False)
    federated = Column(Boolean, default=False)
    admin = Column(Boolean, default=False)
    subscription = Column(String, unique=False, default="Regular")
    photo_url = Column(String, unique=False)
    following = relationship(
        "User",
        secondary=followingTable,
        primaryjoin=uid == followingTable.c.uid,
        secondaryjoin=uid == followingTable.c.following_uid,
        backref="followers")
    genres = Column(String, unique=False)
