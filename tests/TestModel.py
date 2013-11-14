#!/usr/bin/python

import sys
import pkg_resources

# fancy way to get the right version of sqlalchemy on rhel6
# in case pkg_resources has already been loaded.
def replace_dist(requirement):
    try:
        pkg_resources.require(requirement)
    except pkg_resources.VersionConflict:
        e = sys.exc_info()[1]
        dist = e.args[0]
        req = e.args[1]
        if dist.key == req.key and not dist.location.endswith('.egg'):
            del pkg_resources.working_set.by_key[dist.key]
            # We assume there is no need to adjust sys.path
            # and the associated pkg_resources.working_set.entries
            return pkg_resources.require(requirement)
replace_dist('SQLAlchemy >= 0.7')

import datetime
import unittest
import getpass
import os
import multiprocessing

ABUSEUTILS_CONFIG = os.path.join(os.path.dirname(__file__), 'abuseutils.cfg')
os.environ['ABUSEUTILS_CONFIG'] = ABUSEUTILS_CONFIG

import abuseutils
import abuseutils.constants as C
from abuseutils.manager import *
from abuseutils.model import *

INCIDENT = { 'ip': '10.1.2.3', 'time': datetime.datetime.now(), 'type': 'malware' }
REPORTER = {'name': 'Fake Inc', 'email': 'fake@example.net', 'phone': '555-1212'}

class TestDBInit(unittest.TestCase):
    def test_create_db(self):
        self.mgr = Manager(C.DEFAULT_DB_URI, debug=True)
        self.mgr.session.commit()
        self.assertEqual(self.mgr.session.connection().engine.name, 'sqlite')

class TestModel(unittest.TestCase):

    def setUp(self):
        self.mgr = Manager(C.DEFAULT_DB_URI, debug=True)

    def test_create_db(self):
        self.mgr = Manager(C.DEFAULT_DB_URI, debug=True)
        self.mgr.session.commit()
        self.assertEqual(self.mgr.session.connection().engine.name, 'sqlite')

    def test_incident(self):
        n = Incident(INCIDENT['ip'], INCIDENT['time'])
        self.mgr.session.add(n)
        r = self.mgr.session.commit()

    def test_incident_type(self):
        n = IncidentType(INCIDENT['type'], 'a longer description')
        self.mgr.session.add(n)
        self.mgr.session.commit()

    def test_reporter(self):
        n = Reporter(REPORTER['name'], REPORTER['email'], REPORTER['phone'])
        self.mgr.session.add(n)
        self.mgr.session.commit()

