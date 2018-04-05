# Copyright 2017 Fortinet Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import sys
import logging

from oslo_config import cfg
from faas.conf import config
from log_test import log
from faas.common import constants as consts
from faas.version import version_info


CFG_ARGS = [
    '--config-file',
    '/etc/fas/fas.conf'
]

CFG_KWARGS = {}

config.init()

cfg.CONF(args=CFG_ARGS,
         project=consts.PRODUCT_NAME,
         version=version_info, **CFG_KWARGS)

CONF = config.CONF


def setup_logging():
    """Sets up the logging options for a log with supplied name."""
    # logging_context_format = ' '.join(consts.LOGGING_CONTEXT_FORMAT)
    # log.set_defaults(logging_context_format_string=logging_context_format)
    log.setup(CONF, consts.PRODUCT_NAME)
    logging.captureWarnings(True)
    LOG.info("Logging enabled!")
    LOG.info("{prog} version {version}".format(prog=sys.argv[0],
                                               version=version_info))
    LOG.debug("command line: %s", " ".join(sys.argv))


_loggers = {}


def get_loggers():
    """Return a copy of the oslo loggers dictionary."""
    return _loggers.copy()


def getLogger(name=None, project='unknown', version='unknown'):
    """Build a logger with the given name.

    :param name: The name for the logger. This is usually the module
                 name, ``__name__``.
    :type name: string
    :param project: The name of the project, to be injected into log
                    messages. For example, ``'nova'``.
    :type project: string
    :param version: The version of the project, to be injected into log
                    messages. For example, ``'2014.2'``.
    :type version: string
    """
    # NOTE(dhellmann): To maintain backwards compatibility with the
    # old oslo namespace package logger configurations, and to make it
    # possible to control all oslo logging with one logger node, we
    # replace "oslo_" with "oslo." so that modules under the new
    # non-namespaced packages get loggers as though they are.
    if name and name.startswith('oslo_'):
        name = 'oslo.' + name[5:]
    if name not in _loggers:
        _loggers[name] = log.KeywordArgumentAdapter(logging.getLogger(name),
                                                    {'project': project,
                                                    'version': version})
    return _loggers[name]


LOG = getLogger(__name__)

if __name__ == '__main__':
    setup_logging()
