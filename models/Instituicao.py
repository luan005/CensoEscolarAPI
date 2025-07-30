from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from helpers.database import db

if TYPE_CHECKING:
    from models.Municipio import Municipio

class Instituicao(db.Model):
    __tablename__ = "tb_instituicao"

    id: Mapped[int] = mapped_column(primary_key=True)
    nu_ano_censo: Mapped[int]
    no_regiao: Mapped[str]
    sg_uf: Mapped[str]
    no_municipio: Mapped[str]
    no_mesorregiao: Mapped[str]
    no_microrregiao: Mapped[str]
    co_entidade: Mapped[str]
    qt_mat_bas: Mapped[str]
    co_regiao: Mapped[str]
    co_uf: Mapped[str]

    co_municipio: Mapped[int] = mapped_column(ForeignKey("tb_municipio.id"))
    co_microrregiao: Mapped[str]
    co_mesorregiao: Mapped[str]

    municipio: Mapped[Municipio] = relationship("Municipio", back_populates="instituicoes")
