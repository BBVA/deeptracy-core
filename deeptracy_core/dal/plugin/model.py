# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, Boolean

from deeptracy_core.utils import make_uuid
from deeptracy_core.dal.database import Base


class Plugin(Base):
    """SQLAlchemy Plugin model"""
    __tablename__ = 'plugin'

    id = Column(String, primary_key=True, default=make_uuid)
    name = Column(String)
    lang = Column(String)
    active = Column(Boolean)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'lang': self.lang,
            'active': self.active
        }
