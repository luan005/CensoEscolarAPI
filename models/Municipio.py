from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from helpers.database import db

if TYPE_CHECKING:
    from models.Mesorregiao import Mesorregiao
    from models.Microrregiao import Microrregiao
    from models.UF import UF
    from models.Instituicao import Instituicao

class Municipio(db.Model):
    __tablename__ = "tb_municipio"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str]

    microrregiao_id: Mapped[int] = mapped_column(ForeignKey("tb_microrregiao.id"))
    microrregiao_nome: Mapped[str]

    mesorregiao_id: Mapped[int] = mapped_column(ForeignKey("tb_mesorregiao.id"))
    mesorregiao_nome: Mapped[str]

    uf_id: Mapped[int] = mapped_column(ForeignKey("tb_uf.id"))
    uf_nome: Mapped[str]
    uf_sigla: Mapped[str]
    regiao_id: Mapped[int]
    regiao_nome: Mapped[str]
    regiao_sigla: Mapped[str]

    microrregiao: Mapped[Microrregiao] = relationship("Microrregiao", back_populates="municipios")
    mesorregiao: Mapped[Mesorregiao] = relationship("Mesorregiao", back_populates="municipios")
    uf: Mapped[UF] = relationship("UF", back_populates="municipios")

    instituicoes: Mapped[list[Instituicao]] = relationship("Instituicao", back_populates="municipio")
