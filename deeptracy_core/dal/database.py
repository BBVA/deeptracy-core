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

"""Provides the sqlalchemy engine."""
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from contextlib import contextmanager

from sqlalchemy.ext.declarative import declarative_base
from deeptracy_core.config import DATABASE_URI


class DeeptracyDBEngine:

    engine = None
    Session = None

    def init_engine(self, db_uri=None):
        self.engine = sqlalchemy.create_engine(db_uri or DATABASE_URI)
        self.Session = sessionmaker(bind=self.engine)

        if not database_exists(db.engine.url):
            try:
                create_database(db.engine.url)
                # reflect the engine into metadata object from models
                Base.metadata.reflect(bind=self.engine)
                Base.metadata.create_all(bind=self.engine)
            except Exception as e:
                print(e)
                pass

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
