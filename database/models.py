from typing import List

from sqlalchemy import Integer, Column, DateTime, func, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.settings import Base


class Request(Base):
    __tablename__ = "requests"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_chat_id: Mapped[int] = mapped_column(Integer)
    command: Mapped[str] = mapped_column(String(20))
    hotels: Mapped[List["Hotel"]] = relationship(
        "Hotel",
        back_populates="request",
        lazy="joined",
        cascade="all, delete",
    )
    time_created = Column(DateTime(timezone=True), server_default=func.now())


class Hotel(Base):
    __tablename__ = "hotels"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    address: Mapped[str] = mapped_column(String(300))
    hotel_name: Mapped[str] = mapped_column(String(300))
    price: Mapped[float] = mapped_column(Float)
    request_id: Mapped[int] = mapped_column(ForeignKey("requests.id"), index=True)
    request: Mapped["Request"] = relationship(back_populates="hotels")
    images: Mapped[List["Image"]] = relationship(
        "Image", back_populates="image", lazy="joined", cascade="all, delete"
    )


class Image(Base):
    __tablename__ = "images"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    image_url: Mapped[str] = mapped_column(String(length=200))
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"), index=True)
    hotel: Mapped["Hotel"] = relationship(back_populates="images")
