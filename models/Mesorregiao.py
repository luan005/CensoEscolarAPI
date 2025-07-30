from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from helpers.database import db

if TYPE_CHECKING:
    from models.UF import UF
    from models.Microrregiao import Microrregiao
    from models.Municipio import Municipio

class Mesorregiao(db.Model):
    __tablename__ = "tb_mesorregiao"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str]
    uf_id: Mapped[int] = mapped_column(ForeignKey("tb_uf.id"))

    uf_nome: Mapped[str]
    uf_sigla: Mapped[str]
    regiao_id: Mapped[int]
    regiao_nome: Mapped[str]
    regiao_sigla: Mapped[str]

    uf: Mapped[UF] = relationship("UF", back_populates="mesorregioes")
    microrregioes: Mapped[list[Microrregiao]] = relationship("Microrregiao", back_populates="mesorregiao")
    municipios: Mapped[list[Municipio]] = relationship("Municipio", back_populates="mesorregiao")
