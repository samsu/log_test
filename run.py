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
from faas import context


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

LOG = log.getLogger(__name__)


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


if __name__ == '__main__':
    context.RequestContext(user_id='6ce90b4d', customer_id='d6134462',
                           request_id='req-a6b9360e')
    setup_logging()
