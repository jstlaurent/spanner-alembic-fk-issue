from __future__ import annotations

from sqlalchemy import Column, ForeignKey, ForeignKeyConstraint, MetaData, PrimaryKeyConstraint, String, create_engine
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import declarative_base, relationship

from demo.config import settings

# SQLAlchemy standard initialization
engine = create_engine(settings.SPANNER_URL, pool_recycle=settings.SPANNER_SESSION_RECYCLE_AGE)
metadata = MetaData(bind=engine)
Base = declarative_base(bind=engine, metadata=metadata)


class EnvironmentMixin:

    @declared_attr
    def environment_id(self) -> Column[String]:
        return Column(String, ForeignKey('environment.id'), nullable=False)


class Environment(Base):
    __tablename__ = 'environment'

    id = Column(String, primary_key=True)


class A(Base, EnvironmentMixin):
    __tablename__ = 'a'

    id = Column(String, primary_key=True)
    content = Column(String, nullable=False)


class B(Base, EnvironmentMixin):
    __tablename__ = 'b'

    id = Column(String, primary_key=True)


class Link(Base, EnvironmentMixin):
    __tablename__ = 'link'
    __table_args__ = (
        # Enforce at DB-level that associated A and B must share the same Environment
        PrimaryKeyConstraint('environment_id', 'a_id', 'b_id', name='pk_test'),
        ForeignKeyConstraint(
            ['environment_id', 'a_id'],
            ['a.environment_id', 'a.id'],
            name='fk_1',
        ),
        ForeignKeyConstraint(
            ['environment_id', 'b_id'],
            ['b.environment_id', 'b.id'],
            name='fk_2',
        ),
    )

    a_id = Column(String, nullable=False)
    b_id = Column(String, nullable=False)

    a: A = relationship('A', foreign_keys=[a_id])
    b: B = relationship('B', foreign_keys=[b_id])
