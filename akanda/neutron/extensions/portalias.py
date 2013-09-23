# Copyright 2012 New Dream Network, LLC (DreamHost)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# DreamHost Neutron Extensions
# @author: Murali Raju, New Dream Network, LLC (DreamHost)


from neutron.api import extensions
from neutron.api.v2 import attributes
from neutron.common import exceptions

from akanda.neutron.db import models_v2
from akanda.neutron.extensions import _authzbase


class PortaliasResource(_authzbase.ResourceDelegate):
    """This resource was created merely to satisfy
    Horizon's need to store alias names for ports. It is
    recommended to refactor this to perhaps just an alias
    resource that can contain aliases for multiple entities
    """
    model = models_v2.PortAlias
    resource_name = 'portalias'
    collection_name = 'portaliases'

    ATTRIBUTE_MAP = {
        'id': {'allow_post': False, 'allow_put': False,
               'validate': {'type:regex': attributes.UUID_PATTERN},
               'is_visible': True},
        'name': {'allow_post': True, 'allow_put': True,
                 'default': '', 'is_visible': True},
        'tenant_id': {'allow_post': True, 'allow_put': False,
                      'required_by_policy': True,
                      'is_visible': True},
        'protocol': {'allow_post': True, 'allow_put': True,
                     'required_by_policy': True,
                     'is_visible': True},
        'port': {'allow_post': True, 'allow_put': True,
                 'required_by_policy': True,
                 'is_visible': True},

    }

    def make_dict(self, portalias):
        """
        Convert a portalias model object to a dictionary.
        """
        res = {'id': portalias['id'],
               'name': portalias['name'],
               'protocol': portalias['protocol'],
               'port': portalias['port'],
               'tenant_id': portalias['tenant_id']}
        return res

    def before_delete(self, resource):
        if resource.port == 0:
            # FIXME(dhellmann): This will apply if the user creates
            # any of their own aliases with a zero port.
            raise exceptions.PolicyNotAuthorized(
                action='modification of system port aliases.'
            )
        return super(PortaliasResource, self).before_delete(resource)

    def update(self, context, resource, resource_dict):
        if resource.port == 0:
            # FIXME(dhellmann): This will apply if the user creates
            # any of their own aliases with a zero port.
            raise exceptions.PolicyNotAuthorized(
                action='deletion of system port aliases.'
            )
        return super(PortaliasResource, self).update(context,
                                                     resource,
                                                     resource_dict,
                                                     )

    def create(self, context, tenant_id, body):
        if body.get('port') == 0:
            # FIXME(dhellmann): This will apply if the user creates
            # any of their own aliases with a zero port.
            raise exceptions.PolicyNotAuthorized(
                action='creation of wildcard port aliases'
            )
        return super(PortaliasResource, self).create(context,
                                                     tenant_id,
                                                     body
                                                     )


_authzbase.register_quota('portalias', 'quota_portalias')


class Portalias(object):
    """
    """
    def get_name(self):
        return "portalias"

    def get_alias(self):
        return "dhportalias"

    def get_description(self):
        return "A portalias extension"

    def get_namespace(self):
        return 'http://docs.dreamcompute.com/api/ext/v1.0'

    def get_updated(self):
        return "2012-08-02T16:00:00-05:00"

    def get_resources(self):
        return [extensions.ResourceExtension(
            'dhportalias',
            _authzbase.create_extension(PortaliasResource()))]
            #_authzbase.ResourceController(PortAliasResource()))]

    def get_actions(self):
        return []

    def get_request_extensions(self):
        return []
