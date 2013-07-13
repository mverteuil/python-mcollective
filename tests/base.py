# coding: utf-8
import os

import jinja2

ROOT = os.path.abspath(os.path.join(__file__, '..'))
DEFAULT_CTXT = {
    'topicprefix': 'topic',
    'collectives': ['mcollective', 'sub1', 'sub2'],
    'main_collective': 'mcollective',
    'libdir': '{root}/integration/vendor/plugins'.format(root=ROOT),
    'logfile': '{root}/mcollective.log'.format(root=ROOT),
    'loglevel': 'debug',
    'daemonize': 0,
    'identity': 'mco1',
    'securityprovider': 'ssl',
    'plugin.ssl_server_public': 'mcserver-public.pem',
    'plugin.ssl_client_private': '{root}/fixtures/testkey-private.pem'.format(
        root=ROOT),
    'plugin.ssl_client_public': '{root}/fixtures/testkey-public.pem'.format(
        root=ROOT),
    'plugin.ssl_serializer': 'yaml',
    'connector': 'activemq',
    'plugin.activemq.pool.size': '1',
    'plugin.activemq.pool.1.host': 'localhost',
    'plugin.activemq.pool.1.port': '6163',
    'plugin.activemq.pool.1.user': 'mcollective',
    'plugin.activemq.pool.1.password': 'secret',
    'plugin.activemq.pool.1.ssl': 'false',
}
TEST_CFG = os.path.join(ROOT, 'server.cfg')


def get_template(name, package=__package__):
    env = jinja2.Environment(loader=jinja2.PackageLoader(package, 'templates'))
    return env.get_template(name)


def configfile(ctxt=None):
    if not ctxt:
        ctxt = DEFAULT_CTXT
    with open(TEST_CFG, 'wt') as cfg:
        cfg.write(get_template('server.cfg.jinja').render({'config': ctxt}))
    return TEST_CFG
