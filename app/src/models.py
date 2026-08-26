from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    price: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
