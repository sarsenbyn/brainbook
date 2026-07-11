from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Text
from config.database.database import Base
from pgvector.sqlalchemy import Vector
import numpy as np

class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[list[float]] = mapped_column(Vector(768))
    page_number: Mapped[int] = mapped_column(Integer, nullable=False)