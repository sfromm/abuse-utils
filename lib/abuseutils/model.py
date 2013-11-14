# Written by Stephen Fromm <stephenf@nero.net>
# (C) 2013 University of Oregon

# This file is part of abuse-utils
#
# abuse-utils is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# abuse-utils is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with abuse-utils.  If not, see <http://www.gnu.org/licenses/>.

import datetime
import logging

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.types import TypeDecorator, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Incident(Base):
    __tablename__ = 'incident'

    id = Column(Integer, primary_key=True)
    src_ip      = Column(String) # FIXME
    timestamp   = Column(DateTime, default=datetime.datetime.now)
    reporter_id = Column(Integer, ForeignKey('reporter.id'))
    incident_type_id     = Column(Integer, ForeignKey('incident_type.id'))

    def __init__(self, src_ip, timestamp):
        self.src_ip = src_ip
        self.timestamp = timestamp

    def __repr__(self):
        return "<Incident<'%s', '%s'>" % (self.src_ip, self.timestamp)

class IncidentType(Base):
    __tablename__ = 'incident_type'

    id          = Column(Integer, primary_key=True)
    name        = Column(String)
    description = Column(String)

    def __init__(self, name, description=None):
        self.name = name
        if description is not None:
            self.description = description

    def __repr__(self):
        return "<IncidentType<'%s'>" % (self.name)

class Reporter(Base):
    __tablename__ = 'reporter'

    id = Column(Integer, primary_key=True)
    name  = Column(String)
    email = Column(String)
    phone = Column(String)

    def __init__(self, name, email, phone=None):
        self.name = name
        self.email = email
        if phone is not None:
            self.phone = phone

    def __repr__(self):
        return "<Reporter<'%s'>" % (self.name)
