# Copyright 2017 BBVA
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Provides the sqlalchemy engine.

Dogpile.cache is used to create a cache layer for the engine.
"""

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
from dogpile.cache import make_region

from ..config import DATABASE_URI
from . import caching_query


class DeeptracyDBEngine:

    engine = None
    Session = None
    regions = {}  # dogpile cache regions.  A home base for cache configurations.

    def init_engine(self, db_uri=None):
        self.engine = sqlalchemy.create_engine(db_uri or DATABASE_URI)
        self.create_cache_regions()
        self.Session = sessionmaker(
            bind=self.engine,
            query_cls=caching_query.query_callable(self.regions)
        )

        if not database_exists(db.engine.url):
            try:
                create_database(db.engine.url)
                # reflect the engine into metadata object from models
                Base.metadata.reflect(bind=self.engine)
                Base.metadata.create_all(bind=self.engine)
            except Exception as e:
                print(e)
                pass

    def create_cache_regions(self):
        # configure the "default" cache region.
        self.regions['default'] = make_region(
            key_mangler=caching_query.md5_key_mangler
        ).configure(
            'dogpile.cache.memory_pickle',
            expiration_time=3600
        )

    @contextmanager
    def session_scope(self, commit=True):
        session = self.Session()
        try:
            yield session
            if commit:
                session.commit()
        except:  # noqa
            session.rollback()
            raise
        finally:
            session.close()


db = DeeptracyDBEngine()
Base = declarative_base()
