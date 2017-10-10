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

"""Manager for Plugin objects"""

from deeptracy_core.dal.plugin.model import Plugin
from sqlalchemy.orm import Session


def deactivate_all_plugins(session: Session):
    """Deactivate (set active=false) for all plugins in the database

    :param session: (Session) Database session
    """
    session.query(Plugin).update({Plugin.active: False})


def add_or_activate_plugin(name: str, lang: str, session: Session) -> Plugin:
    """If a plugin does not exists, create it (a plugin is identified by its name and lang.
    If the plugin exists, activate it (set active = True)

    :param name: (str) plugin name
    :param lang: (str) plugin lang
    :param session: (Session) Database session

    :rtype Plugin:
    """
    query = session.query(Plugin).filter((Plugin.name == name) & (Plugin.lang == lang))
    plugin = query.first()
    if plugin is not None:
        plugin.active = True
    else:
        plugin = Plugin(name=name, lang=lang, active=True)

    session.add(plugin)
    return plugin


def get_plugins_for_lang(lang: str, session: Session):
    """Returns a list of active Plugins for a given lang

    :param lang: (str) plugin lang
    :param session: (Session) Database session

    :rtype list(Plugin):
    """
    query = session.query(Plugin)\
        .filter(Plugin.lang == lang)\
        .filter(Plugin.active == True)
    return query.all()


__all__ = ('deactivate_all_plugins', 'add_or_activate_plugin', 'get_plugins_for_lang')
