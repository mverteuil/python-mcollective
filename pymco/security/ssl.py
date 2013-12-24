"""
:py:mod:`pymco.ssl`
-------------------
Contains SSL security provider plugin.
"""
from __future__ import print_function
import os

try:
    from Crypto.Signature import PKCS1_v1_5
    from Crypto.Hash import SHA
except ImportError:
    print('You need install pycrypto for using SSL security provider')

from . import none
from .. import utils


class SSLProvider(none.NoneProvider):
    """Provide SSL security provider plugin.

    See
    http://docs.puppetlabs.com/mcollective/reference/plugins/security_ssl.html
    for further information.
    """
    def __init__(self, config):
        super(SSLProvider, self).__init__(config=config)
        self._private_key = None
        self._server_public_key = None
        self._caller_id = None
        self._serializer = None

    def sign(self, message):
        """Implement :py:meth:`pymco.security.SecurityProvider.sign`."""
        message[':callerid'] = self.callerid
        message[':hash'] = self.get_hash(message)
        return message

    def get_hash(self, message):
        """Get the hash for the given message.

        Params:
            ``message``: A dict like object, usually a
            :py:class:`pymco.message.Message` instance.

        Returns:
            ``hash``: Message hash so the receiver can verify the message.
        """
        hashed_signature = SHA.new(message[':body'])
        signer = PKCS1_v1_5.new(self.private_key)
        hashed_signature = signer.sign(hashed_signature)
        return hashed_signature.encode('base64').replace('\n', '').strip()

    @property
    def callerid(self):
        """Property returning the MCollective SSL caller id.

        As MCollective docs states, the caller ID will be the name of public
        key filename, without the extension part.
        """
        if not self._caller_id:
            caller_id = os.path.basename(
                self.config['plugin.ssl_client_public']).split('.')[0]
            self._caller_id = 'cert={0}'.format(caller_id)

        return self._caller_id

    def _load_rsa_key(self, key, cache):
        if not cache:
            cache = self._server_public_key = utils.load_rsa_key(self.config[key])

        return cache

    @property
    def server_public_key(self):
        """Property returning the server public key after being loaded."""
        return self._load_rsa_key(key='plugin.ssl_server_public',
                                  cache=self._server_public_key)

    @property
    def private_key(self):
        """Property returning the private key after being loaded."""
        return self._load_rsa_key(key='plugin.ssl_client_private',
                                  cache=self._server_public_key)

    @property
    def serializer(self):
        """Property returning the serializer object.

        Serailzer object should be any subclass
        :py:class:`pymco.serializer.Serializer`, depending on configuration.
        However, right now, only YAML serialization can be supported,
        since the default serializer (Marshal) isn't portable.
        """
        if not self._serializer:
            self._serializer = self.config.get_serializer('plugin.ssl_serializer')

        return self._serializer
