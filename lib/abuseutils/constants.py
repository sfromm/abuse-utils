# Written by Stephen Fromm <stephenf@nero.net>
# (C) 2013 University of Oregon
#
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

import os
import sys
import datetime
import ConfigParser

def get_config_value(p, section, key, env_var, default):
    ''' return configuration variable '''
    if env_var is not None:
        value = os.environ.get(env_var, None)
        if value is not None:
            return value
    if p is not None:
        try:
            return p.get(section, key)
        except:
            return default
    return default

def load_config_file():
    cfg = ConfigParser.ConfigParser()
    found = False
    paths = [
            os.path.expanduser(os.environ.get('ABUSEUTILS_CONFIG', '~/.abuseutils.cfg')),
            os.path.join(os.getcwd(), 'abuseutils.cfg'),
            '/etc/abuseutils/abuseutils.cfg'
            ]
    for path in paths:
        if os.path.exists(path):
            cfg.read(path)
            found = True
            break
    if not found:
        cfg = None
    return cfg

cfg = load_config_file()
SECTION = 'default'

DEFAULT_DB_URI = get_config_value(cfg, SECTION, 'sqlalchemy.url', None, 'sqlite://')
DEFAULT_LOG_FORMAT = get_config_value(
        cfg, SECTION, 'log_format', 'ABUSEUTILS_LOG_FORMAT', '%(asctime)s: [%(levelname)s] %(message)s'
        )
DEFAULT_SMTP_SERVER = get_config_value(
        cfg, SECTION, 'smtp_server', 'ABUSEUTILS_SMTP_SERVER', 'localhost'
        )
DEFAULT_SPOOL_DIR = get_config_value(
        cfg, SECTION, 'spooldir', 'ABUSEUTILS_SPOOL_DIR', '/var/spool/abuseutils'
        )
