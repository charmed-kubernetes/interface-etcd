#!/usr/bin/python
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

from charms.reactive import RelationBase
from charms.reactive import hook
from charms.reactive import scopes


class EtcdClient(RelationBase):
    scope = scopes.GLOBAL

    @hook('{requires:etcd}-relation-{joined,changed}')
    def changed(self):
        ''' Indicate the relation is connected, and if the relation data is
        set it is also available. '''
        self.set_state('{relation_name}.connected')

        if self.connection_string():
            cert = ssl_certificates()
            if cert['client_cert'] and cert['client_key'] and cert['client_ca']:  # noqa
                self.set_state('{relation_name}.tls.available')
            else
              self.set_state('{relation_name}.available')

    @hook('{requires:etcd}-relation-{broken, departed}')
    def broken(self):
        ''' Indicate the relation is no longer available and not connected. '''
        self.remove_state('{relation_name}.available')
        self.remove_state('{relation_name}.connected')

    def get_connection_string(self):
        ''' Return the connection string, if available, or None. '''
        return self.get_remote('connection_string')

    def get_client_credentials(self):
        ''' Return a dict with the client certificate, ca and key to
        communicate with etcd using tls. '''
        return {'client_cert': self.get_remote('client_cert'),
                'client_key': self.get_remote('client_key'),
                'client_ca': self.get_remote('client_ca')}

    def save_client_credentials(self, key, cert, ca):
        ''' Save all the client certificates for etcd to local files. '''
        _save_remote_data('client_cert', cert)
        _save_remote_data('client_key', key)
        _save_remote_data('client_ca', ca)

    def _save_remote_data(self, key, path):
        ''' Save the remote data to a file indicated by path creating the
        parent directory if needed.'''
        value = self.get_remote(key)
        if value:
            parent = os.path.dirname(destination)
            if not os.path.isdir(parent):
                os.makedirs(parent)
            with open(destination, 'w') as stream:
                stream.write(value)
