from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from helpers.database import db

if TYPE_CHECKING:
    from models.Mesorregiao import Mesorregiao
    from models.Microrregiao import Microrregiao
    from models.Municipio import Municipio
    from models.Instituicao import Instituicao

class UF(db.Model):
    __tablename__ = "tb_uf"

    id: Mapped[int] = mapped_column(primary_key=True)
    sigla: Mapped[str]
    nome: Mapped[str]
    regiao_id: Mapped[int]
    regiao_nome: Mapped[str]

    mesorregioes: Mapped[list[Mesorregiao]] = relationship("Mesorregiao", back_populates="uf")
    microrregioes: Mapped[list[Microrregiao]] = relationship("Microrregiao", back_populates="uf")
    municipios: Mapped[list[Municipio]] = relationship("Municipio", back_populates="uf")
