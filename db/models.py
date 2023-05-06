from sqlalchemy import Integer, String
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()


class Service(Base):
    __tablename__ = "services"
    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    tg_id: Mapped[int] = mapped_column(Integer())
    name: Mapped[str] = mapped_column(String(200))
    login: Mapped[str] = mapped_column(String(200))
    password: Mapped[str] = mapped_column(String(200))
