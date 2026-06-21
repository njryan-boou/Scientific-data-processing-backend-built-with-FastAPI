from sqlalchemy import Integer, String, Text, DateTime, Column
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from .database import Base


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    
    
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    
    password_hash = Column(String(128), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
