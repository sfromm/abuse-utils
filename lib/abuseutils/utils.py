# Written by Stephen Fromm <sfromm@gmail.com>
# (C) 2013 University of Oregon

# This file is part of ansible-report
#
# ansible-report is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ansible-report is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ansible-report.  If not, see <http://www.gnu.org/licenses/>.

import os
import yaml
import json
import abuseutils.constants as C

def parse_json(data):
    ''' convert json string to data structure '''
    return json.loads(data)

def parse_json_from_file(path):
    ''' convert json file to data structure '''
    try:
        data = file(path).read()
        return parse_json(data)
    except IOError:
        logging.error("file not found: %s" % path)
        return None
    except Exception:
        logging.error("failed to parse json from file %s", path)
        return None

def parse_yaml(data):
    ''' convert yaml string to data structure '''
    return yaml.load(data)

def parse_yaml_from_file(path):
    ''' convert yaml file to data structure '''
    try:
        data = file(path).read()
        return parse_yaml(data)
    except IOError:
        logging.error("file not found: %s" % path)
        return None
    except yaml.YAMLError, e:
        if hasattr(e, 'problem_mark'):
            mark = e.problem_mark
            msg = "Problem loading file %s: line %s, column %s" % (path, mark.line + 1, mark.column + 1)
        else:
            msg = "Could not parse YAML in %s" % path
        logging.error(msg)
        return None

def setup_logging(verbose, debug, use_syslog):
    ''' setup logging bits '''
    loglevel = 'WARN'
    if verbose:
        loglevel = 'INFO'
    if debug:
        loglevel = 'DEBUG'
    numlevel = getattr(logging, loglevel.upper(), None)
    if not isinstance(numlevel, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logargs = {}
    logargs['level'] = numlevel
    logargs['datefmt'] = '%FT%T'
    logargs['format'] = C.DEFAULT_LOG_FORMAT
    logging.basicConfig(**logargs)
    if use_syslog:
        # remove default logger and add syslog handler
        logger = logging.getLogger()
        if 'flush' in dir(logger):
            logger.flush()

        filelogger = logger.handlers[0]

        syslog = None
        try:
            syslog = logging.handlers.SysLogHandler(address='/dev/log')
            formatter = logging.Formatter('%(filename)s: %(message)s')
            syslog.setFormatter(formatter)
            logger.addHandler(syslog)
        except socket.error:
            if syslog is not None:
                syslog.close()
        else:
            logger.removeHandler(filelogger)
            if isinstance(filelogger, logging.FileHandler):
                filelogger.close()
