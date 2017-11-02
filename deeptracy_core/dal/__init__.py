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

"""Data Access Layer package for Deeptracy.

 This package contains objects and methods related with the database access. It provides models and managers as well
 as a DeeptracyDBEngine to manage sessions and the database engine.

 It uses SQLAlchemy as the connection provider and provides a context manager to be used in order to provide sessions
 and metadata to interact with the db engine.

 Models:
    Models are objects that represents tables in the database schema.

    Project: Projects are the higher elements in the schema. They have one repository (which has an UNIQUE constrain)
    Plugin: Plugins are analyzers. Each plugin can have multiple languages
    Scans: Every project can have many scans, and every scan is performed against the project repository. Each scan
     is tied to a language.
    ScanAnalysis: Every scan may have many analysis. Each analysis is tied to a plugin.
    ScanAnalysisVulnerability: Every ScanAnalysis may generate vulnerabilities detected during the analysis.
    ScanVulnerability: When every analysis for a scan is done, all the vulnerabilities are merged into this table.

 Managers:
    Managers are methods to interact with models and the database. Methods in managers accepts a sqlalchemy.orm.Session
    object that is used to interact with the engine. Manager methods do not interact with the session (they don't
    commit, rollback or close the session), they just query the database through it and and objects, expecting someone
    else to perform the commit, or rollback when needed.

 DeeptracyDBEngine:
    Main object to interact with the database, it provides the session management, a context manager to facilitate
    interacting with the session, and a method to initialize the engine, create the database and tables if it doesn't
    exist and create.
"""

from .project.model import Project
from .scan.model import Scan
from .plugin.model import Plugin
from .scan_dep.model import ScanDep
from .scan_analysis.model import ScanAnalysis
from .models import ScanAnalysisVulnerability, ScanVulnerability
from .plugin_results import *
