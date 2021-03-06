
# Copyright 2017-present Open Networking Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import base64
import struct
import socket
from netaddr import IPAddress, IPNetwork
from synchronizers.new_base.syncstep import *
from synchronizers.new_base.ansible_helper import *
from mock_modelaccessor import *

class SyncControllerNetworks(SyncStep):
    requested_interval = 0
    provides=[Network]
    observes=ControllerNetwork	
    external_dependencies = [User]
    playbook='sync_controller_networks.yaml'

    def fetch_pending(self, deleted):
        ci = ControllerNetwork()
        i = Network()
        i.name = "Lush Loss"
	s = Slice()
	s.name = "Ghastly Notebook"
	i.owner = s
        ci.i = i
        return [ci]

    def map_sync_outputs(self, controller_network,res):
        network_id = res[0]['network']['id']
        subnet_id = res[1]['subnet']['id']
        controller_network.net_id = network_id
        controller_network.subnet = self.cidr
        controller_network.subnet_id = subnet_id
	controller_network.backend_status = '1 - OK'
        if not controller_network.segmentation_id:
            controller_network.segmentation_id = str(self.get_segmentation_id(controller_network))
        controller_network.save()

    def map_sync_inputs(self, controller_network):
        pass

    def map_delete_inputs(self, controller_network):
	network_name = controller_network.network.name
        subnet_name = '%s-%d'%(network_name,controller_network.pk)
	cidr = controller_network.subnet
	network_fields = {'endpoint':controller_network.controller.auth_url,
                    'admin_user':slice.creator.email, # XXX: FIXME
                    'admin_project':slice.name, # XXX: FIXME
                    'admin_password':slice.creator.remote_password,
                    'name':network_name,
                    'subnet_name':subnet_name,
                    'ansible_tag':'%s-%s@%s'%(network_name,slice.slicename,controller_network.controller.name),
                    'cidr':cidr,
		    'delete':True	
                    }

        return network_fields

