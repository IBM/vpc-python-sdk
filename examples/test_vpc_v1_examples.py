# -*- coding: utf-8 -*-
# (C) Copyright IBM Corp. 2021.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Examples for VpcV1
"""

from ibm_cloud_sdk_core import ApiException, read_external_sources
import os
import pytest
from ibm_vpc.vpc_v1 import *

data={}
data['zone'] = 'us-east-1'
data['region'] = 'us-east'

#
# This file provides an example of how to use the vpc service.
#
# The following configuration properties are assumed to be defined:
# VPC_URL=<service base url>
# VPC_AUTH_TYPE=iam
# VPC_APIKEY=<IAM apikey>
# VPC_AUTH_URL=<IAM token service base URL - omit this if using the production environment>
#
# These configuration properties can be exported as environment variables, or stored
# in a configuration file and then:
# export IBM_CREDENTIALS_FILE=<name of configuration file>
#
config_file = 'vpc.env'

vpc_service = None

config = None


##############################################################################
# Start of Examples for Service: VpcV1
##############################################################################
# region
class TestVpcV1Examples():
    """
    Example Test Class for VpcV1
    """

    @classmethod
    def setup_class(cls):
        global vpc_service
        if os.path.exists(config_file):
            os.environ['IBM_CREDENTIALS_FILE'] = config_file

            # begin-common

            vpc_service = VpcV1.new_instance()

            # end-common
            assert vpc_service is not None

            # Load the configuration
            global config
            config = read_external_sources(VpcV1.DEFAULT_SERVICE_NAME)

        print('Setup complete.')

    needscredentials = pytest.mark.skipif(
        not os.path.exists(config_file),
        reason="External configuration not available, skipping...")

    @needscredentials
    def test_list_vpcs_example(self):
        """
        list_vpcs request example
        """
        try:
            print('\nlist_vpcs() result:')
            # begin-list_vpcs

            all_results = []
            pager = VpcsPager(
                client=vpc_service,
                limit=10,
                classic_access=False,
            )
            while pager.has_next():
                next_page = pager.get_next()
                assert next_page is not None
                all_results.extend(next_page)

            # end-list_vpcs

            print(json.dumps(all_results, indent=2))
            assert all_results is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_vpc_example(self):
        """
        create_vpc request example
        """
        try:
            print('\ncreate_vpc() result:')
            # begin-create_vpc

            vpc = vpc_service.create_vpc(
                address_prefix_management="manual",
                classic_access=True,
                name="my-vpc",
            ).get_result()

            # end-create_vpc
            assert vpc["id"] is not None
            data["vpcID"]=vpc["id"]

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_hub_vpc_example(self):
        """
        create_vpc request example
        """
        try:
            print('\ncreate_vpc() result:')
            # begin-create_vpc

            zone_identity_model = {
                'name': 'us-south-1',
            }
            dns_server_prototype_model = {
                'address': '192.168.3.4',
                'zone_affinity': zone_identity_model,
            }
            vpcdns_resolver_prototype_model = {
                'manual_servers': [dns_server_prototype_model],
                'type': 'manual',
            }
            vpcdns_prototype_model = {
                'enable_hub': False,
                'resolver': vpcdns_resolver_prototype_model,
            }
            vpc = vpc_service.create_vpc(
                address_prefix_management="manual",
                classic_access=True,
                name="my-vpc-hub",
                dns=vpcdns_prototype_model,
            ).get_result()

            # end-create_vpc
            assert vpc["id"] is not None
            data["vpcHubID"]=vpc["id"]

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_vpc_example(self):
        """
        get_vpc request example
        """
        try:
            print('\nget_vpc() result:')
            # begin-get_vpc

            vpc = vpc_service.get_vpc(id=data["vpcID"]).get_result()

            # end-get_vpc
            assert vpc is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_vpc_example(self):
        """
        update_vpc request example
        """
        try:
            print('\nupdate_vpc() result:')
            # begin-update_vpc

            vpc_patch_model = {}
            vpc_patch_model['name']='my-vpc-modified'

            vpc = vpc_service.update_vpc(
                id=data["vpcID"], vpc_patch=vpc_patch_model).get_result()

            # end-update_vpc
            assert vpc is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_vpc_default_network_acl_example(self):
        """
        get_vpc_default_network_acl request example
        """
        try:
            print('\nget_vpc_default_network_acl() result:')
            # begin-get_vpc_default_network_acl

            default_network_acl = vpc_service.get_vpc_default_network_acl(
                id=data["vpcID"]).get_result()

            # end-get_vpc_default_network_acl
            assert default_network_acl is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_vpc_default_routing_table_example(self):
        """
        get_vpc_default_routing_table request example
        """
        try:
            print('\nget_vpc_default_routing_table() result:')
            # begin-get_vpc_default_routing_table

            default_routing_table = vpc_service.get_vpc_default_routing_table(
                id=data["vpcID"]).get_result()

            # end-get_vpc_default_routing_table
            assert default_routing_table is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_vpc_default_security_group_example(self):
        """
        get_vpc_default_security_group request example
        """
        try:
            print('\nget_vpc_default_security_group() result:')
            # begin-get_vpc_default_security_group

            default_security_group = vpc_service.get_vpc_default_security_group(
                id=data["vpcID"]).get_result()

            # end-get_vpc_default_security_group
            assert default_security_group is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_vpc_address_prefixes_example(self):
        """
        list_vpc_address_prefixes request example
        """
        try:
            print('\nlist_vpc_address_prefixes() result:')
            # begin-list_vpc_address_prefixes

            all_results = []
            pager = VpcAddressPrefixesPager(
                client=vpc_service,
                vpc_id=data['vpcID'],
                limit=10,
            )
            while pager.has_next():
                next_page = pager.get_next()
                assert next_page is not None
                all_results.extend(next_page)

            # end-list_vpc_address_prefixes

            print(json.dumps(all_results, indent=2))
            assert all_results is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_vpc_address_prefix_example(self):
        """
        create_vpc_address_prefix request example
        """
        try:
            print('\ncreate_vpc_address_prefix() result:')
            # begin-create_vpc_address_prefix

            zone_identity_model = {}
            zone_identity_model['name']= data['zone']
            address_prefix = vpc_service.create_vpc_address_prefix(
                vpc_id=data['vpcID'],
                cidr='10.0.0.0/24',
                zone=zone_identity_model,
                name='my-address-prefix').get_result()

            # end-create_vpc_address_prefix
            assert address_prefix['id'] is not None
            data['vpcAddressPrefixId']=address_prefix['id']

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_vpc_address_prefix_example(self):
        """
        get_vpc_address_prefix request example
        """
        try:
            print('\nget_vpc_address_prefix() result:')
            # begin-get_vpc_address_prefix

            address_prefix = vpc_service.get_vpc_address_prefix(
                vpc_id=data['vpcID'], id=data['vpcAddressPrefixId']).get_result()

            # end-get_vpc_address_prefix
            assert address_prefix is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_vpc_address_prefix_example(self):
        """
        update_vpc_address_prefix request example
        """
        try:
            print('\nupdate_vpc_address_prefix() result:')
            # begin-update_vpc_address_prefix

            address_prefix_patch_model = {}
            address_prefix_patch_model['name']='my-address-prefix-updated'

            address_prefix = vpc_service.update_vpc_address_prefix(
                vpc_id=data['vpcID'],
                id=data['vpcAddressPrefixId'],
                address_prefix_patch=address_prefix_patch_model).get_result()

            # end-update_vpc_address_prefix
            assert address_prefix is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_vpc_dns_resolution_binding_example(self):
        """
        create_vpc_dns_resolution_binding request example
        """
        try:
            print('\ncreate_vpc_dns_resolution_binding() result:')
            # begin-create_vpc_dns_resolution_binding

            vpc_identity_model = {
                'id': data["vpcHubID"],
            }

            response = vpc_service.create_vpc_dns_resolution_binding(
                vpc_id=data['vpcID'],
                name='my-vpc-dns-resolution-binding',
                vpc=vpc_identity_model,
            )
            vpcdns_resolution_binding = response.get_result()
            # end-create_vpc_dns_resolution_binding
            data['vpcDnsResolutionBindingID'] = vpcdns_resolution_binding['id']
        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_vpc_dns_resolution_bindings_example(self):
        """
        list_vpc_dns_resolution_bindings request example
        """
        try:
            print('\nlist_vpc_dns_resolution_bindings() result:')
            # begin-list_vpc_dns_resolution_bindings

            all_results = []
            pager = VpcDnsResolutionBindingsPager(
                client=vpc_service,
                vpc_id=data['vpcID'],
                limit=10,
            )
            while pager.has_next():
                next_page = pager.get_next()
                assert next_page is not None
                all_results.extend(next_page)

            # end-list_vpc_dns_resolution_bindings
        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_vpc_dns_resolution_binding_example(self):
        """
        get_vpc_dns_resolution_binding request example
        """
        try:
            print('\nget_vpc_dns_resolution_binding() result:')
            # begin-get_vpc_dns_resolution_binding

            response = vpc_service.get_vpc_dns_resolution_binding(
                vpc_id=data['vpcID'],
                id=data['vpcDnsResolutionBindingID'],
            )
            vpcdns_resolution_binding = response.get_result()

            # end-get_vpc_dns_resolution_binding

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_vpc_dns_resolution_binding_example(self):
        """
        update_vpc_dns_resolution_binding request example
        """
        try:
            print('\nupdate_vpc_dns_resolution_binding() result:')
            # begin-update_vpc_dns_resolution_binding

            vpcdns_resolution_binding_patch_model = {
            }
            vpcdns_resolution_binding_patch_model['name']='my-vpc-dns-resolution-binding-updated'

            response = vpc_service.update_vpc_dns_resolution_binding(
                vpc_id=data['vpcID'],
                id=data['vpcDnsResolutionBindingID'],
                vpcdns_resolution_binding_patch=vpcdns_resolution_binding_patch_model,
            )
            vpcdns_resolution_binding = response.get_result()
            # end-update_vpc_dns_resolution_binding

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_vpc_routing_tables_example(self):
        """
        list_vpc_routing_tables request example
        """
        try:
            print('\nlist_vpc_routing_tables() result:')
            # begin-list_vpc_routing_tables

            all_results = []
            pager = VpcRoutingTablesPager(
                client=vpc_service,
                limit=10,
                vpc_id=data['vpcID'],
                is_default=True,
            )
            while pager.has_next():
                next_page = pager.get_next()
                assert next_page is not None
                all_results.extend(next_page)

            # end-list_vpc_routing_tables

            print(json.dumps(all_results, indent=2))
            assert all_results is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_vpc_routing_table_example(self):
        """
        create_vpc_routing_table request example
        """
        try:
            print('\ncreate_vpc_routing_table() result:')
            # begin-create_vpc_routing_table

            route_next_hop_prototype_model = {}
            route_next_hop_prototype_model['address']= '192.168.3.4'

            zone_identity_model = {}
            zone_identity_model['name']= data['zone']

            route_prototype_model = {}
            route_prototype_model['action'] = 'delegate'
            route_prototype_model['destination'] = '192.168.3.0/24'
            route_prototype_model['name'] = 'my-route'
            route_prototype_model['next_hop'] = route_next_hop_prototype_model
            route_prototype_model['zone'] = zone_identity_model

            routing_table = vpc_service.create_vpc_routing_table(
                vpc_id=data['vpcID'],
                name='my-routing-table',
                routes=[route_prototype_model],).get_result()

            # end-create_vpc_routing_table
            assert routing_table['id'] is not None
            data['vpcRoutingTableId']=routing_table['id']

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_vpc_routing_table_example(self):
        """
        get_vpc_routing_table request example
        """
        try:
            print('\nget_vpc_routing_table() result:')
            # begin-get_vpc_routing_table

            routing_table = vpc_service.get_vpc_routing_table(
                vpc_id=data['vpcID'], id=data['vpcRoutingTableId']).get_result()

            # end-get_vpc_routing_table
            assert routing_table is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_vpc_routing_table_example(self):
        """
        update_vpc_routing_table request example
        """
        try:
            print('\nupdate_vpc_routing_table() result:')
            # begin-update_vpc_routing_table

            routing_table_patch_model = {}
            routing_table_patch_model['name'] = 'my-routing-table-modified'

            routing_table = vpc_service.update_vpc_routing_table(
                vpc_id=data['vpcID'],
                id=data['vpcRoutingTableId'],
                routing_table_patch=routing_table_patch_model).get_result()

            # end-update_vpc_routing_table
            assert routing_table is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_vpc_routing_table_routes_example(self):
        """
        list_vpc_routing_table_routes request example
        """
        try:
            print('\nlist_vpc_routing_table_routes() result:')
            # begin-list_vpc_routing_table_routes

            all_results = []
            pager = VpcRoutingTableRoutesPager(
                client=vpc_service,
                vpc_id=data['vpcID'],
                routing_table_id=data['vpcRoutingTableId'],
                limit=10,
            )
            while pager.has_next():
                next_page = pager.get_next()
                assert next_page is not None
                all_results.extend(next_page)

            # end-list_vpc_routing_table_routes

            print(json.dumps(all_results, indent=2))
            assert all_results is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_vpc_routing_table_route_example(self):
        """
        create_vpc_routing_table_route request example
        """
        try:
            print('\ncreate_vpc_routing_table_route() result:')
            # begin-create_vpc_routing_table_route

            zone_identity_model = {}
            zone_identity_model['name'] = data['zone']

            route_next_hop_prototype_model = {}
            route_next_hop_prototype_model['address'] = '192.168.3.7'

            route = vpc_service.create_vpc_routing_table_route(
                vpc_id=data['vpcID'],
                routing_table_id=data['vpcRoutingTableId'],
                destination='192.168.77.0/24',
                zone=zone_identity_model,
                next_hop=route_next_hop_prototype_model,
                action='delegate',
                priority=1,
                name='my-routing-table-route').get_result()

            # end-create_vpc_routing_table_route
            assert route['id'] is not None
            data['vpcRoutingTableRouteId']=route['id']

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_vpc_routing_table_route_example(self):
        """
        get_vpc_routing_table_route request example
        """
        try:
            print('\nget_vpc_routing_table_route() result:')
            # begin-get_vpc_routing_table_route

            route = vpc_service.get_vpc_routing_table_route(
                vpc_id=data['vpcID'],
                routing_table_id=data['vpcRoutingTableId'],
                id=data['vpcRoutingTableRouteId']).get_result()

            # end-get_vpc_routing_table_route
            assert route is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_vpc_routing_table_route_example(self):
        """
        update_vpc_routing_table_route request example
        """
        try:
            print('\nupdate_vpc_routing_table_route() result:')
            # begin-update_vpc_routing_table_route

            route_patch_model = {}
            route_patch_model['name'] = 'my-routing-table-route-updated'
            route = vpc_service.update_vpc_routing_table_route(
                vpc_id=data['vpcID'],
                routing_table_id=data['vpcRoutingTableId'],
                id=data['vpcRoutingTableRouteId'],
                route_patch=route_patch_model).get_result()

            # end-update_vpc_routing_table_route
            assert route is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_subnets_example(self):
        """
        list_subnets request example
        """
        try:
            print('\nlist_subnets() result:')
            # begin-list_subnets

            all_results = []
            pager = SubnetsPager(
                client=vpc_service,
                limit=10,
            )
            while pager.has_next():
                next_page = pager.get_next()
                assert next_page is not None
                all_results.extend(next_page)

            # end-list_subnets

            print(json.dumps(all_results, indent=2))
            assert all_results is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_subnet_example(self):
        """
        create_subnet request example
        """
        try:
            print('\ncreate_subnet() result:')
            # begin-create_subnet

            vpc_identity_model = {}
            vpc_identity_model['id'] = data['vpcID']

            zone_identity_model = {}
            zone_identity_model['name'] = data['zone']

            subnet_prototype_model = {}
            subnet_prototype_model['name'] = 'my-subnet'
            subnet_prototype_model['vpc'] = vpc_identity_model
            subnet_prototype_model['ipv4_cidr_block'] = '10.0.1.0/24'
            subnet_prototype_model['zone'] = zone_identity_model

            subnet = vpc_service.create_subnet(
                subnet_prototype=subnet_prototype_model).get_result()

            # end-create_subnet
            assert subnet['id'] is not None
            data['subnetId']=subnet['id']

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_subnet_example(self):
        """
        get_subnet request example
        """
        try:
            print('\nget_subnet() result:')
            # begin-get_subnet

            subnet = vpc_service.get_subnet(id=data['subnetId']).get_result()

            # end-get_subnet
            assert subnet is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_subnet_example(self):
        """
        update_subnet request example
        """
        try:
            print('\nupdate_subnet() result:')
            # begin-update_subnet

            subnet_patch_model = {}
            subnet_patch_model['name'] ='my-subnet-updated'

            subnet = vpc_service.update_subnet(
                id=data['subnetId'], subnet_patch=subnet_patch_model).get_result()

            # end-update_subnet
            assert subnet is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_subnet_network_acl_example(self):
        """
        get_subnet_network_acl request example
        """
        try:
            print('\nget_subnet_network_acl() result:')
            # begin-get_subnet_network_acl

            network_acl = vpc_service.get_subnet_network_acl(
                id=data['subnetId']).get_result()

            # end-get_subnet_network_acl
            assert network_acl is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_replace_subnet_network_acl_example(self):
        """
        replace_subnet_network_acl request example
        """
        try:
            print('\nreplace_subnet_network_acl() result:')

            vpc_model = {}
            vpc_model['id'] = data['vpcID']

            network_acl_prototype_model = {}
            network_acl_prototype_model['name'] = 'my-subnet-network-acl'
            network_acl_prototype_model['vpc'] = vpc_model

            network_acl = vpc_service.create_network_acl(
                network_acl_prototype=network_acl_prototype_model).get_result()
            # begin-replace_subnet_network_acl

            network_acl_identity_model = {}
            network_acl_identity_model['id'] = network_acl['id']

            network_replace_acl = vpc_service.replace_subnet_network_acl(
                id=data['subnetId'],
                network_acl_identity=network_acl_identity_model).get_result()

            # end-replace_subnet_network_acl
            assert network_replace_acl is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_set_subnet_public_gateway_example(self):
        """
        set_subnet_public_gateway request example
        """
        try:
            print('\nset_subnet_public_gateway() result:')

            vpc_identity_model = {}
            vpc_identity_model['id']= data['vpcID']

            zone_identity_model = {}
            zone_identity_model['name']= data['zone']

            public_gateway = vpc_service.create_public_gateway(
                vpc=vpc_identity_model, zone=zone_identity_model).get_result()

            # begin-set_subnet_public_gateway

            public_gateway_identity_model = {}
            public_gateway_identity_model['id']= public_gateway['id']

            public_gateway_subnet = vpc_service.set_subnet_public_gateway(
                id=data['subnetId'],
                public_gateway_identity=public_gateway_identity_model
            ).get_result()

            # end-set_subnet_public_gateway
            assert public_gateway_subnet['id'] is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_subnet_public_gateway_example(self):
        """
        get_subnet_public_gateway request example
        """
        try:
            print('\nget_subnet_public_gateway() result:')
            # begin-get_subnet_public_gateway

            public_gateway = vpc_service.get_subnet_public_gateway(
                id=data['subnetId']).get_result()

            # end-get_subnet_public_gateway
            assert public_gateway is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_unset_subnet_public_gateway_example(self):
        """
        unset_subnet_public_gateway request example
        """
        try:
            # begin-unset_subnet_public_gateway

            response = vpc_service.unset_subnet_public_gateway(id=data['subnetId'])

            # end-unset_subnet_public_gateway
            assert response is not None
            print('\nunset_subnet_public_gateway() response status code: ',
                  response.get_status_code())

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_subnet_routing_table_example(self):
        """
        get_subnet_routing_table request example
        """
        try:
            print('\nget_subnet_routing_table() result:')
            # begin-get_subnet_routing_table

            routing_table = vpc_service.get_subnet_routing_table(
                id=data['subnetId']).get_result()

            # end-get_subnet_routing_table
            assert routing_table is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_replace_subnet_routing_table_example(self):
        """
        replace_subnet_routing_table request example
        """
        try:
            print('\nreplace_subnet_routing_table() result:')
            # begin-replace_subnet_routing_table

            routing_table_identity_model = {}
            routing_table_identity_model['id']= data['vpcRoutingTableId']

            routing_table = vpc_service.replace_subnet_routing_table(
                id=data['subnetId'],
                routing_table_identity=routing_table_identity_model).get_result(
                )

            # end-replace_subnet_routing_table
            assert routing_table is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_subnet_reserved_ips_example(self):
        """
        list_subnet_reserved_ips request example
        """
        try:
            print('\nlist_subnet_reserved_ips() result:')
            # begin-list_subnet_reserved_ips

            all_results = []
            pager = SubnetReservedIpsPager(
                client=vpc_service,
                subnet_id=data['subnetId'],
                limit=10,
                sort='name',
            )
            while pager.has_next():
                next_page = pager.get_next()
                assert next_page is not None
                all_results.extend(next_page)

            # end-list_subnet_reserved_ips

            print(json.dumps(all_results, indent=2))
            assert all_results is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_subnet_reserved_ip_example(self):
        """
        create_subnet_reserved_ip request example
        """
        try:
            print('\ncreate_subnet_reserved_ip() result:')
            # begin-create_subnet_reserved_ip

            reserved_ip = vpc_service.create_subnet_reserved_ip(
                subnet_id=data['subnetId'],name='my-subnet-reserved-ip', auto_delete=False).get_result()

            # end-create_subnet_reserved_ip
            assert reserved_ip['id'] is not None
            data['subnetReservedIp']=reserved_ip['id']

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_subnet_reserved_ip_example(self):
        """
        get_subnet_reserved_ip request example
        """
        try:
            print('\nget_subnet_reserved_ip() result:')
            # begin-get_subnet_reserved_ip

            reserved_ip = vpc_service.get_subnet_reserved_ip(
                subnet_id=data['subnetId'], id=data['subnetReservedIp']).get_result()

            # end-get_subnet_reserved_ip
            assert reserved_ip is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_subnet_reserved_ip_example(self):
        """
        update_subnet_reserved_ip request example
        """
        try:
            print('\nupdate_subnet_reserved_ip() result:')
            # begin-update_subnet_reserved_ip

            reserved_ip_patch_model = {}
            reserved_ip_patch_model['name']= 'my-reserved-ip-updated'

            reserved_ip = vpc_service.update_subnet_reserved_ip(
                subnet_id=data['subnetId'],
                id=data['subnetReservedIp'],
                reserved_ip_patch=reserved_ip_patch_model).get_result()

            # end-update_subnet_reserved_ip
            assert reserved_ip is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_images_example(self):
        """
        list_images request example
        """
        try:
            print('\nlist_images() result:')
            # begin-list_images

            all_results = []
            pager = ImagesPager(
                client=vpc_service,
                limit=10,
                visibility='private',
                user_data_format='cloud_init',
            )
            while pager.has_next():
                next_page = pager.get_next()
                assert next_page is not None
                all_results.extend(next_page)

            # end-list_images

            assert all_results is not None
            print(json.dumps(all_results, indent=2))

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_image_example(self):
        """
        create_image request example
        """
        try:
            print('\ncreate_image() result:')
            # begin-create_image

            image_file_prototype_model = {}
            image_file_prototype_model['href']= 'cos://us-south/my-bucket/my-image.qcow2'

            operating_system_identity_model = {}
            operating_system_identity_model['name'] = 'debian-9-amd64'

            image_prototype_model = {}
            image_prototype_model['file'] = image_file_prototype_model
            image_prototype_model['operating_system'] = operating_system_identity_model
            image_prototype_model['name'] = 'my-image'

            image = vpc_service.create_image(
                image_prototype=image_prototype_model).get_result()

            # end-create_image
            assert image['id'] is not None
            data['imageId']=image['id']

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_image_example(self):
        """
        get_image request example
        """
        try:
            print('\nget_image() result:')
            # begin-get_image

            image = vpc_service.get_image(id=data['imageId']).get_result()

            # end-get_image
            assert image is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_image_example(self):
        """
        update_image request example
        """
        try:
            print('\nupdate_image() result:')
            # begin-update_image

            image_patch_model = {}
            image_patch_model['name'] = 'my-image-updated'

            image = vpc_service.update_image(
                id=data['imageId'], image_patch=image_patch_model).get_result()

            # end-update_image
            assert image is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_image_export_jobs_example(self):
        """
        list_image_export_jobs request example
        """
        try:
            print('\nlist_image_export_jobs() result:')
            # begin-list_image_export_jobs

            response = vpc_service.list_image_export_jobs(
                image_id=data['imageId']
            )
            image_export_job_unpaginated_collection = response.get_result()

            # end-list_image_export_jobs
            assert image_export_job_unpaginated_collection is not None
        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_image_export_job_example(self):
        """
        create_image_export_job request example
        """
        try:
            print('\ncreate_image_export_job() result:')
            # begin-create_image_export_job

            cloud_object_storage_bucket_identity_model = {
                'name': 'bucket-27200-lwx4cfvcue',
            }

            image_export_job = vpc_service.create_image_export_job(
                image_id=data['imageId'],
                name='my-image-export-job',
                storage_bucket=cloud_object_storage_bucket_identity_model
            ).get_result()

            # end-create_image_export_job
            assert image_export_job is not None
            data['imageExportJobId']=image_export_job['id']
        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_image_export_job_example(self):
        """
        get_image_export_job request example
        """
        try:
            print('\nget_image_export_job() result:')
            # begin-get_image_export_job

            image_export_job = vpc_service.get_image_export_job(
                image_id=data['imageId'],
                id=data['imageExportJobId']
            ).get_result()

            # end-get_image_export_job
            assert image_export_job is not None
        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_image_export_job_example(self):
        """
        update_image_export_job request example
        """
        try:
            print('\nupdate_image_export_job() result:')
            # begin-update_image_export_job

            image_export_job_patch_model = {
                'name' : 'my-image-export-job-updated'
            }

            image_export_job = vpc_service.update_image_export_job(
                image_id=data['imageId'],
                id=data['imageExportJobId'],
                image_export_job_patch=image_export_job_patch_model
            ).get_result()

            # end-update_image_export_job
            assert image_export_job is not None
        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_image_export_job_example(self):
        """
        delete_image_export_job request example
        """
        try:
            # begin-delete_image_export_job

            response = vpc_service.delete_image_export_job(
                image_id=data['imageId'],
                id=data['imageExportJobId']
            )

            # end-delete_image_export_job
            print('\ndelete_image_export_job() response status code: ', response.get_status_code())

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_operating_systems_example(self):
        """
        list_operating_systems request example
        """
        try:
            print('\nlist_operating_systems() result:')
            # begin-list_operating_systems

            all_results = []
            pager = OperatingSystemsPager(
                client=vpc_service,
                limit=10,
            )
            while pager.has_next():
                next_page = pager.get_next()
                assert next_page is not None
                all_results.extend(next_page)

            # end-list_operating_systems

            print(json.dumps(all_results, indent=2))
            assert all_results is not None
            data['operatingSystemName']=all_results[0]['name']

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_operating_system_example(self):
        """
        get_operating_system request example
        """
        try:
            print('\nget_operating_system() result:')
            # begin-get_operating_system

            operating_system = vpc_service.get_operating_system(
                name=data['operatingSystemName']).get_result()

            # end-get_operating_system
            assert operating_system is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_keys_example(self):
        """
        list_keys request example
        """
        try:
            print('\nlist_keys() result:')
            # begin-list_keys

            all_results = []
            pager = KeysPager(
                client=vpc_service,
                limit=10,
            )
            while pager.has_next():
                next_page = pager.get_next()
                assert next_page is not None
                all_results.extend(next_page)

            # end-list_keys

            print(json.dumps(all_results, indent=2))
            assert all_results is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_key_example(self):
        """
        create_key request example
        """
        try:
            print('\ncreate_key() result:')
            # begin-create_key

            key = vpc_service.create_key(
                public_key=
                'AAAAB3NzaC1yc2EAAAADAQABAAABAQDDGe50Bxa5T5NDddrrtbx2Y4/VGbiCgXqnBsYToIUKoFSHTQl5IX3PasGnneKanhcLwWz5M5MoCRvhxTp66NKzIfAz7r+FX9rxgR+ZgcM253YAqOVeIpOU408simDZKriTlN8kYsXL7P34tsWuAJf4MgZtJAQxous/2byetpdCv8ddnT4X3ltOg9w+LqSCPYfNivqH00Eh7S1Ldz7I8aw5WOp5a+sQFP/RbwfpwHp+ny7DfeIOokcuI42tJkoBn7UsLTVpCSmXr2EDRlSWe/1M/iHNRBzaT3CK0+SwZWd2AEjePxSnWKNGIEUJDlUYp7hKhiQcgT5ZAnWU121oc5En',
                name='my-ssh-key'
            ).get_result()

            # end-create_key
            assert key['id'] is not None
            data['keyId']=key['id']

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_key_example(self):
        """
        get_key request example
        """
        try:
            print('\nget_key() result:')
            # begin-get_key

            key = vpc_service.get_key(id=data['keyId']).get_result()

            # end-get_key
            assert key is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_key_example(self):
        """
        update_key request example
        """
        try:
            print('\nupdate_key() result:')
            # begin-update_key

            key_patch_model = {}
            key_patch_model['name'] = 'my-ssh-key-updated'

            key = vpc_service.update_key(
                id=data['keyId'], key_patch=key_patch_model).get_result()

            # end-update_key
            assert key is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_floating_ips_example(self):
        """
        list_floating_ips request example
        """
        try:
            print('\nlist_floating_ips() result:')
            # begin-list_floating_ips

            all_results = []
            pager = FloatingIpsPager(
                client=vpc_service,
                limit=10,
                sort='name',
            )
            while pager.has_next():
                next_page = pager.get_next()
                assert next_page is not None
                all_results.extend(next_page)

            # end-list_floating_ips

            print(json.dumps(all_results, indent=2))
            assert all_results is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_floating_ip_example(self):
        """
        create_floating_ip request example
        """
        try:
            print('\ncreate_floating_ip() result:')
            # begin-create_floating_ip

            zone_identity_model = {}
            zone_identity_model['name'] = data['zone']

            floating_ip_prototype_model = {}
            floating_ip_prototype_model['zone'] = zone_identity_model
            floating_ip_prototype_model['name'] = 'my-floating-ip'

            floating_ip = vpc_service.create_floating_ip(
                floating_ip_prototype=floating_ip_prototype_model).get_result()

            # end-create_floating_ip
            assert floating_ip['id'] is not None
            data['floatingIpId']=floating_ip['id']

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_floating_ip_example(self):
        """
        get_floating_ip request example
        """
        try:
            print('\nget_floating_ip() result:')
            # begin-get_floating_ip

            floating_ip = vpc_service.get_floating_ip(
                id=data['floatingIpId']).get_result()

            # end-get_floating_ip
            assert floating_ip['id'] is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_floating_ip_example(self):
        """
        update_floating_ip request example
        """
        try:
            print('\nupdate_floating_ip() result:')
            # begin-update_floating_ip

            floating_ip_patch_model = {}
            floating_ip_patch_model['name'] = 'my-floating-ip-updated'

            floating_ip = vpc_service.update_floating_ip(
                id=data['floatingIpId'],
                floating_ip_patch=floating_ip_patch_model).get_result()

            # end-update_floating_ip
            assert floating_ip is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_volume_profiles_example(self):
        """
        list_volume_profiles request example
        """
        try:
            print('\nlist_volume_profiles() result:')
            # begin-list_volume_profiles

            all_results = []
            pager = VolumeProfilesPager(
                client=vpc_service,
                limit=10,
            )
            while pager.has_next():
                next_page = pager.get_next()
                assert next_page is not None
                all_results.extend(next_page)

            # end-list_volume_profiles

            print(json.dumps(all_results, indent=2))
            assert all_results is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_volume_profile_example(self):
        """
        get_volume_profile request example
        """
        try:
            print('\nget_volume_profile() result:')
            # begin-get_volume_profile

            volume_profile = vpc_service.get_volume_profile(
                name='10iops-tier').get_result()

            # end-get_volume_profile

            assert volume_profile is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_volumes_example(self):
        """
        list_volumes request example
        """
        try:
            print('\nlist_volumes() result:')
            # begin-list_volumes

            all_results = []
            pager = VolumesPager(
                client=vpc_service,
                limit=10,
                attachment_state='attached',
                encryption='provider_managed',
                operating_system_family='Ubuntu Server',
                operating_system_architecture='amd64',
                zone_name='us-south-2',
            )
            while pager.has_next():
                next_page = pager.get_next()
                assert next_page is not None
                all_results.extend(next_page)

            # end-list_volumes

            print(json.dumps(all_results, indent=2))
            assert all_results is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_volume_example(self):
        """
        create_volume request example
        """
        try:
            print('\ncreate_volume() result:')
            # begin-create_volume

            volume_profile_identity_model = {}
            volume_profile_identity_model['name'] = '5iops-tier'

            zone_identity_model = {}
            zone_identity_model['name'] = data['zone']

            volume_prototype_model = {}
            volume_prototype_model['name'] = 'my-volume'
            volume_prototype_model['profile'] = volume_profile_identity_model
            volume_prototype_model['zone'] = zone_identity_model
            volume_prototype_model['capacity'] = 100
            volume_prototype_model['user_tags'] = ['my-daily-backup-policy']
            volume = vpc_service.create_volume(
                volume_prototype=volume_prototype_model).get_result()

            # end-create_volume
            assert volume['id'] is not None
            data['volumeId']=volume['id']

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_volume_example(self):
        """
        get_volume request example
        """
        try:
            print('\nget_volume() result:')
            # begin-get_volume

            volume = vpc_service.get_volume(id=data['volumeId']).get_result()

            # end-get_volume
            assert volume is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_volume_example(self):
        """
        update_volume request example
        """
        try:
            print('\nupdate_volume() result:')
            # begin-update_volume

            volume_patch_model = {}
            volume_patch_model['name'] = 'my-volume-updated'

            volume = vpc_service.update_volume(
                id=data['volumeId'], volume_patch=volume_patch_model).get_result()

            # end-update_volume
            assert volume is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_instance_profiles_example(self):
        """
        list_instance_profiles request example
        """
        try:
            print('\nlist_instance_profiles() result:')
            # begin-list_instance_profiles

            instance_profile_collection = vpc_service.list_instance_profiles(
            ).get_result()

            # end-list_instance_profiles
            assert instance_profile_collection is not None
            data['instanceProfileName']=instance_profile_collection['profiles'][0]['name']

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_instance_profile_example(self):
        """
        get_instance_profile request example
        """
        try:
            print('\nget_instance_profile() result:')
            # begin-get_instance_profile

            instance_profile = vpc_service.get_instance_profile(
                name=data['instanceProfileName']).get_result()

            # end-get_instance_profile
            assert instance_profile is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_instance_templates_example(self):
        """
        list_instance_templates request example
        """
        try:
            print('\nlist_instance_templates() result:')
            # begin-list_instance_templates

            instance_template_collection = vpc_service.list_instance_templates(
            ).get_result()

            # end-list_instance_templates

            assert instance_template_collection is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_instance_template_example(self):
        """
        create_instance_template request example
        """
        try:
            print('\ncreate_instance_template() result:')
            # begin-create_instance_template

            key_identity_model = {}
            key_identity_model['id'] =  data['keyId']

            subnet_identity_model = {}
            subnet_identity_model['id'] = data['subnetId']

            network_interface_prototype_model = {}
            network_interface_prototype_model['subnet'] = subnet_identity_model
            network_interface_prototype_model['name'] = 'my-network-interface'

            instance_profile_identity_model = {}
            instance_profile_identity_model['name'] = data['instanceProfileName']

            vpc_identity_model = {}
            vpc_identity_model['id'] = data['vpcID']

            zone_identity_model = {}
            zone_identity_model['name'] = data['zone']

            image_identity_model = {}
            image_identity_model['id'] = data['imageId']

            metadata_service_model = {}
            metadata_service_model['enabled'] = True
            metadata_service_model['protocol'] = 'https'
            metadata_service_model['response_hop_limit'] = 5
            instance_template_prototype_model = {}
            instance_template_prototype_model['keys'] = [key_identity_model]
            instance_template_prototype_model['name'] = 'my-instance-template'
            instance_template_prototype_model['profile'] = instance_profile_identity_model
            instance_template_prototype_model['vpc'] = vpc_identity_model
            instance_template_prototype_model['image'] = image_identity_model
            instance_template_prototype_model['primary_network_interface'] = network_interface_prototype_model
            instance_template_prototype_model['zone'] = zone_identity_model

            instance_template = vpc_service.create_instance_template(
                instance_template_prototype=instance_template_prototype_model
            ).get_result()

            # end-create_instance_template

            assert instance_template is not None
            data['instanceTemplateId']=instance_template['id']

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_instance_template_example(self):
        """
        get_instance_template request example
        """
        try:
            print('\nget_instance_template() result:')
            # begin-get_instance_template

            instance_template = vpc_service.get_instance_template(
                id=data['instanceTemplateId']).get_result()
            # end-get_instance_template

            assert instance_template is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_instance_template_example(self):
        """
        update_instance_template request example
        """
        try:
            print('\nupdate_instance_template() result:')
            # begin-update_instance_template

            instance_template_patch_model = {}
            instance_template_patch_model['name'] = 'my-instance-template-updated'

            instance_template = vpc_service.update_instance_template(
                id=data['instanceTemplateId'],
                instance_template_patch=instance_template_patch_model
            ).get_result()

            # end-update_instance_template

            assert instance_template is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_instances_example(self):
        """
        list_instances request example
        """
        try:
            print('\nlist_instances() result:')
            # begin-list_instances

            all_results = []
            pager = InstancesPager(
                client=vpc_service,
                limit=10,
                vpc_id=data['vpcID'],
            )
            while pager.has_next():
                next_page = pager.get_next()
                assert next_page is not None
                all_results.extend(next_page)

            # end-list_instances

            print(json.dumps(all_results, indent=2))
            assert all_results is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_instance_example(self):
        """
        create_instance request example
        """
        try:
            print('\ncreate_instance() result:')
            # begin-create_instance

            subnet_identity_model = {}
            subnet_identity_model['id'] = data['subnetId']

            network_interface_prototype_model = {}
            network_interface_prototype_model['name'] = 'my-network-interface'
            network_interface_prototype_model['subnet'] = subnet_identity_model

            instance_profile_identity_model = {}
            instance_profile_identity_model['name'] = 'bx2-2x8'

            vpc_identity_model = {}
            vpc_identity_model['id'] = data['vpcID']

            zone_identity_model = {}
            zone_identity_model['name'] = data['zone']

            image_identity_model = {}
            image_identity_model['id'] = data['imageId']

            instance_prototype_model = {}
            instance_prototype_model['name'] = 'my-instance'
            instance_prototype_model['profile'] = instance_profile_identity_model
            instance_prototype_model['vpc'] = vpc_identity_model
            instance_prototype_model['primary_network_interface'] = network_interface_prototype_model
            instance_prototype_model['zone'] = zone_identity_model
            instance_prototype_model['image'] = image_identity_model

            instance = vpc_service.create_instance(
                instance_prototype=instance_prototype_model).get_result()

            # end-create_instance

            assert instance is not None
            data['instanceId']=instance['id']

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_instance_example(self):
        """
        get_instance request example
        """
        try:
            print('\nget_instance() result:')
            # begin-get_instance

            instance = vpc_service.get_instance(id=data['instanceId']).get_result()

            # end-get_instance
            assert instance is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_instance_example(self):
        """
        update_instance request example
        """
        try:
            print('\nupdate_instance() result:')
            # begin-update_instance

            instance_patch_model = {}
            instance_patch_model['name']='my-instance-updated'

            instance = vpc_service.update_instance(
                id=data['instanceId'],
                instance_patch=instance_patch_model).get_result()

            # end-update_instance
            assert instance is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_instance_initialization_example(self):
        """
        get_instance_initialization request example
        """
        try:
            print('\nget_instance_initialization() result:')
            # begin-get_instance_initialization

            instance_initialization = vpc_service.get_instance_initialization(
                id=data['instanceId']).get_result()

            # end-get_instance_initialization
            assert instance_initialization is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_instance_action_example(self):
        """
        create_instance_action request example
        """
        try:
            print('\ncreate_instance_action() result:')
            # begin-create_instance_action

            instance_action = vpc_service.create_instance_action(
                instance_id=data['instanceId'], type='reboot').get_result()

            # end-create_instance_action
            assert instance_action is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    @pytest.mark.skip(reason="mock")
    def test_create_instance_console_access_token_example(self):
        """
        create_instance_console_access_token request example
        """
        try:
            print('\ncreate_instance_console_access_token() result:')
            # begin-create_instance_console_access_token

            instance_console_access_token = vpc_service.create_instance_console_access_token(
                instance_id=data['instanceId'], console_type='serial').get_result()

            assert instance_console_access_token is not None

            # end-create_instance_console_access_token

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    @pytest.mark.skip(reason="mock")
    def test_list_instance_disks_example(self):
        """
        list_instance_disks request example
        """
        try:
            print('\nlist_instance_disks() result:')
            # begin-list_instance_disks

            instance_disk_collection = vpc_service.list_instance_disks(instance_id=data['instanceId']).get_result()

            assert instance_disk_collection is not None
            data['instanceDiskId']=instance_disk_collection['disks'][0]['id']

            # end-list_instance_disks

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    @pytest.mark.skip(reason="mock")
    def test_get_instance_disk_example(self):
        """
        get_instance_disk request example
        """
        try:
            print('\nget_instance_disk() result:')
            # begin-get_instance_disk

            instance_disk = vpc_service.get_instance_disk(
                instance_id=data['instanceId'], id=data['instanceDiskId']).get_result()

            assert instance_disk is not None

            # end-get_instance_disk

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    @pytest.mark.skip(reason="mock")
    def test_update_instance_disk_example(self):
        """
        update_instance_disk request example
        """
        try:
            print('\nupdate_instance_disk() result:')
            # begin-update_instance_disk

            instance_disk_patch_model = {
                'name': 'my-instance-disk-updated'
            }

            instance_disk = vpc_service.update_instance_disk(
                instance_id=data['instanceId'],
                id=data['instanceDiskId'],
                instance_disk_patch=instance_disk_patch_model).get_result()

            assert instance_disk is not None

            # end-update_instance_disk

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_instance_network_interfaces_example(self):
        """
        list_instance_network_interfaces request example
        """
        try:
            print('\nlist_instance_network_interfaces() result:')
            # begin-list_instance_network_interfaces

            network_interface_unpaginated_collection = vpc_service.list_instance_network_interfaces(
                instance_id=data['instanceId']).get_result()

            # end-list_instance_network_interfaces
            assert network_interface_unpaginated_collection is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_instance_network_interface_example(self):
        """
        create_instance_network_interface request example
        """
        try:
            print('\ncreate_instance_network_interface() result:')
            # begin-create_instance_network_interface

            subnet_identity_model = {}
            subnet_identity_model['id'] = data['subnetId']

            network_interface = vpc_service.create_instance_network_interface(
                name='my-network-interface',
                instance_id=data['instanceId'],
                subnet=subnet_identity_model).get_result()

            # end-create_instance_network_interface

            assert network_interface is not None
            data['eth2Id']=network_interface['id']

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_instance_network_interface_example(self):
        """
        get_instance_network_interface request example
        """
        try:
            print('\nget_instance_network_interface() result:')
            # begin-get_instance_network_interface

            network_interface = vpc_service.get_instance_network_interface(
                instance_id=data['instanceId'], id=data['eth2Id']).get_result()

            # end-get_instance_network_interface

            assert network_interface is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_instance_network_interface_example(self):
        """
        update_instance_network_interface request example
        """
        try:
            print('\nupdate_instance_network_interface() result:')
            # begin-update_instance_network_interface

            network_interface_patch_model = {}
            network_interface_patch_model['name'] = 'my-network-interface-updated'
            network_interface_patch_model['allow_ip_spoofing'] = True

            network_interface = vpc_service.update_instance_network_interface(
                instance_id=data['instanceId'],
                id=data['eth2Id'],
                network_interface_patch=network_interface_patch_model
            ).get_result()

            # end-update_instance_network_interface

            assert network_interface is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_add_instance_network_interface_floating_ip_example(self):
        """
        add_instance_network_interface_floating_ip request example
        """
        try:
            print('\nadd_instance_network_interface_floating_ip() result:')
            # begin-add_instance_network_interface_floating_ip

            floating_ip = vpc_service.add_instance_network_interface_floating_ip(
                instance_id=data['instanceId'],
                network_interface_id=data['eth2Id'],
                id=data['floatingIpId']).get_result()

            # end-add_instance_network_interface_floating_ip

            assert floating_ip is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_instance_network_interface_floating_ips_example(self):
        """
        list_instance_network_interface_floating_ips request example
        """
        try:
            print('\nlist_instance_network_interface_floating_ips() result:')
            # begin-list_instance_network_interface_floating_ips

            floating_ip_unpaginated_collection = vpc_service.list_instance_network_interface_floating_ips(
                instance_id=data['instanceId'],
                network_interface_id=data['eth2Id']).get_result()

            # end-list_instance_network_interface_floating_ips

            assert floating_ip_unpaginated_collection is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_instance_network_interface_floating_ip_example(self):
        """
        get_instance_network_interface_floating_ip request example
        """
        try:
            print('\nget_instance_network_interface_floating_ip() result:')
            # begin-get_instance_network_interface_floating_ip

            floating_ip = vpc_service.get_instance_network_interface_floating_ip(
                instance_id=data['instanceId'],
                network_interface_id=data['eth2Id'],
                id=data['floatingIpId']).get_result()

            # end-get_instance_network_interface_floating_ip

            assert floating_ip is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_instance_network_interface_ips_example(self):
        """
        list_instance_network_interface_ips request example
        """
        try:
            print('\nlist_instance_network_interface_ips() result:')
            # begin-list_instance_network_interface_ips

            all_results = []
            pager = InstanceNetworkInterfaceIpsPager(
                client=vpc_service,
                instance_id=data['instanceId'],
                network_interface_id=data['eth2Id'],
                limit=10,
            )
            while pager.has_next():
                next_page = pager.get_next()
                assert next_page is not None
                all_results.extend(next_page)

            # end-list_instance_network_interface_ips

            print(json.dumps(all_results, indent=2))
            assert all_results is not None
        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_instance_network_interface_ip_example(self):
        """
        get_instance_network_interface_ip request example
        """
        try:
            print('\nget_instance_network_interface_ip() result:')
            # begin-get_instance_network_interface_ip

            reserved_ip = vpc_service.get_instance_network_interface_ip(
                instance_id=data['instanceId'],
                network_interface_id=data['eth2Id'],
                id=data['subnetReservedIp']
            ).get_result()


            # end-get_instance_network_interface_ip
            assert reserved_ip is not None
        except ApiException as e:
            pytest.fail(str(e))
    @needscredentials
    def test_list_instance_volume_attachments_example(self):
        """
        list_instance_volume_attachments request example
        """
        try:
            print('\nlist_instance_volume_attachments() result:')
            # begin-list_instance_volume_attachments

            volume_attachment_collection = vpc_service.list_instance_volume_attachments(
                instance_id=data['instanceId']).get_result()

            # end-list_instance_volume_attachments

            assert volume_attachment_collection is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_instance_volume_attachment_example(self):
        """
        create_instance_volume_attachment request example
        """
        try:
            print('\ncreate_instance_volume_attachment() result:')
            # begin-create_instance_volume_attachment

            volume_attachment_prototype_volume_model = {}
            volume_attachment_prototype_volume_model['id'] = data['volumeId']

            volume_attachment = vpc_service.create_instance_volume_attachment(
                instance_id=data['instanceId'],
                volume=volume_attachment_prototype_volume_model,
                 name='my-instance-volume-attachment',
                 delete_volume_on_instance_delete=True).get_result()

            # end-create_instance_volume_attachment

            assert volume_attachment is not None
            data['volumeAttachmentId']=volume_attachment['id']

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_instance_volume_attachment_example(self):
        """
        get_instance_volume_attachment request example
        """
        try:
            print('\nget_instance_volume_attachment() result:')
            # begin-get_instance_volume_attachment

            volume_attachment = vpc_service.get_instance_volume_attachment(
                instance_id=data['instanceId'], id=data['volumeAttachmentId']).get_result()

            # end-get_instance_volume_attachment

            assert volume_attachment is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_instance_volume_attachment_example(self):
        """
        update_instance_volume_attachment request example
        """
        try:
            print('\nupdate_instance_volume_attachment() result:')
            # begin-update_instance_volume_attachment

            volume_attachment_patch_model = {}
            volume_attachment_patch_model['name'] = 'my-instance-volume-attachment-updated'

            volume_attachment = vpc_service.update_instance_volume_attachment(
                instance_id=data['instanceId'],
                id=data['volumeAttachmentId'],
                volume_attachment_patch=volume_attachment_patch_model
            ).get_result()

            # end-update_instance_volume_attachment

            assert volume_attachment is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_reservations_example(self):
        """
        list_reservations request example
        """
        try:
            print('\nlist_reservations() result:')
            # begin-list_reservations

            reservation_collection = vpc_service.list_reservations().get_result()

            # end-list_instance_profiles
            assert reservation_collection is not None
        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_reservation_example(self):
        """
        create_reservation request example
        """
        try:
            print('\ncreate_reservation() result:')
            # begin-create_reservation

            capacity_model = {}
            capacity_model['total'] = 10

            committed_use_model = {}
            committed_use_model['term'] = 'one_year'

            profile_model = {}
            profile_model['name'] = 'ba2-2x8'
            profile_model['resource_type'] = 'instance_profile'

            zone_identity_model = {}
            zone_identity_model['name'] = data['zone']

            reservation = vpc_service.create_reservation(
                capacity=capacity_model, 
                committed_use=committed_use_model, 
                profile=profile_model, 
                zone=zone_identity_model, 
                name='my-reservation').get_result()

            # end-create_reservation
            assert reservation['id'] is not None
            data['reservationId']=reservation['id']

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_reservation_example(self):
        """
        update_reservation request example
        """
        try:
            print('\nupdate_reservation() result:')
            # begin-update_reservation

            reservation_patch_model = {}
            reservation_patch_model['name'] ='my-reservation-updated'

            reservation = vpc_service.update_reservation(
                id=data['reservationId'], reservation_patch=reservation_patch_model).get_result()

            # end-update_reservation
            assert reservation is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_activate_reservation_example(self):
        """
        activate_reservation request example
        """
        try:
            print('\nactivate_reservation() result:')
            # begin-activate_reservation

            response = vpc_service.activate_reservation(
                id=data['reservationId']).get_result()

            # end-activate_reservation
        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_reservation_example(self):
        """
        get_reservation request example
        """
        try:
            print('\nget_reservation() result:')
            # begin-activate_reservation

            reservation = vpc_service.get_reservation(
                id=data['reservationId']).get_result()

            # end-get_reservation
            assert reservation is not None
        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_instance_with_reservation_example(self):
        """
        create_instance with reservation request example
        """
        try:
            print('\ncreate_instance_with_reservation() result:')
            # begin-create_instance

            subnet_identity_model = {}
            subnet_identity_model['id'] = data['subnetId']

            network_interface_prototype_model = {}
            network_interface_prototype_model['name'] = 'my-network-interface'
            network_interface_prototype_model['subnet'] = subnet_identity_model

            instance_profile_identity_model = {}
            instance_profile_identity_model['name'] = 'bx2-2x8'

            vpc_identity_model = {}
            vpc_identity_model['id'] = data['vpcID']

            zone_identity_model = {}
            zone_identity_model['name'] = data['zone']

            reservation_identity_model = {}
            reservation_identity_model['id'] =  data['reservationId']

            reservation_affinity_model = {}
            reservation_affinity_model['policy'] = 'manual'
            reservation_affinity_model['pool'] = [reservation_identity_model]

            image_identity_model = {}
            image_identity_model['id'] = data['imageId']

            instance_prototype_model = {}
            instance_prototype_model['name'] = 'my-instance-with-res'
            instance_prototype_model['profile'] = instance_profile_identity_model
            instance_prototype_model['vpc'] = vpc_identity_model
            instance_prototype_model['primary_network_interface'] = network_interface_prototype_model
            instance_prototype_model['zone'] = zone_identity_model
            instance_prototype_model['image'] = image_identity_model
            instance_prototype_model['reservation_affinity'] = reservation_affinity_model

            instance = vpc_service.create_instance(
                instance_prototype=instance_prototype_model).get_result()

            # end-create_instance

            assert instance is not None
            data['instanceIdWithRes']=instance['id']

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_instance_with_reservation_example(self):
        """
        update_instance with reservation request example
        """
        try:
            print('\nupdate_instance_with_reservation() result:')
            # begin-update_instance

            reservation_identity_model = {}
            reservation_identity_model['id'] =  data['reservationId']

            reservation_affinity_model = {}
            reservation_affinity_model['policy'] = 'manual'
            reservation_affinity_model['pool'] = [reservation_identity_model]

            instance_patch_model = {}
            instance_patch_model['name']='my-instance-updated'
            instance_patch_model['reservation_affinity'] = reservation_affinity_model

            instance = vpc_service.update_instance(
                id=data['instanceId'],
                instance_patch=instance_patch_model).get_result()

            # end-update_instance
            assert instance is not None

        except ApiException as e:
            pytest.fail(str(e))


    @needscredentials
    @pytest.mark.skip(reason="mock")
    def test_delete_reservation_example(self):
        """
        delete_reservation request example
        """
        try:
            # begin-delete_reservation

            response = vpc_service.delete_reservation(
                id=data['reservationId'])

            assert response is not None

            # end-delete_reservation
            print('\ndelete_reservation() response status code: ',
                  response.get_status_code())

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_instance_groups_example(self):
        """
        list_instance_groups request example
        """
        try:
            print('\nlist_instance_groups() result:')
            # begin-list_instance_groups

            all_results = []
            pager = InstanceGroupsPager(
                client=vpc_service,
                limit=10,
            )
            while pager.has_next():
                next_page = pager.get_next()
                assert next_page is not None
                all_results.extend(next_page)

            # end-list_instance_groups

            print(json.dumps(all_results, indent=2))
            assert all_results is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_instance_group_example(self):
        """
        create_instance_group request example
        """
        try:
            print('\ncreate_instance_group() result:')
            # begin-create_instance_group

            instance_template_identity_model = {}
            instance_template_identity_model['id'] = data['instanceTemplateId']

            subnet_identity_model = {}
            subnet_identity_model['id'] = data['subnetId']

            instance_group = vpc_service.create_instance_group(
                instance_template=instance_template_identity_model,
                subnets=[subnet_identity_model],
                name='my-instance-group').get_result()

            # end-create_instance_group

            assert instance_group is not None
            data['instanceGroupId']=instance_group['id']

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_instance_group_example(self):
        """
        get_instance_group request example
        """
        try:
            print('\nget_instance_group() result:')
            # begin-get_instance_group

            instance_group = vpc_service.get_instance_group(
                id=data['instanceGroupId']).get_result()

            # end-get_instance_group

            assert instance_group is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_instance_group_example(self):
        """
        update_instance_group request example
        """
        try:
            print('\nupdate_instance_group() result:')
            # begin-update_instance_group

            instance_group_patch_model = {}
            instance_group_patch_model['name'] = 'my-instance-group-updated'

            instance_group = vpc_service.update_instance_group(
                id=data['instanceGroupId'],
                instance_group_patch=instance_group_patch_model).get_result()

            # end-update_instance_group

            assert instance_group is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_instance_group_managers_example(self):
        """
        list_instance_group_managers request example
        """
        try:
            print('\nlist_instance_group_managers() result:')
            # begin-list_instance_group_managers

            all_results = []
            pager = InstanceGroupManagersPager(
                client=vpc_service,
                instance_group_id=data['instanceGroupId'],
                limit=10,
            )
            while pager.has_next():
                next_page = pager.get_next()
                assert next_page is not None
                all_results.extend(next_page)

            # end-list_instance_group_managers

            print(json.dumps(all_results, indent=2))
            assert all_results is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_instance_group_manager_example(self):
        """
        create_instance_group_manager request example
        """
        try:
            print('\ncreate_instance_group_manager() result:')
            # begin-create_instance_group_manager

            instance_group_manager_prototype_model = {}
            instance_group_manager_prototype_model['name'] = 'my-instance-group-manager'
            instance_group_manager_prototype_model['manager_type'] = 'autoscale'
            instance_group_manager_prototype_model['max_membership_count'] = 5
            instance_group_manager_prototype_model['manager_type' ] = 'autoscale'

            instance_group_manager = vpc_service.create_instance_group_manager(
                instance_group_id=data['instanceGroupId'],
                instance_group_manager_prototype=
                instance_group_manager_prototype_model).get_result()

            # end-create_instance_group_manager

            assert instance_group_manager is not None
            data['instanceGroupManagerId']=instance_group_manager['id']

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_instance_group_manager_example(self):
        """
        get_instance_group_manager request example
        """
        try:
            print('\nget_instance_group_manager() result:')
            # begin-get_instance_group_manager

            instance_group_manager = vpc_service.get_instance_group_manager(
                instance_group_id=data['instanceGroupId'], id=data['instanceGroupManagerId']).get_result()

            # end-get_instance_group_manager

            assert instance_group_manager is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_instance_group_manager_example(self):
        """
        update_instance_group_manager request example
        """
        try:
            print('\nupdate_instance_group_manager() result:')
            # begin-update_instance_group_manager

            instance_group_manager_patch_model = {}
            instance_group_manager_patch_model['name'] = 'my-instance-group-manager-updated'

            instance_group_manager = vpc_service.update_instance_group_manager(
                instance_group_id=data['instanceGroupId'],
                id=data['instanceGroupManagerId'],
                instance_group_manager_patch=instance_group_manager_patch_model
            ).get_result()

            # end-update_instance_group_manager

            assert instance_group_manager is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_instance_group_manager_actions_example(self):
        """
        list_instance_group_manager_actions request example
        """
        try:
            print('\nlist_instance_group_manager_actions() result:')
            # begin-list_instance_group_manager_actions

            all_results = []
            pager = InstanceGroupManagerActionsPager(
                client=vpc_service,
                instance_group_id=data['instanceGroupId'],
                instance_group_manager_id=data['instanceGroupManagerId'],
                limit=10,
            )
            while pager.has_next():
                next_page = pager.get_next()
                assert next_page is not None
                all_results.extend(next_page)

            # end-list_instance_group_manager_actions

            print(json.dumps(all_results, indent=2))
            assert all_results is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_instance_group_manager_action_example(self):
        """
        create_instance_group_manager_action request example
        """
        try:
            print('\ncreate_instance_group_manager_action() result:')
            # begin-create_instance_group_manager_action

            instance_group_manager_scheduled_action_group_prototype_model = {}
            instance_group_manager_scheduled_action_group_prototype_model['membership_count'] = 5

            instance_group_manager_action_prototype_model = {}
            instance_group_manager_action_prototype_model['name'] = 'my-instance-group-manager-action'
            instance_group_manager_action_prototype_model['group'] = instance_group_manager_scheduled_action_group_prototype_model


            instance_group_manager_action = vpc_service.create_instance_group_manager_action(
                instance_group_id=data['instanceGroupId'],
                instance_group_manager_id=data['instanceGroupManagerId'],
                instance_group_manager_action_prototype=
                instance_group_manager_action_prototype_model).get_result()

            # end-create_instance_group_manager_action

            assert instance_group_manager_action is not None
            data['instanceGroupManagerActionId']=instance_group_manager_action['id']

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_instance_group_manager_action_example(self):
        """
        get_instance_group_manager_action request example
        """
        try:
            print('\nget_instance_group_manager_action() result:')
            # begin-get_instance_group_manager_action

            instance_group_manager_action = vpc_service.get_instance_group_manager_action(
                instance_group_id=data['instanceGroupId'],
                instance_group_manager_id=data['instanceGroupManagerId'],
                id=data['instanceGroupManagerActionId']).get_result()

            # end-get_instance_group_manager_action

            assert instance_group_manager_action is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_instance_group_manager_action_example(self):
        """
        update_instance_group_manager_action request example
        """
        try:
            print('\nupdate_instance_group_manager_action() result:')
            # begin-update_instance_group_manager_action

            instance_group_manager_action_patch_model = {}
            instance_group_manager_action_patch_model['name'] = 'my-instance-group-manager-action-updated'

            instance_group_manager_action = vpc_service.update_instance_group_manager_action(
                instance_group_id=data['instanceGroupId'],
                instance_group_manager_id=data['instanceGroupManagerId'],
                id=data['instanceGroupManagerActionId'],
                instance_group_manager_action_patch=
                instance_group_manager_action_patch_model).get_result()

            # end-update_instance_group_manager_action

            assert instance_group_manager_action is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_instance_group_manager_policies_example(self):
        """
        list_instance_group_manager_policies request example
        """
        try:
            print('\nlist_instance_group_manager_policies() result:')
            # begin-list_instance_group_manager_policies

            all_results = []
            pager = InstanceGroupManagerPoliciesPager(
                client=vpc_service,
                instance_group_id=data['instanceGroupId'],
                instance_group_manager_id=data['instanceGroupManagerId'],
                limit=10,
            )
            while pager.has_next():
                next_page = pager.get_next()
                assert next_page is not None
                all_results.extend(next_page)


            # end-list_instance_group_manager_policies

            print(json.dumps(all_results, indent=2))

            assert all_results is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_instance_group_manager_policy_example(self):
        """
        create_instance_group_manager_policy request example
        """
        try:
            print('\ncreate_instance_group_manager_policy() result:')
            # begin-create_instance_group_manager_policy

            instance_group_manager_policy_prototype_model = {}
            instance_group_manager_policy_prototype_model['metric_type'] = 'cpu'
            instance_group_manager_policy_prototype_model['metric_value'] = 20
            instance_group_manager_policy_prototype_model['policy_type'] = 'target'
            instance_group_manager_policy_prototype_model['name'] = 'my-instance-group-manager-policy'

            instance_group_manager_policy = vpc_service.create_instance_group_manager_policy(
                instance_group_id=data['instanceGroupId'],
                instance_group_manager_id=data['instanceGroupManagerId'],
                instance_group_manager_policy_prototype=
                instance_group_manager_policy_prototype_model).get_result()

            # end-create_instance_group_manager_policy

            assert instance_group_manager_policy is not None
            data['instanceGroupManagerPolicyId']=instance_group_manager_policy['id']

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_instance_group_manager_policy_example(self):
        """
        get_instance_group_manager_policy request example
        """
        try:
            print('\nget_instance_group_manager_policy() result:')
            # begin-get_instance_group_manager_policy

            instance_group_manager_policy = vpc_service.get_instance_group_manager_policy(
                instance_group_id=data['instanceGroupId'],
                instance_group_manager_id=data['instanceGroupManagerId'],
                id=data['instanceGroupManagerPolicyId']).get_result()

            # end-get_instance_group_manager_policy

            assert instance_group_manager_policy is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_instance_group_manager_policy_example(self):
        """
        update_instance_group_manager_policy request example
        """
        try:
            print('\nupdate_instance_group_manager_policy() result:')
            # begin-update_instance_group_manager_policy

            instance_group_manager_policy_patch_model = {}
            instance_group_manager_policy_patch_model['metric_type'] = 'cpu'
            instance_group_manager_policy_patch_model['metric_value'] = 70
            instance_group_manager_policy_patch_model['name'] = 'my-instance-group-manager-policy-updated'

            instance_group_manager_policy = vpc_service.update_instance_group_manager_policy(
                instance_group_id=data['instanceGroupId'],
                instance_group_manager_id=data['instanceGroupManagerId'],
                id=data['instanceGroupManagerPolicyId'],
                instance_group_manager_policy_patch=
                instance_group_manager_policy_patch_model).get_result()

            # end-update_instance_group_manager_policy

            assert instance_group_manager_policy is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_instance_group_memberships_example(self):
        """
        list_instance_group_memberships request example
        """
        try:
            print('\nlist_instance_group_memberships() result:')
            # begin-list_instance_group_memberships

            all_results = []
            pager = InstanceGroupMembershipsPager(
                client=vpc_service,
                instance_group_id=data['instanceGroupId'],
                limit=10,
            )
            while pager.has_next():
                next_page = pager.get_next()
                assert next_page is not None
                all_results.extend(next_page)

            # end-list_instance_group_memberships

            print(json.dumps(all_results, indent=2))
            assert all_results is not None
            data['instanceGroupMembershipId']=all_results[0]['id']

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_instance_group_membership_example(self):
        """
        get_instance_group_membership request example
        """
        try:
            print('\nget_instance_group_membership() result:')
            # begin-get_instance_group_membership

            instance_group_membership = vpc_service.get_instance_group_membership(
                instance_group_id=data['instanceGroupId'], id=data['instanceGroupMembershipId']).get_result()

            # end-get_instance_group_membership

            assert instance_group_membership is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_instance_group_membership_example(self):
        """
        update_instance_group_membership request example
        """
        try:
            print('\nupdate_instance_group_membership() result:')
            # begin-update_instance_group_membership

            instance_group_membership_patch_model = {}
            instance_group_membership_patch_model['name'] = 'my-instance-group-membership-updated'

            instance_group_membership = vpc_service.update_instance_group_membership(
                instance_group_id=data['instanceGroupId'],
                id=data['instanceGroupMembershipId'],
                instance_group_membership_patch=
                instance_group_membership_patch_model).get_result()

            # end-update_instance_group_membership

            assert instance_group_membership is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_dedicated_host_groups_example(self):
        """
        list_dedicated_host_groups request example
        """
        try:
            print('\nlist_dedicated_host_groups() result:')
            # begin-list_dedicated_host_groups

            all_results = []
            pager = DedicatedHostGroupsPager(
                client=vpc_service,
                limit=10,
                zone_name='us-south-2',
            )
            while pager.has_next():
                next_page = pager.get_next()
                assert next_page is not None
                all_results.extend(next_page)

            # end-list_dedicated_host_groups

            print(json.dumps(all_results, indent=2))

            assert all_results is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_dedicated_host_group_example(self):
        """
        create_dedicated_host_group request example
        """
        try:
            print('\ncreate_dedicated_host_group() result:')
            # begin-create_dedicated_host_group

            zone_identity_model = {}
            zone_identity_model['name'] = data['zone']

            dedicated_host_group = vpc_service.create_dedicated_host_group(
                class_='mx2', family='balanced', zone=zone_identity_model,name='my-dedicated-host-group').get_result()

            # end-create_dedicated_host_group

            assert dedicated_host_group is not None
            data['dedicatedHostGroupId']=dedicated_host_group['id']

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_dedicated_host_group_example(self):
        """
        get_dedicated_host_group request example
        """
        try:
            print('\nget_dedicated_host_group() result:')
            # begin-get_dedicated_host_group

            dedicated_host_group = vpc_service.get_dedicated_host_group(
                id=data['dedicatedHostGroupId']).get_result()

            # end-get_dedicated_host_group

            assert dedicated_host_group is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_dedicated_host_group_example(self):
        """
        update_dedicated_host_group request example
        """
        try:
            print('\nupdate_dedicated_host_group() result:')
            # begin-update_dedicated_host_group

            dedicated_host_group_patch_model = {}
            dedicated_host_group_patch_model['name'] = 'my-host-group-updated'

            dedicated_host_group = vpc_service.update_dedicated_host_group(
                id=data['dedicatedHostGroupId'],
                dedicated_host_group_patch=dedicated_host_group_patch_model
            ).get_result()

            # end-update_dedicated_host_group

            assert dedicated_host_group is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_dedicated_host_profiles_example(self):
        """
        list_dedicated_host_profiles request example
        """
        try:
            print('\nlist_dedicated_host_profiles() result:')
            # begin-list_dedicated_host_profiles

            all_results = []
            pager = DedicatedHostProfilesPager(
                client=vpc_service,
                limit=10,
            )
            while pager.has_next():
                next_page = pager.get_next()
                assert next_page is not None
                all_results.extend(next_page)

            # end-list_dedicated_host_profiles

            print(json.dumps(all_results, indent=2))
            assert all_results is not None
            data['dhProfile']="mx2d-host-152x1216"

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_dedicated_host_profile_example(self):
        """
        get_dedicated_host_profile request example
        """
        try:
            print('\nget_dedicated_host_profile() result:')
            # begin-get_dedicated_host_profile

            dedicated_host_profile = vpc_service.get_dedicated_host_profile(
                name=data['dhProfile']).get_result()

            print(json.dumps(dedicated_host_profile, indent=2))
            # end-get_dedicated_host_profile

            assert dedicated_host_profile is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_dedicated_hosts_example(self):
        """
        list_dedicated_hosts request example
        """
        try:
            print('\nlist_dedicated_hosts() result:')
            # begin-list_dedicated_hosts

            all_results = []
            pager = DedicatedHostsPager(
                client=vpc_service,
                limit=10,
                zone_name='us-south-2',
            )
            while pager.has_next():
                next_page = pager.get_next()
                assert next_page is not None
                all_results.extend(next_page)

            # end-list_dedicated_hosts

            print(json.dumps(all_results, indent=2))

            assert all_results is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_dedicated_host_example(self):
        """
        create_dedicated_host request example
        """
        try:
            print('\ncreate_dedicated_host() result:')
            # begin-create_dedicated_host

            dedicated_host_profile_identity_model = {}
            dedicated_host_profile_identity_model['name'] = data['dhProfile']

            dedicated_host_group_identity_model = {}
            dedicated_host_group_identity_model['id'] = data['dedicatedHostGroupId']

            dedicated_host_prototype_model = {}
            dedicated_host_prototype_model['profile'] = dedicated_host_profile_identity_model
            dedicated_host_prototype_model['group'] = dedicated_host_group_identity_model
            dedicated_host_prototype_model['name'] = 'my-dedicated-host'

            dedicated_host = vpc_service.create_dedicated_host(
                dedicated_host_prototype=dedicated_host_prototype_model
            ).get_result()

            # end-create_dedicated_host

            assert dedicated_host is not None
            data['dedicatedHostId']=dedicated_host['id']

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_dedicated_host_example(self):
        """
        get_dedicated_host request example
        """
        try:
            print('\nget_dedicated_host() result:')
            # begin-get_dedicated_host

            dedicated_host = vpc_service.get_dedicated_host(
                id=data['dedicatedHostId']).get_result()

            # end-get_dedicated_host

            assert dedicated_host is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_dedicated_host_disks_example(self):
        """
        list_dedicated_host_disks request example
        """
        try:
            print('\nlist_dedicated_host_disks() result:')

            dedicated_host_collection = vpc_service.list_dedicated_hosts(
            ).get_result()

            assert dedicated_host_collection is not None

            for dh in dedicated_host_collection['dedicated_hosts']:
                if len(dh['disks'])>0:
                    data['dhId']=dh['id']
                    break

            # begin-list_dedicated_host_disks


            dedicated_host_disk_collection = vpc_service.list_dedicated_host_disks(
                dedicated_host_id=data['dedicatedHostId']).get_result()

            # end-list_dedicated_host_disks

            assert dedicated_host_disk_collection is not None
            data['diskId']=dedicated_host_disk_collection['disks'][0]['id']

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_dedicated_host_disk_example(self):
        """
        get_dedicated_host_disk request example
        """
        try:
            print('\nget_dedicated_host_disk() result:')
            # begin-get_dedicated_host_disk

            dedicated_host_disk = vpc_service.get_dedicated_host_disk(
                dedicated_host_id=data['dedicatedHostId'], id=data['diskId']).get_result()

            # end-get_dedicated_host_disk

            assert dedicated_host_disk is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_dedicated_host_disk_example(self):
        """
        update_dedicated_host_disk request example
        """
        try:
            print('\nupdate_dedicated_host_disk() result:')
            # begin-update_dedicated_host_disk

            dedicated_host_disk_patch_model = {}
            dedicated_host_disk_patch_model['name'] = 'my-disk-updated'

            dedicated_host_disk = vpc_service.update_dedicated_host_disk(
                dedicated_host_id=data['dedicatedHostId'],
                id=data['diskId'],
                dedicated_host_disk_patch=dedicated_host_disk_patch_model
            ).get_result()

            # end-update_dedicated_host_disk

            assert dedicated_host_disk is not None

        except ApiException as e:
            pytest.fail(str(e))


    @needscredentials
    def test_update_dedicated_host_example(self):
        """
        update_dedicated_host request example
        """
        try:
            print('\nupdate_dedicated_host() result:')
            # begin-update_dedicated_host

            dedicated_host_patch_model = {}
            dedicated_host_patch_model['name'] = 'my-dedicated-host-updated'
            dedicated_host_patch_model['instance_placement_enabled'] = False

            dedicated_host = vpc_service.update_dedicated_host(
                id=data['dedicatedHostId'],
                dedicated_host_patch=dedicated_host_patch_model).get_result()

            # end-update_dedicated_host

            assert dedicated_host is not None

        except ApiException as e:
            pytest.fail(str(e))


    @needscredentials
    def test_list_snapshots_example(self):
        """
        list_snapshots request example
        """
        try:
            print('\nlist_snapshots() result:')
            # begin-list_snapshots

            all_results = []
            pager = SnapshotsPager(
                client=vpc_service,
                limit=10,
            )
            while pager.has_next():
                next_page = pager.get_next()
                assert next_page is not None
                all_results.extend(next_page)

            # end-list_snapshots

            print(json.dumps(all_results, indent=2))

            assert all_results is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_snapshot_example(self):
        """
        create_snapshot request example
        """
        try:
            print('\ncreate_snapshot() result:')
            zoneName = data['zone']
            # begin-create_snapshot

            volume_identity_model = {}
            volume_identity_model['id'] = data['volumeId']
            zone_identity_model = {
                'name': zoneName,
            }

            snapshot_clone_prototype_model = {
                'zone': zone_identity_model,
            }
            
            snapshot_prototype_model = {
                'clones': [snapshot_clone_prototype_model],
                'source_volume': volume_identity_model,
                'name': 'my-snapshot-1'
            }
            snapshot = vpc_service.create_snapshot(
                snapshot_prototype=snapshot_prototype_model).get_result()

            # end-create_snapshot

            assert snapshot is not None
            data['snapshotId']=snapshot['id']
            data['snapshotCRN']=snapshot['crn']
            volume_identity_model = {}
            volume_identity_model['id'] = data['volumeId']

            
            snapshot_prototype_model = {
                'source_volume': volume_identity_model,
                'name': 'my-snapshot-2'
            }
            snapshot = vpc_service.create_snapshot(
                snapshot_prototype=snapshot_prototype_model)
            
            # copy snapshot
            snapshot_identity_by_crn_model = {}  # SnapshotIdentityByCRN
            snapshot_identity_by_crn_model['crn'] = data['snapshotCRN']
            source_snapshot_prototype_model = {
                'source_snapshot' : snapshot_identity_by_crn_model,
                'name': 'source-snapshot-copy'
            }
            snapshotCRC = vpc_service.create_snapshot(
                snapshot_prototype=source_snapshot_prototype_model)
            assert snapshotCRC is not None
            print(snapshotCRC)
        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_snapshot_example(self):
        """
        get_snapshot request example
        """
        try:
            print('\nget_snapshot() result:')
            # begin-get_snapshot

            snapshot = vpc_service.get_snapshot(id=data['snapshotId']).get_result()

            # end-get_snapshot

            assert snapshot is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_snapshot_example(self):
        """
        update_snapshot request example
        """
        try:
            print('\nupdate_snapshot() result:')
            # begin-update_snapshot

            snapshot_patch_model = {}
            snapshot_patch_model['name'] = 'my-snapshot-updated'

            snapshot = vpc_service.update_snapshot(
                id=data['snapshotId'],
                snapshot_patch=snapshot_patch_model).get_result()

            # end-update_snapshot

            assert snapshot is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_snapshot_clones_example(self):
        """
        list_snapshot_clones request example
        """
        try:
            print('\nlist_snapshot_clones() result:')
            snapshotID = data['snapshotId']
            # begin-list_snapshot_clones

            response = vpc_service.list_snapshot_clones(
                id=snapshotID,
            )
            snapshot_clone_collection = response.get_result()

            print(json.dumps(snapshot_clone_collection, indent=2))

            # end-list_snapshot_clones
    
        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_snapshot_clone_example(self):
        """
        get_snapshot_clone request example
        """
        try:
            print('\nget_snapshot_clone() result:')
            zoneName = data['zone']
            snapshotID = data['snapshotId']
            # begin-get_snapshot_clone

            response = vpc_service.get_snapshot_clone(
                id=snapshotID,
                zone_name=zoneName,
            )
            snapshot_clone = response.get_result()

            print(json.dumps(snapshot_clone, indent=2))

            # end-get_snapshot_clone

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_snapshot_clone_example(self):
        """
        create_snapshot_clone request example
        """
        try:
            print('\ncreate_snapshot_clone() result:')
            zoneName = data['zone']
            snapshotID = data['snapshotId']
            # begin-create_snapshot_clone

            response = vpc_service.create_snapshot_clone(
                id=snapshotID,
                zone_name=zoneName,
            )
            snapshot_clone = response.get_result()

            print(json.dumps(snapshot_clone, indent=2))

            # end-create_snapshot_clone

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_share_profiles_example(self):
        """
        list_share_profiles request example
        """
        try:
            print('\nlist_share_profiles() result:')
            # begin-list_share_profiles

            all_results = []
            pager = ShareProfilesPager(
                client=vpc_service,
                limit=10,
                sort='name',
            )
            while pager.has_next():
                next_page = pager.get_next()
                assert next_page is not None
                all_results.extend(next_page)


            # end-list_share_profiles
            print(json.dumps(all_results, indent=2))
            data['shareProfileName'] = all_results[0]['name']
            assert all_results is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_share_profile_example(self):
        """
        get_share_profile request example
        """
        try:
            print('\nget_share_profile() result:')
            # begin-get_share_profile

            response = vpc_service.get_share_profile(
                name=data['shareProfileName'],
            )
            share_profile = response.get_result()


            # end-get_share_profile
            print(json.dumps(share_profile, indent=2))
            assert share_profile is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_shares_example(self):
        """
        list_shares request example
        """
        try:
            print('\nlist_shares() result:')
            # begin-list_shares

            all_results = []
            pager = SharesPager(
                client=vpc_service,
                limit=10,
                sort='name',
            )
            while pager.has_next():
                next_page = pager.get_next()
                assert next_page is not None
                all_results.extend(next_page)


            # end-list_shares
            print(json.dumps(all_results, indent=2))
            assert all_results is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_share_example(self):
        """
        create_share request example
        """
        try:
            print('\ncreate_share() result:')
            # begin-create_share

            share_profile_identity_model = {
                'name': data['shareProfileName'],
            }

            zone_identity_model = {
                'name': 'us-east-1',
            }

            share_prototype_model = {
                'profile': share_profile_identity_model,
                'zone': zone_identity_model,
                'size': 200,
                'name': 'my-share',
            }

            response = vpc_service.create_share(
                share_prototype=share_prototype_model,
            )
            share = response.get_result()

            #replica share
            source_share_prototype_model = {
                'id': share['id'],
            }
            share_replica_prototype_model = {
                'profile': share_profile_identity_model,
                'zone': zone_identity_model,
                'replication_cron_spec': '0 */5 * * *',
                'source_share': source_share_prototype_model,
                'name': 'my-share-replica',
            }

            response_replica = vpc_service.create_share(
                share_prototype=share_replica_prototype_model,
            )
            share_replica = response_replica.get_result()
            # end-create_share
            print(json.dumps(share, indent=2))
            data['shareId']=share['id']
            data['shareCRN']=share['crn']
            data['shareReplicaId']=share_replica['id']
            data['shareReplicaETag']=response_replica.get_headers()['ETag']
            assert share is not None
            assert share_replica is not None
            

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_accessor_share_example(self):
        """
        create_share request example
        """
        try:
            print('\ncreate_share() result:')
            # begin-create_share

            share_identity = {
                'crn': data["shareCRN"]
            }
            share_prototype_model = {
                'origin_share': share_identity,
                'name': 'my-accessor-share',
            }

            response = vpc_service.create_share(
                share_prototype=share_prototype_model,
            )
            share = response.get_result()

            # end-create_share
            data['shareAccessorId']=share['id']
            assert share is not None
            

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_share_example(self):
        """
        get_share request example
        """
        try:
            print('\nget_share() result:')
            # begin-get_share

            response = vpc_service.get_share(
                id=data['shareId'],
            )
            share = response.get_result()


            # end-get_share
            print(json.dumps(share, indent=2))
            data['shareETag'] = response.get_headers()['ETag']
            assert share is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_share_example(self):
        """
        update_share request example
        """
        try:
            print('\nupdate_share() result:')
            # begin-update_share

            share_patch_model = {
            }
            share_patch_model['name'] = 'my-share-updated'

            response = vpc_service.update_share(
                id=data['shareId'],
                share_patch=share_patch_model,
                if_match=data['shareETag'],
            )
            share = response.get_result()


            # end-update_share
            print(json.dumps(share, indent=2))
            data['shareETag'] = response.get_headers()['ETag']
            assert share is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_share_accessor_bindings_example(self):
        """
        list_share_accessor_bindings request example
        """
        try:
            print('\nlist_share_accessor_bindings() result:')

            # begin-list_share_accessor_bindings

            all_results = []
            pager = ShareAccessorBindingsPager(
                client=vpc_service,
                id=data['shareId'],
                limit=10,
            )
            while pager.has_next():
                next_page = pager.get_next()
                assert next_page is not None
                all_results.extend(next_page)

            # end-list_share_accessor_bindings
            data['shareAccessorBindingId'] = all_results[0]['id']
        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_share_accessor_binding_example(self):
        """
        get_share_accessor_binding request example
        """
        try:
            print('\nget_share_accessor_binding() result:')

            # begin-get_share_accessor_binding

            response = vpc_service.get_share_accessor_binding(
                share_id=data['shareId'],
                id=data['shareAccessorBindingId'],
            )
            share_accessor_binding = response.get_result()

            print(json.dumps(share_accessor_binding, indent=2))

            # end-get_share_accessor_binding
            assert share_accessor_binding is not None
        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_share_accessor_binding_example(self):
        """
        delete_share_accessor_binding request example
        """
        try:
            # begin-delete_share_accessor_binding

            response = vpc_service.delete_share_accessor_binding(
                share_id=data['shareId'],
                id=data['shareAccessorBindingId'],
            )

            # end-delete_share_accessor_binding
            print('\ndelete_share_accessor_binding() response status code: ',
                  response.get_status_code())

        except ApiException as e:
            pytest.fail(str(e))
    @needscredentials
    def test_failover_share_example(self):
        """
        failover_share request example
        """
        try:
            # begin-failover_share

            response = vpc_service.failover_share(
                share_id=data['shareReplicaId'],
            )

            # end-failover_share
            print('\nfailover_share() response status code: ', response.get_status_code())
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_share_mount_targets_example(self):
        """
        list_share_mount_targets request example
        """
        try:
            print('\nlist_share_mount_targets() result:')
            # begin-list_share_mount_targets

            all_results = []
            pager = ShareMountTargetsPager(
                client=vpc_service,
                share_id=data['shareId'],
                limit=10,
            )
            while pager.has_next():
                next_page = pager.get_next()
                assert next_page is not None
                all_results.extend(next_page)


            # end-list_share_mount_targets
            print(json.dumps(all_results, indent=2))
            assert all_results is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_share_mount_target_example(self):
        """
        create_share_mount_target request example
        """
        try:
            print('\ncreate_share_mount_target() result:')
            # begin-create_share_mount_target
            subnet_prototype_model = {
                'id': data['subnetId'],
            }
            share_mount_target_virtual_network_interface_prototype_model = {
                'name': 'my-share-mount-target-vni',
                'subnet': subnet_prototype_model,
            }

            share_mount_target_prototype_model = {
                'virtual_network_interface': share_mount_target_virtual_network_interface_prototype_model,
                'name': 'my-share-mount-target',
            }

            response = vpc_service.create_share_mount_target(
                share_id=data['shareId'],
                share_mount_target_prototype=share_mount_target_prototype_model,
            )
            share_mount_target = response.get_result()


            # end-create_share_mount_target
            print(json.dumps(share_mount_target, indent=2))
            data['shareMountTargetId'] = share_mount_target['id']
            assert share_mount_target is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_share_mount_target_example(self):
        """
        get_share_mount_target request example
        """
        try:
            print('\nget_share_mount_target() result:')
            # begin-get_share_mount_target

            response = vpc_service.get_share_mount_target(
                share_id=data['shareId'],
                id=data['shareMountTargetId'],
            )
            share_mount_target = response.get_result()


            # end-get_share_mount_target
            print(json.dumps(share_mount_target, indent=2))
            assert share_mount_target is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_share_mount_target_example(self):
        """
        update_share_mount_target request example
        """
        try:
            print('\nupdate_share_mount_target() result:')
            # begin-update_share_mount_target

            share_mount_target_patch_model = {
            }
            share_mount_target_patch_model['name'] = 'my-share-mount-target-updated'

            response = vpc_service.update_share_mount_target(
                share_id=data['shareId'],
                id=data['shareMountTargetId'],
                share_mount_target_patch=share_mount_target_patch_model,
            )
            share_mount_target = response.get_result()


            # end-update_share_mount_target
            print(json.dumps(share_mount_target, indent=2))
            assert share_mount_target is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    @pytest.mark.skip(reason="mock")
    def test_get_share_source_example(self):
        """
        get_share_source request example
        """
        try:
            print('\nget_share_source() result:')
            # begin-get_share_source

            response = vpc_service.get_share_source(
                share_id=data['shareReplicaId'],
            )
            share = response.get_result()


            # end-get_share_source
            print(json.dumps(share, indent=2))
            assert share is not None

        except ApiException as e:
            pytest.fail(str(e))


    @needscredentials
    def test_list_regions_example(self):
        """
        list_regions request example
        """
        try:
            print('\nlist_regions() result:')
            # begin-list_regions

            region_collection = vpc_service.list_regions().get_result()

            # end-list_regions

            assert region_collection is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_region_example(self):
        """
        get_region request example
        """
        try:
            print('\nget_region() result:')
            # begin-get_region

            region = vpc_service.get_region(name='us-east').get_result()

            # end-get_region

            assert region is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_region_zones_example(self):
        """
        list_region_zones request example
        """
        try:
            print('\nlist_region_zones() result:')
            # begin-list_region_zones

            zone_collection = vpc_service.list_region_zones(
                region_name='us-east').get_result()

            # end-list_region_zones

            assert zone_collection is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_region_zone_example(self):
        """
        get_region_zone request example
        """
        try:
            print('\nget_region_zone() result:')
            # begin-get_region_zone

            zone = vpc_service.get_region_zone(region_name='us-east',
                                               name='us-east-1').get_result()

            # end-get_region_zone

            assert zone is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_public_gateways_example(self):
        """
        list_public_gateways request example
        """
        try:
            print('\nlist_public_gateways() result:')
            # begin-list_public_gateways

            all_results = []
            pager = PublicGatewaysPager(
                client=vpc_service,
                limit=10,
            )
            while pager.has_next():
                next_page = pager.get_next()
                assert next_page is not None
                all_results.extend(next_page)

            # end-list_public_gateways

            print(json.dumps(all_results, indent=2))
            assert all_results is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_public_gateway_example(self):
        """
        create_public_gateway request example
        """
        try:
            print('\ncreate_public_gateway() result:')
            # begin-create_public_gateway

            vpc_identity_model = {}
            vpc_identity_model['id'] = data['vpcID']

            zone_identity_model = {}
            zone_identity_model['name'] = data['zone']

            public_gateway = vpc_service.create_public_gateway(
                vpc=vpc_identity_model,
                zone=zone_identity_model,
                name='my-public-gateway').get_result()

            # end-create_public_gateway

            assert public_gateway is not None
            data['publicGatewayId']=public_gateway['id']

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_public_gateway_example(self):
        """
        get_public_gateway request example
        """
        try:
            print('\nget_public_gateway() result:')
            # begin-get_public_gateway

            public_gateway = vpc_service.get_public_gateway(
                id=data['publicGatewayId']).get_result()

            # end-get_public_gateway

            assert public_gateway is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_public_gateway_example(self):
        """
        update_public_gateway request example
        """
        try:
            print('\nupdate_public_gateway() result:')
            # begin-update_public_gateway

            public_gateway_patch_model = {}
            public_gateway_patch_model['name'] = 'my-public-gateway-updated'

            public_gateway = vpc_service.update_public_gateway(
                id=data['publicGatewayId'],
                public_gateway_patch=public_gateway_patch_model).get_result()

            # end-update_public_gateway

            assert public_gateway is not None

        except ApiException as e:
            pytest.fail(str(e))


    @needscredentials
    def test_list_network_acls_example(self):
        """
        list_network_acls request example
        """
        try:
            print('\nlist_network_acls() result:')
            # begin-list_network_acls

            all_results = []
            pager = NetworkAclsPager(
                client=vpc_service,
                limit=10,
            )
            while pager.has_next():
                next_page = pager.get_next()
                assert next_page is not None
                all_results.extend(next_page)

            # end-list_network_acls

            print(json.dumps(all_results, indent=2))
            assert all_results is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_network_acl_example(self):
        """
        create_network_acl request example
        """
        try:
            print('\ncreate_network_acl() result:')
            # begin-create_network_acl

            vpc_identity_model = {}
            vpc_identity_model['id'] = data['vpcID']

            network_acl_prototype_model_rules = {}
            network_acl_prototype_model_rules['name'] = ['my-network-acl-rule']
            network_acl_prototype_model_rules['action'] = ['allow']
            network_acl_prototype_model_rules['destination'] = ['192.168.3.2/32']
            network_acl_prototype_model_rules['direction'] = ['inbound']
            network_acl_prototype_model_rules['source'] = ['192.168.3.2/32']
            network_acl_prototype_model_rules['protocol'] = ['tcp']

            network_acl_prototype_model = {}
            network_acl_prototype_model['name'] = 'my-network-acl-rule',
            network_acl_prototype_model['vpc'] = vpc_identity_model,
            network_acl_prototype_model['rules'] = [network_acl_prototype_model_rules]

            network_acl = vpc_service.create_network_acl(
                network_acl_prototype=network_acl_prototype_model).get_result()

            # end-create_network_acl

            assert network_acl is not None
            data['networkACLId']=network_acl['id']

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_network_acl_example(self):
        """
        get_network_acl request example
        """
        try:
            print('\nget_network_acl() result:')
            # begin-get_network_acl

            network_acl = vpc_service.get_network_acl(
                id=data['networkACLId']).get_result()

            # end-get_network_acl

            assert network_acl is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_network_acl_example(self):
        """
        update_network_acl request example
        """
        try:
            print('\nupdate_network_acl() result:')
            # begin-update_network_acl

            network_acl_patch_model = {}
            network_acl_patch_model['name'] = 'my-network-acl-updated'

            network_acl = vpc_service.update_network_acl(
                id=data['networkACLId'],
                network_acl_patch=network_acl_patch_model).get_result()

            # end-update_network_acl

            assert network_acl is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_network_acl_rules_example(self):
        """
        list_network_acl_rules request example
        """
        try:
            print('\nlist_network_acl_rules() result:')
            # begin-list_network_acl_rules

            all_results = []
            pager = NetworkAclRulesPager(
                client=vpc_service,
                network_acl_id=data['networkACLId'],
                limit=10,
                direction='inbound',
            )
            while pager.has_next():
                next_page = pager.get_next()
                assert next_page is not None
                all_results.extend(next_page)

            # end-list_network_acl_rules

            print(json.dumps(all_results, indent=2))
            assert all_results is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_network_acl_rule_example(self):
        """
        create_network_acl_rule request example
        """
        try:
            print('\ncreate_network_acl_rule() result:')
            # begin-create_network_acl_rule

            network_acl_rule_prototype_model = {}
            network_acl_rule_prototype_model['name'] = 'my-network-acl-rule'
            network_acl_rule_prototype_model['action'] = 'allow'
            network_acl_rule_prototype_model['destination'] = '192.168.3.2/32'
            network_acl_rule_prototype_model['direction'] = 'inbound'
            network_acl_rule_prototype_model['source'] = '192.168.3.2/32'
            network_acl_rule_prototype_model['protocol'] = 'all'
            network_acl_rule_prototype_model['code'] = 0
            network_acl_rule_prototype_model['type'] = 8

            network_acl_rule = vpc_service.create_network_acl_rule(
                network_acl_id=data['networkACLId'],
                network_acl_rule_prototype=network_acl_rule_prototype_model
            ).get_result()

            # end-create_network_acl_rule

            assert network_acl_rule is not None
            data['networkACLRuleId']=network_acl_rule['id']

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_network_acl_rule_example(self):
        """
        get_network_acl_rule request example
        """
        try:
            print('\nget_network_acl_rule() result:')
            # begin-get_network_acl_rule

            network_acl_rule = vpc_service.get_network_acl_rule(
                network_acl_id=data['networkACLId'], id=data['networkACLRuleId']).get_result()

            # end-get_network_acl_rule

            assert network_acl_rule is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_network_acl_rule_example(self):
        """
        update_network_acl_rule request example
        """
        try:
            print('\nupdate_network_acl_rule() result:')
            # begin-update_network_acl_rule

            network_acl_rule_patch_model = {}
            network_acl_rule_patch_model['name'] = 'my-network-acl-rule-updated'

            network_acl_rule = vpc_service.update_network_acl_rule(
                network_acl_id=data['networkACLId'],
                id=data['networkACLRuleId'],
                network_acl_rule_patch=network_acl_rule_patch_model).get_result(
                )

            # end-update_network_acl_rule

            assert network_acl_rule is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_security_groups_example(self):
        """
        list_security_groups request example
        """
        try:
            print('\nlist_security_groups() result:')
            # begin-list_security_groups

            all_results = []
            pager = SecurityGroupsPager(
                client=vpc_service,
                limit=10,
                vpc_id=data['vpcID'],
            )
            while pager.has_next():
                next_page = pager.get_next()
                assert next_page is not None
                all_results.extend(next_page)

            # end-list_security_groups

            print(json.dumps(all_results, indent=2))

            assert all_results is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_security_group_example(self):
        """
        create_security_group request example
        """
        try:
            print('\ncreate_security_group() result:')
            # begin-create_security_group

            vpc_identity_model = {}
            vpc_identity_model['id'] = data['vpcID']

            security_group = vpc_service.create_security_group(vpc=vpc_identity_model,name='my-security-group').get_result()

            # end-create_security_group

            assert security_group is not None
            data['securityGroupId']=security_group['id']

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_security_group_example(self):
        """
        get_security_group request example
        """
        try:
            print('\nget_security_group() result:')
            # begin-get_security_group

            security_group = vpc_service.get_security_group(
                id=data['securityGroupId']).get_result()

            # end-get_security_group

            assert security_group is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_security_group_example(self):
        """
        update_security_group request example
        """
        try:
            print('\nupdate_security_group() result:')
            # begin-update_security_group

            security_group_patch_model = {}
            security_group_patch_model['name'] = 'my-security-group-updated'

            security_group = vpc_service.update_security_group(
                id=data['securityGroupId'],
                security_group_patch=security_group_patch_model).get_result()

            # end-update_security_group

            assert security_group is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_security_group_rules_example(self):
        """
        list_security_group_rules request example
        """
        try:
            print('\nlist_security_group_rules() result:')
            # begin-list_security_group_rules

            security_group_rule_collection = vpc_service.list_security_group_rules(
                security_group_id=data['securityGroupId']).get_result()

            # end-list_security_group_rules

            assert security_group_rule_collection is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_security_group_rule_example(self):
        """
        create_security_group_rule request example
        """
        try:
            print('\ncreate_security_group_rule() result:')
            # begin-create_security_group_rule

            security_group_rule_prototype_model_remote = {}
            security_group_rule_prototype_model_remote['address'] = '192.168.3.4'

            security_group_rule_prototype_model = {}
            security_group_rule_prototype_model['direction'] = 'inbound'
            security_group_rule_prototype_model['protocol'] = 'tcp'
            security_group_rule_prototype_model['code'] = 0
            security_group_rule_prototype_model['type'] = 8
            security_group_rule_prototype_model['ip_version'] = 'ipv4'
            security_group_rule_prototype_model['remote'] = security_group_rule_prototype_model_remote

            security_group_rule = vpc_service.create_security_group_rule(
                security_group_id=data['securityGroupId'],
                security_group_rule_prototype=security_group_rule_prototype_model
            ).get_result()

            # end-create_security_group_rule

            assert security_group_rule is not None
            data['securityGroupRuleId']=security_group_rule['id']

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_security_group_rule_example(self):
        """
        get_security_group_rule request example
        """
        try:
            print('\nget_security_group_rule() result:')
            # begin-get_security_group_rule

            security_group_rule = vpc_service.get_security_group_rule(
                security_group_id=data['securityGroupId'], id=data['securityGroupRuleId']).get_result()

            # end-get_security_group_rule

            assert security_group_rule is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_security_group_rule_example(self):
        """
        update_security_group_rule request example
        """
        try:
            print('\nupdate_security_group_rule() result:')
            # begin-update_security_group_rule

            security_group_rule_patch_model = {}
            security_group_rule_patch_model['direction'] = 'outbound'

            security_group_rule = vpc_service.update_security_group_rule(
                security_group_id=data['securityGroupId'],
                id=data['securityGroupRuleId'],
                security_group_rule_patch=security_group_rule_patch_model
            ).get_result()

            # end-update_security_group_rule

            assert security_group_rule is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_security_group_targets_example(self):
        """
        list_security_group_targets request example
        """
        try:
            print('\nlist_security_group_targets() result:')
            # begin-list_security_group_targets

            all_results = []
            pager = SecurityGroupTargetsPager(
                client=vpc_service,
                security_group_id=data['securityGroupId'],
                limit=10,
            )
            while pager.has_next():
                next_page = pager.get_next()
                assert next_page is not None
                all_results.extend(next_page)


            # end-list_security_group_targets

            print(json.dumps(all_results, indent=2))

            assert all_results is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_security_group_target_binding_example(self):
        """
        create_security_group_target_binding request example
        """
        try:
            print('\ncreate_security_group_target_binding() result:')
            # begin-create_security_group_target_binding

            security_group_target_reference = vpc_service.create_security_group_target_binding(
                security_group_id=data['securityGroupId'], id=data['eth2Id']).get_result()

            # end-create_security_group_target_binding

            assert security_group_target_reference is not None
            data['targetId']=security_group_target_reference['id']

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_security_group_target_example(self):
        """
        get_security_group_target request example
        """
        try:
            print('\nget_security_group_target() result:')
            # begin-get_security_group_target

            security_group_target_reference = vpc_service.get_security_group_target(
                security_group_id=data['securityGroupId'], id=data['targetId']).get_result()

            # end-get_security_group_target

            assert security_group_target_reference is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_ike_policies_example(self):
        """
        list_ike_policies request example
        """
        try:
            print('\nlist_ike_policies() result:')
            # begin-list_ike_policies

            all_results = []
            pager = IkePoliciesPager(
                client=vpc_service,
                limit=10,
            )
            while pager.has_next():
                next_page = pager.get_next()
                assert next_page is not None
                all_results.extend(next_page)


            # end-list_ike_policies

            print(json.dumps(all_results, indent=2))

            assert all_results is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_ike_policy_example(self):
        """
        create_ike_policy request example
        """
        try:
            print('\ncreate_ike_policy() result:')
            # begin-create_ike_policy

            ike_policy = vpc_service.create_ike_policy(
                authentication_algorithm='sha256',
                dh_group=14,
                encryption_algorithm='aes128',
                ike_version=1,
                name='my-ike-policy').get_result()

            # end-create_ike_policy

            assert ike_policy is not None
            data['ikePolicyId']=ike_policy['id']

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_ike_policy_example(self):
        """
        get_ike_policy request example
        """
        try:
            print('\nget_ike_policy() result:')
            # begin-get_ike_policy

            ike_policy = vpc_service.get_ike_policy(
                id=data['ikePolicyId']).get_result()

            # end-get_ike_policy

            assert ike_policy is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_ike_policy_example(self):
        """
        update_ike_policy request example
        """
        try:
            print('\nupdate_ike_policy() result:')
            # begin-update_ike_policy

            ike_policy_patch_model = {}
            ike_policy_patch_model['name'] = 'my-ike-policy-modified'
            ike_policy_patch_model['dh_group'] = 15

            ike_policy = vpc_service.update_ike_policy(
                id=data['ikePolicyId'],
                ike_policy_patch=ike_policy_patch_model).get_result()

            # end-update_ike_policy

            assert ike_policy is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_ike_policy_connections_example(self):
        """
        list_ike_policy_connections request example
        """
        try:
            print('\nlist_ike_policy_connections() result:')
            # begin-list_ike_policy_connections

            vpn_gateway_connection_collection = vpc_service.list_ike_policy_connections(
                id=data['ikePolicyId']).get_result()

            # end-list_ike_policy_connections

            assert vpn_gateway_connection_collection is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_ipsec_policies_example(self):
        """
        list_ipsec_policies request example
        """
        try:
            print('\nlist_ipsec_policies() result:')
            # begin-list_ipsec_policies

            all_results = []
            pager = IpsecPoliciesPager(
                client=vpc_service,
                limit=10,
            )
            while pager.has_next():
                next_page = pager.get_next()
                assert next_page is not None
                all_results.extend(next_page)


            # end-list_ipsec_policies

            print(json.dumps(all_results, indent=2))

            assert all_results is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_ipsec_policy_example(self):
        """
        create_ipsec_policy request example
        """
        try:
            print('\ncreate_ipsec_policy() result:')
            # begin-create_ipsec_policy

            i_psec_policy = vpc_service.create_ipsec_policy(
                authentication_algorithm='sha256',
                encryption_algorithm='aes128',
                pfs='disabled',key_lifetime=3600,
                name='my-ipsec-policy').get_result()

            # end-create_ipsec_policy

            assert i_psec_policy is not None
            data['ipsecPolicyId']=i_psec_policy['id']

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_ipsec_policy_example(self):
        """
        get_ipsec_policy request example
        """
        try:
            print('\nget_ipsec_policy() result:')
            # begin-get_ipsec_policy

            i_psec_policy = vpc_service.get_ipsec_policy(
                id=data['ipsecPolicyId']).get_result()

            # end-get_ipsec_policy

            assert i_psec_policy is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_ipsec_policy_example(self):
        """
        update_ipsec_policy request example
        """
        try:
            print('\nupdate_ipsec_policy() result:')
            # begin-update_ipsec_policy

            i_psec_policy_patch_model = {}
            i_psec_policy_patch_model['name'] = 'my-ipsec-policy-updated'
            i_psec_policy_patch_model['authentication_algorithm'] = 'sha256'

            i_psec_policy = vpc_service.update_ipsec_policy(
                id=data['ipsecPolicyId'],
                i_psec_policy_patch=i_psec_policy_patch_model).get_result()

            # end-update_ipsec_policy

            assert i_psec_policy is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_ipsec_policy_connections_example(self):
        """
        list_ipsec_policy_connections request example
        """
        try:
            print('\nlist_ipsec_policy_connections() result:')
            # begin-list_ipsec_policy_connections

            vpn_gateway_connection_collection = vpc_service.list_ipsec_policy_connections(
                id=data['ipsecPolicyId']).get_result()

            # end-list_ipsec_policy_connections

            assert vpn_gateway_connection_collection is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_vpn_gateways_example(self):
        """
        list_vpn_gateways request example
        """
        try:
            print('\nlist_vpn_gateways() result:')
            # begin-list_vpn_gateways

            all_results = []
            pager = VpnGatewaysPager(
                client=vpc_service,
                limit=10,
                sort='name',
                mode='route',
            )
            while pager.has_next():
                next_page = pager.get_next()
                assert next_page is not None
                all_results.extend(next_page)

            # end-list_vpn_gateways

            print(json.dumps(all_results, indent=2))

            assert all_results is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_vpn_gateway_example(self):
        """
        create_vpn_gateway request example
        """
        try:
            print('\ncreate_vpn_gateway() result:')
            # begin-create_vpn_gateway

            subnet_identity_model = {}
            subnet_identity_model['id'] = data['subnetId']

            vpn_gateway_prototype_model = {}
            vpn_gateway_prototype_model['subnet'] = subnet_identity_model
            vpn_gateway_prototype_model['name'] = 'my-vpn-gateway'
            vpn_gateway_prototype_model['mode'] = 'route'

            vpn_gateway = vpc_service.create_vpn_gateway(
                vpn_gateway_prototype=vpn_gateway_prototype_model).get_result()

            # end-create_vpn_gateway

            assert vpn_gateway is not None
            data['vpnGateway']=vpn_gateway
            data['vpnGatewayId']=vpn_gateway['id']

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_vpn_gateway_example(self):
        """
        get_vpn_gateway request example
        """
        try:
            print('\nget_vpn_gateway() result:')
            # begin-get_vpn_gateway

            vpn_gateway = vpc_service.get_vpn_gateway(
                id=data['vpnGatewayId']).get_result()

            # end-get_vpn_gateway

            assert vpn_gateway is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_vpn_gateway_example(self):
        """
        update_vpn_gateway request example
        """
        try:
            print('\nupdate_vpn_gateway() result:')
            # begin-update_vpn_gateway

            vpn_gateway_patch_model = {}
            vpn_gateway_patch_model['name'] = 'my-vpn-gateway-updated'

            vpn_gateway = vpc_service.update_vpn_gateway(
                id=data['vpnGatewayId'],
                vpn_gateway_patch=vpn_gateway_patch_model).get_result()

            # end-update_vpn_gateway

            assert vpn_gateway is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_vpn_gateway_connections_example(self):
        """
        list_vpn_gateway_connections request example
        """
        try:
            print('\nlist_vpn_gateway_connections() result:')
            # begin-list_vpn_gateway_connections

            vpn_gateway_connection_collection = vpc_service.list_vpn_gateway_connections(
                vpn_gateway_id=data['vpnGatewayId']).get_result()

            # end-list_vpn_gateway_connections

            assert vpn_gateway_connection_collection is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_vpn_gateway_connection_example(self):
        """
        create_vpn_gateway_connection request example
        """
        try:
            print('\ncreate_vpn_gateway_connection() result:')
            # begin-create_vpn_gateway_connection

            # Construct a dict representation of a VPNGatewayConnectionDPDPrototype model
            vpn_gateway_connection_dpd_prototype_model = {
                'action': 'restart',
                'interval': 30,
                'timeout': 120,
            }
            # Construct a dict representation of a VPNGatewayConnectionIKEPolicyPrototypeIKEPolicyIdentityById model
            vpn_gateway_connection_ike_policy_prototype_model = {
                'id': 'ddf51bec-3424-11e8-b467-0ed5f89f718b',
            }
            # Construct a dict representation of a VPNGatewayConnectionIPsecPolicyPrototypeIPsecPolicyIdentityById model
            vpn_gateway_connection_i_psec_policy_prototype_model = {
                'id': 'ddf51bec-3424-11e8-b467-0ed5f89f718b',
            }
            # Construct a dict representation of a VPNGatewayConnectionIKEIdentityPrototypeVPNGatewayConnectionIKEIdentityFQDN model
            vpn_gateway_connection_ike_identity_prototype_model = {
                'type': 'fqdn',
                'value': 'my-service.example.com',
            }
            # Construct a dict representation of a VPNGatewayConnectionStaticRouteModeLocalPrototype model
            vpn_gateway_connection_static_route_mode_local_prototype_model = {
                'ike_identities': [vpn_gateway_connection_ike_identity_prototype_model],
            }
            # Construct a dict representation of a VPNGatewayConnectionStaticRouteModePeerPrototypeVPNGatewayConnectionPeerByAddress model
            vpn_gateway_connection_static_route_mode_peer_prototype_model = {
                'ike_identity': vpn_gateway_connection_ike_identity_prototype_model,
                'address': '169.21.50.5',
            }
            # Construct a dict representation of a VPNGatewayConnectionPrototypeVPNGatewayConnectionStaticRouteModePrototype model
            vpn_gateway_connection_prototype_model = {
                'admin_state_up': True,
                'dead_peer_detection': vpn_gateway_connection_dpd_prototype_model,
                'establish_mode': 'bidirectional',
                'ike_policy': vpn_gateway_connection_ike_policy_prototype_model,
                'ipsec_policy': vpn_gateway_connection_i_psec_policy_prototype_model,
                'name': 'my-vpn-connection',
                'psk': 'lkj14b1oi0alcniejkso',
                'local': vpn_gateway_connection_static_route_mode_local_prototype_model,
                'peer': vpn_gateway_connection_static_route_mode_peer_prototype_model,
                'routing_protocol': 'none',
            }

            vpn_gateway_connection = vpc_service.create_vpn_gateway_connection(
                vpn_gateway_id=data['vpnGatewayId'],
                vpn_gateway_connection_prototype=vpn_gateway_connection_prototype_model,
            ).get_result()

            # end-create_vpn_gateway_connection

            assert vpn_gateway_connection is not None
            data['vpnGatewayConnectionId']=vpn_gateway_connection['id']

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_vpn_gateway_connection_example(self):
        """
        get_vpn_gateway_connection request example
        """
        try:
            print('\nget_vpn_gateway_connection() result:')
            # begin-get_vpn_gateway_connection

            vpn_gateway_connection = vpc_service.get_vpn_gateway_connection(
                vpn_gateway_id=data['vpnGatewayId'],
                id=data['vpnGatewayConnectionId']).get_result()

            # end-get_vpn_gateway_connection

            assert vpn_gateway_connection is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_vpn_gateway_connection_example(self):
        """
        update_vpn_gateway_connection request example
        """
        try:
            print('\nupdate_vpn_gateway_connection() result:')
            # begin-update_vpn_gateway_connection

            vpn_gateway_connection_patch_model = {}
            vpn_gateway_connection_patch_model['name'] = 'my-vpn-gateway-connection-updated'
            vpn_gateway_connection_patch_model['peer_address'] = '192.132.5.0'
            vpn_gateway_connection_patch_model['psk'] = 'lkj14b1oi0alcniejkso'

            vpn_gateway_connection = vpc_service.update_vpn_gateway_connection(
                vpn_gateway_id=data['vpnGatewayId'],
                id=data['vpnGatewayConnectionId'],
                vpn_gateway_connection_patch=vpn_gateway_connection_patch_model
            ).get_result()

            # end-update_vpn_gateway_connection

            assert vpn_gateway_connection is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_add_vpn_gateway_connection_local_cidr_example(self):
        """
        add_vpn_gateway_connection_local_cidr request example
        """
        try:
            # begin-add_vpn_gateway_connection_local_cidr

            response = vpc_service.add_vpn_gateway_connections_local_cidr(
                vpn_gateway_id=data['vpnGatewayId'],
                id=data['vpnGatewayConnectionId'],
                cidr='192.144.0.0/28')

            # end-add_vpn_gateway_connection_local_cidr
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_vpn_gateway_connection_local_cidrs_example(self):
        """
        list_vpn_gateway_connection_local_cidrs request example
        """
        try:
            print('\nlist_vpn_gateway_connection_local_cidrs() result:')
            # begin-list_vpn_gateway_connection_local_cidrs

            vpn_gateway_connection_local_cid_rs = vpc_service.list_vpn_gateway_connections_local_cidrs(
                vpn_gateway_id=data['vpnGatewayId'], id=data['vpnGatewayConnectionId']).get_result()

            # end-list_vpn_gateway_connection_local_cidrs

            assert vpn_gateway_connection_local_cid_rs is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_add_vpn_gateway_connection_peer_cidr_example(self):
        """
        add_vpn_gateway_connection_peer_cidr request example
        """
        try:
            # begin-add_vpn_gateway_connection_peer_cidr

            response = vpc_service.add_vpn_gateway_connections_peer_cidr(
                vpn_gateway_id=data['vpnGatewayId'],
                id=data['vpnGatewayConnectionId'],
                cidr='192.144.0.0/28')

            # end-add_vpn_gateway_connection_peer_cidr
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_check_vpn_gateway_connection_local_cidr_example(self):
        """
        check_vpn_gateway_connection_local_cidr request example
        """
        try:
            # begin-check_vpn_gateway_connection_local_cidr

            response = vpc_service.check_vpn_gateway_connections_local_cidr(
                vpn_gateway_id=data['vpnGatewayId'],
                id=data['vpnGatewayConnectionId'],
                cidr='192.144.0.0/28')

            # end-check_vpn_gateway_connection_local_cidr
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_vpn_gateway_connection_peer_cidrs_example(self):
        """
        list_vpn_gateway_connection_peer_cidrs request example
        """
        try:
            print('\nlist_vpn_gateway_connection_peer_cidrs() result:')
            # begin-list_vpn_gateway_connection_peer_cidrs

            vpn_gateway_connection_peer_cid_rs = vpc_service.list_vpn_gateway_connections_peer_cidrs(
                vpn_gateway_id=data['vpnGatewayId'], id=data['vpnGatewayConnectionId']).get_result()

            # end-list_vpn_gateway_connection_peer_cidrs

            assert vpn_gateway_connection_peer_cid_rs is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_check_vpn_gateway_connection_peer_cidr_example(self):
        """
        check_vpn_gateway_connection_peer_cidr request example
        """
        try:
            # begin-check_vpn_gateway_connection_peer_cidr

            response = vpc_service.check_vpn_gateway_connections_peer_cidr(
                vpn_gateway_id=data['vpnGatewayId'],
                id=data['vpnGatewayConnectionId'],
                cidr='192.144.0.0/28')

            # end-check_vpn_gateway_connection_peer_cidr
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_vpn_servers_example(self):
        """
        list_vpn_servers request example
        """
        try:
            print('\nlist_vpn_servers() result:')
            # begin-list_vpn_servers

            all_results = []
            pager = VpnServersPager(
                client=vpc_service,
                limit=10,
                sort='name',
            )
            while pager.has_next():
                next_page = pager.get_next()
                assert next_page is not None
                all_results.extend(next_page)

            # end-list_vpn_servers

            print(json.dumps(all_results, indent=2))

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_vpn_server_example(self):
        """
        create_vpn_server request example
        """
        try:
            print('\ncreate_vpn_server() result:')
            # begin-create_vpn_server

            certificate_instance_identity_model = {
                'crn': 'crn:v1:bluemix:public:secrets-manager:us-south:a/123456:36fa422d-080d-4d83-8d2d-86851b4001df:secret:2e786aab-42fa-63ed-14f8-d66d552f4dd5',
            }

            vpn_server_authentication_by_username_id_provider_model = {
                'provider_type': 'iam',
            }

            vpn_server_authentication_prototype_model = {
                'method': 'certificate',
                'identity_provider': vpn_server_authentication_by_username_id_provider_model,
            }

            subnet_identity_model = {
                'id': data['subnetId'],
            }

            vpn_server = vpc_service.create_vpn_server(
                certificate=certificate_instance_identity_model,
                client_authentication=[vpn_server_authentication_prototype_model],
                client_ip_pool='172.16.0.0/16',
                subnets=[subnet_identity_model],
                name='my-example-vpn-server'
            ).get_result()

            print(json.dumps(vpn_server, indent=2))

            # end-create_vpn_server

            data['vpnserverId']=vpn_server['id']
        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_vpn_server_example(self):
        """
        get_vpn_server request example
        """
        try:
            print('\nget_vpn_server() result:')
            # begin-get_vpn_server

            vpn_server_response = vpc_service.get_vpn_server(
                id=data['vpnserverId']
            )
            data['created_vpn_server_etag'] = vpn_server_response.get_headers()['ETag']
            vpn_server = vpn_server_response.get_result()

            print(json.dumps(vpn_server, indent=2))

            # end-get_vpn_server
        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_vpn_server_example(self):
        """
        update_vpn_server request example
        """
        try:
            print('\nupdate_vpn_server() result:')
            # begin-update_vpn_server

            vpn_server_patch_model = {}
            vpn_server_patch_model['name']='my-vpn-server-updated'

            vpn_server = vpc_service.update_vpn_server(
                id=data['vpnserverId'],
                vpn_server_patch=vpn_server_patch_model,
                if_match=data['created_vpn_server_etag']
            ).get_result()

            print(json.dumps(vpn_server, indent=2))

            # end-update_vpn_server

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_vpn_server_client_configuration_example(self):
        """
        get_vpn_server_client_configuration request example
        """
        try:
            print('\nget_vpn_server_client_configuration() result:')
            # begin-get_vpn_server_client_configuration

            vpn_server_client_configuration = vpc_service.get_vpn_server_client_configuration(
                id=data['vpnserverId']
            ).get_result()

            print(json.dumps(vpn_server_client_configuration, indent=2))

            # end-get_vpn_server_client_configuration

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_vpn_server_clients_example(self):
        """
        list_vpn_server_clients request example
        """
        try:
            print('\nlist_vpn_server_clients() result:')
            # begin-list_vpn_server_clients

            all_results = []
            pager = VpnServerClientsPager(
                client=vpc_service,
                vpn_server_id=data['vpnserverId'],
                limit=10,
                sort='created_at',
            )
            while pager.has_next():
                next_page = pager.get_next()
                assert next_page is not None
                all_results.extend(next_page)

            # end-list_vpn_server_clients

            print(json.dumps(all_results, indent=2))
            data['vpnserverclientId']=all_results[0]['id']
        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_vpn_server_client_example(self):
        """
        get_vpn_server_client request example
        """
        try:
            print('\nget_vpn_server_client() result:')
            # begin-get_vpn_server_client

            vpn_server_client = vpc_service.get_vpn_server_client(
                vpn_server_id=data['vpnserverId'],
                id=data['vpnserverclientId']
            ).get_result()

            print(json.dumps(vpn_server_client, indent=2))

            # end-get_vpn_server_client

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_disconnect_vpn_client_example(self):
        """
        disconnect_vpn_client request example
        """
        try:
            # begin-disconnect_vpn_client

            response = vpc_service.disconnect_vpn_client(
                vpn_server_id=data['vpnserverId'],
                id=data['vpnserverclientId']
            )

            # end-disconnect_vpn_client
            print('\ndisconnect_vpn_client() response status code: ', response.get_status_code())

        except ApiException as e:
            pytest.fail(str(e))

    
    @needscredentials
    def test_create_vpn_server_route_example(self):
        """
        create_vpn_server_route request example
        """
        try:
            print('\ncreate_vpn_server_route() result:')
            # begin-create_vpn_server_route

            vpn_server_route = vpc_service.create_vpn_server_route(
                vpn_server_id=data['vpnserverId'],
                destination='172.16.0.0/16',
                name='my-vpn-server-route'
            ).get_result()

            print(json.dumps(vpn_server_route, indent=2))

            # end-create_vpn_server_route
            data['vpnserverrouteId']=vpn_server_route['id']
        except ApiException as e:
            pytest.fail(str(e))
    @needscredentials
    @pytest.mark.skip(reason="mock")
    def test_list_vpn_server_routes_example(self):
        """
        list_vpn_server_routes request example
        """
        try:
            print('\nlist_vpn_server_routes() result:')
            # begin-list_vpn_server_routes

            all_results = []
            pager = VpnServerRoutesPager(
                client=vpc_service,
                vpn_server_id=data['vpnserverId'],
                limit=10,
                sort='name',
            )
            while pager.has_next():
                next_page = pager.get_next()
                assert next_page is not None
                all_results.extend(next_page)

            # end-list_vpn_server_routes

            print(json.dumps(all_results, indent=2))

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_vpn_server_route_example(self):
        """
        get_vpn_server_route request example
        """
        try:
            print('\nget_vpn_server_route() result:')
            # begin-get_vpn_server_route

            vpn_server_route = vpc_service.get_vpn_server_route(
                vpn_server_id=data['vpnserverId'],
                id=data['vpnserverrouteId']
            ).get_result()

            print(json.dumps(vpn_server_route, indent=2))

            # end-get_vpn_server_route

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_vpn_server_route_example(self):
        """
        update_vpn_server_route request example
        """
        try:
            print('\nupdate_vpn_server_route() result:')
            # begin-update_vpn_server_route

            vpn_server_route_patch_model = {}
            vpn_server_route_patch_model['name'] = 'my-vpnserver-route-updated'

            vpn_server_route = vpc_service.update_vpn_server_route(
                vpn_server_id=data['vpnserverId'],
                id=data['vpnserverrouteId'],
                vpn_server_route_patch=vpn_server_route_patch_model
            ).get_result()

            print(json.dumps(vpn_server_route, indent=2))

            # end-update_vpn_server_route

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_vpn_server_route_example(self):
        """
        delete_vpn_server_route request example
        """
        try:
            # begin-delete_vpn_server_route

            response = vpc_service.delete_vpn_server_route(
                vpn_server_id=data['vpnserverId'],
                id=data['vpnserverrouteId']
            )

            # end-delete_vpn_server_route
            print('\ndelete_vpn_server_route() response status code: ', response.get_status_code())

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_vpn_server_client_example(self):
        """
        delete_vpn_server_client request example
        """
        try:
            # begin-delete_vpn_server_client

            response = vpc_service.delete_vpn_server_client(
                vpn_server_id=data['vpnserverId'],
                id=data['vpnserverclientId']
            )

            # end-delete_vpn_server_client
            print('\ndelete_vpn_server_client() response status code: ', response.get_status_code())

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_vpn_server_example(self):
        """
        delete_vpn_server request example
        """
        try:
            # begin-delete_vpn_server

            response = vpc_service.delete_vpn_server(
                id=data['vpnserverId'],
                if_match=data['created_vpn_server_etag']
            )

            # end-delete_vpn_server
            print('\ndelete_vpn_server() response status code: ', response.get_status_code())

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_load_balancer_profiles_example(self):
        """
        list_load_balancer_profiles request example
        """
        try:
            print('\nlist_load_balancer_profiles() result:')
            # begin-list_load_balancer_profiles

            all_results = []
            pager = LoadBalancerProfilesPager(
                client=vpc_service,
                limit=10,
            )
            while pager.has_next():
                next_page = pager.get_next()
                assert next_page is not None
                all_results.extend(next_page)

            # end-list_load_balancer_profiles

            print(json.dumps(all_results, indent=2))

            assert all_results is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_load_balancer_profile_example(self):
        """
        get_load_balancer_profile request example
        """
        try:
            print('\nget_load_balancer_profile() result:')
            # begin-get_load_balancer_profile

            load_balancer_profile = vpc_service.get_load_balancer_profile(
                name='network-fixed').get_result()

            # end-get_load_balancer_profile

            assert load_balancer_profile is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_load_balancers_example(self):
        """
        list_load_balancers request example
        """
        try:
            print('\nlist_load_balancers() result:')
            # begin-list_load_balancers

            all_results = []
            pager = LoadBalancersPager(
                client=vpc_service,
                limit=10,
            )
            while pager.has_next():
                next_page = pager.get_next()
                assert next_page is not None
                all_results.extend(next_page)


            # end-list_load_balancers

            print(json.dumps(all_results, indent=2))

            assert all_results is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_load_balancer_example(self):
        """
        create_load_balancer request example
        """
        try:
            print('\ncreate_load_balancer() result:')
            # begin-create_load_balancer
            dns_instance_identity_model = {
                'crn': 'crn:v1:bluemix:public:dns-svcs:global:a/fff1cdf3dc1e4ec692a5f78bbb2584bc:6860c359-b2e2-46fa-a944-b38c28201c6e',
            }

            dns_zone_identity_model = {
                'id': 'd66662cc-aa23-4fe1-9987-858487a61f45',
            }

            load_balancer_dns_prototype_model = {
                'instance': dns_instance_identity_model,
                'zone': dns_zone_identity_model,
            }
            subnet_identity_model = {}
            subnet_identity_model['id'] = data['subnetId']

            load_balancer = vpc_service.create_load_balancer(
                dns=load_balancer_dns_prototype_model,
                is_public=False, subnets=[subnet_identity_model],
                name='my-load-balancer').get_result()

            # end-create_load_balancer

            assert load_balancer is not None
            data['loadBalancerId']=load_balancer['id']

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_load_balancer_example(self):
        """
        get_load_balancer request example
        """
        try:
            print('\nget_load_balancer() result:')
            # begin-get_load_balancer

            load_balancer_response = vpc_service.get_load_balancer(
                id=data['loadBalancerId'])
            load_balancer = load_balancer_response.get_result()
            data['created_load_balancer_etag'] = load_balancer_response.get_headers()['ETag']
            # end-get_load_balancer

            assert load_balancer is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_load_balancer_example(self):
        """
        update_load_balancer request example
        """
        try:
            print('\nupdate_load_balancer() result:')
            # begin-update_load_balancer
            dns_instance_identity_model = {
                'crn': 'crn:v1:bluemix:public:dns-svcs:global:a/fff1cdf3dc1e4ec692a5f78bbb2584bc:6860c359-b2e2-46fa-a944-b38c28201c6e',
            }
            dns_zone_identity_model = {
                'id': 'd66662cc-aa23-4fe1-9987-858487a61f45',
            }
            load_balancer_dns_patch_model = {
                'instance': dns_instance_identity_model,
                'zone': dns_zone_identity_model,
            }

            load_balancer_patch_model = {}
            load_balancer_patch_model['dns'] = load_balancer_dns_patch_model
            load_balancer_patch_model['name'] = 'my-load-balancer-updated'

            load_balancer = vpc_service.update_load_balancer(
                id=data['loadBalancerId'],
                load_balancer_patch=load_balancer_patch_model,
                if_match=data['created_load_balancer_etag']).get_result()

            # end-update_load_balancer

            assert load_balancer is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_load_balancer_statistics_example(self):
        """
        get_load_balancer_statistics request example
        """
        try:
            print('\nget_load_balancer_statistics() result:')
            # begin-get_load_balancer_statistics

            load_balancer_statistics = vpc_service.get_load_balancer_statistics(
                id=data['loadBalancerId']).get_result()

            # end-get_load_balancer_statistics

            assert load_balancer_statistics is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_load_balancer_listeners_example(self):
        """
        list_load_balancer_listeners request example
        """
        try:
            print('\nlist_load_balancer_listeners() result:')
            # begin-list_load_balancer_listeners

            load_balancer_listener_collection = vpc_service.list_load_balancer_listeners(
                load_balancer_id=data['loadBalancerId']).get_result()

            # end-list_load_balancer_listeners

            assert load_balancer_listener_collection is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_load_balancer_listener_example(self):
        """
        create_load_balancer_listener request example
        """
        try:
            print('\ncreate_load_balancer_listener() result:')
            # begin-create_load_balancer_listener

            load_balancer_listener = vpc_service.create_load_balancer_listener(
                load_balancer_id=data['loadBalancerId'], port=5656,
                idle_connection_timeout=100,
                protocol='http').get_result()

            # end-create_load_balancer_listener

            assert load_balancer_listener is not None
            data['listenerId']=load_balancer_listener['id']

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_load_balancer_listener_example(self):
        """
        get_load_balancer_listener request example
        """
        try:
            print('\nget_load_balancer_listener() result:')
            # begin-get_load_balancer_listener

            load_balancer_listener = vpc_service.get_load_balancer_listener(
                load_balancer_id=data['loadBalancerId'], id=data['listenerId']).get_result()

            # end-get_load_balancer_listener

            assert load_balancer_listener is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_load_balancer_listener_example(self):
        """
        update_load_balancer_listener request example
        """
        try:
            print('\nupdate_load_balancer_listener() result:')
            # begin-update_load_balancer_listener
            certificate_instance_identity_model = {}
            certificate_instance_identity_model['crn'] = "certificate_id"

            load_balancer_pool_identity_model = {}
            load_balancer_pool_identity_model['id'] = "load_balancer_pool_id"

            load_balancer_listener_patch_model = {}
            load_balancer_listener_patch_model['port'] = 5666
            load_balancer_listener_patch_model['certificate_instance'] = certificate_instance_identity_model
            load_balancer_listener_patch_model['connection_limit'] = 2500
            load_balancer_listener_patch_model['default_pool'] = load_balancer_pool_identity_model
            load_balancer_listener_patch_model['protocol'] = 'http'

            load_balancer_listener = vpc_service.update_load_balancer_listener(
                load_balancer_id=data['loadBalancerId'],
                id=data['listenerId'],
                load_balancer_listener_patch=load_balancer_listener_patch_model
            ).get_result()

            # end-update_load_balancer_listener

            assert load_balancer_listener is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_load_balancer_listener_policies_example(self):
        """
        list_load_balancer_listener_policies request example
        """
        try:
            print('\nlist_load_balancer_listener_policies() result:')
            # begin-list_load_balancer_listener_policies

            load_balancer_listener_policy_collection = vpc_service.list_load_balancer_listener_policies(
                load_balancer_id=data['loadBalancerId'],
                listener_id=data['listenerId']).get_result()

            # end-list_load_balancer_listener_policies

            assert load_balancer_listener_policy_collection is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_load_balancer_listener_policy_example(self):
        """
        create_load_balancer_listener_policy request example
        """
        try:
            print('\ncreate_load_balancer_listener_policy() result:')
            # begin-create_load_balancer_listener_policy

            load_balancer_listener_policy = vpc_service.create_load_balancer_listener_policy(
                load_balancer_id=data['loadBalancerId'],
                listener_id=data['listenerId'],
                action='reject',
                priority=2,
                name= 'my-load-balancer-listener-policy').get_result()

            # end-create_load_balancer_listener_policy

            assert load_balancer_listener_policy is not None
            data['policyId']=load_balancer_listener_policy['id']

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_load_balancer_listener_policy_example(self):
        """
        get_load_balancer_listener_policy request example
        """
        try:
            print('\nget_load_balancer_listener_policy() result:')
            # begin-get_load_balancer_listener_policy

            load_balancer_listener_policy = vpc_service.get_load_balancer_listener_policy(
                load_balancer_id=data['loadBalancerId'],
                listener_id=data['listenerId'],
                id=data['policyId']).get_result()

            # end-get_load_balancer_listener_policy

            assert load_balancer_listener_policy is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_load_balancer_listener_policy_example(self):
        """
        update_load_balancer_listener_policy request example
        """
        try:
            print('\nupdate_load_balancer_listener_policy() result:')
            # begin-update_load_balancer_listener_policy

            load_balancer_listener_policy_patch_model = {}
            load_balancer_listener_policy_patch_model['name'] = 'my-load-balancer-listener-policy-updated'
            load_balancer_listener_policy_patch_model['priority'] = 5

            load_balancer_listener_policy = vpc_service.update_load_balancer_listener_policy(
                load_balancer_id=data['loadBalancerId'],
                listener_id=data['listenerId'],
                id=data['policyId'],
                load_balancer_listener_policy_patch=
                load_balancer_listener_policy_patch_model).get_result()

            # end-update_load_balancer_listener_policy

            assert load_balancer_listener_policy is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_load_balancer_listener_policy_rules_example(self):
        """
        list_load_balancer_listener_policy_rules request example
        """
        try:
            print('\nlist_load_balancer_listener_policy_rules() result:')
            # begin-list_load_balancer_listener_policy_rules

            load_balancer_listener_policy_rule_collection = vpc_service.list_load_balancer_listener_policy_rules(
                load_balancer_id=data['loadBalancerId'],
                listener_id=data['listenerId'],
                policy_id=data['policyId']).get_result()

            # end-list_load_balancer_listener_policy_rules

            assert load_balancer_listener_policy_rule_collection is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_load_balancer_listener_policy_rule_example(self):
        """
        create_load_balancer_listener_policy_rule request example
        """
        try:
            print('\ncreate_load_balancer_listener_policy_rule() result:')
            # begin-create_load_balancer_listener_policy_rule

            load_balancer_listener_policy_rule = vpc_service.create_load_balancer_listener_policy_rule(
                load_balancer_id=data['loadBalancerId'],
                listener_id=data['listenerId'],
                policy_id=data['policyId'],
                condition='contains',
                type='hostname',
                value='one').get_result()

            # end-create_load_balancer_listener_policy_rule

            assert load_balancer_listener_policy_rule is not None
            data['policyRuleId']=load_balancer_listener_policy_rule['id']

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_load_balancer_listener_policy_rule_example(self):
        """
        get_load_balancer_listener_policy_rule request example
        """
        try:
            print('\nget_load_balancer_listener_policy_rule() result:')
            # begin-get_load_balancer_listener_policy_rule

            load_balancer_listener_policy_rule = vpc_service.get_load_balancer_listener_policy_rule(
                load_balancer_id=data['loadBalancerId'],
                listener_id=data['listenerId'],
                policy_id=data['policyId'],
                id=data['policyRuleId']).get_result()

            # end-get_load_balancer_listener_policy_rule

            assert load_balancer_listener_policy_rule is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_load_balancer_listener_policy_rule_example(self):
        """
        update_load_balancer_listener_policy_rule request example
        """
        try:
            print('\nupdate_load_balancer_listener_policy_rule() result:')
            # begin-update_load_balancer_listener_policy_rule

            load_balancer_listener_policy_rule_patch_model = {}
            load_balancer_listener_policy_rule_patch_model['condition'] = 'contains'
            load_balancer_listener_policy_rule_patch_model['field'] = 'MY-APP-HEADER'
            load_balancer_listener_policy_rule_patch_model['type'] = 'header'
            load_balancer_listener_policy_rule_patch_model['value'] = 'app'

            load_balancer_listener_policy_rule = vpc_service.update_load_balancer_listener_policy_rule(
                load_balancer_id=data['loadBalancerId'],
                listener_id=data['listenerId'],
                policy_id=data['policyId'],
                id=data['policyRuleId'],
                load_balancer_listener_policy_rule_patch=
                load_balancer_listener_policy_rule_patch_model).get_result()

            # end-update_load_balancer_listener_policy_rule

            assert load_balancer_listener_policy_rule is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_load_balancer_pools_example(self):
        """
        list_load_balancer_pools request example
        """
        try:
            print('\nlist_load_balancer_pools() result:')
            # begin-list_load_balancer_pools

            load_balancer_pool_collection = vpc_service.list_load_balancer_pools(
                load_balancer_id=data['loadBalancerId']).get_result()

            # end-list_load_balancer_pools

            assert load_balancer_pool_collection is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_load_balancer_pool_example(self):
        """
        create_load_balancer_pool request example
        """
        try:
            print('\ncreate_load_balancer_pool() result:')
            # begin-create_load_balancer_pool

            load_balancer_pool_health_monitor_prototype_model = {}
            load_balancer_pool_health_monitor_prototype_model['delay'] = 30
            load_balancer_pool_health_monitor_prototype_model['max_retries'] = 3
            load_balancer_pool_health_monitor_prototype_model['timeout'] =  30
            load_balancer_pool_health_monitor_prototype_model['type'] = 'http'

            load_balancer_pool = vpc_service.create_load_balancer_pool(
                load_balancer_id=data['loadBalancerId'],
                algorithm='round_robin',
                health_monitor=load_balancer_pool_health_monitor_prototype_model,
                protocol='http',
                name='my-load-balancer-pool').get_result()

            # end-create_load_balancer_pool

            assert load_balancer_pool is not None
            data['poolId']=load_balancer_pool['id']

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_load_balancer_pool_example(self):
        """
        get_load_balancer_pool request example
        """
        try:
            print('\nget_load_balancer_pool() result:')
            # begin-get_load_balancer_pool

            load_balancer_pool = vpc_service.get_load_balancer_pool(
                load_balancer_id=data['loadBalancerId'], id=data['poolId']).get_result()

            # end-get_load_balancer_pool

            assert load_balancer_pool is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_load_balancer_pool_example(self):
        """
        update_load_balancer_pool request example
        """
        try:
            print('\nupdate_load_balancer_pool() result:')
            # begin-update_load_balancer_pool

            load_balancer_pool_patch_model = {}
            load_balancer_pool_patch_model['name'] = 'my-load-balancer-pool-updated'
            load_balancer_pool_patch_model['session_persistence'] = 'http_cookie'

            load_balancer_pool = vpc_service.update_load_balancer_pool(
                load_balancer_id=data['loadBalancerId'],
                id=data['poolId'],
                load_balancer_pool_patch=load_balancer_pool_patch_model
            ).get_result()

            # end-update_load_balancer_pool

            assert load_balancer_pool is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_load_balancer_pool_members_example(self):
        """
        list_load_balancer_pool_members request example
        """
        try:
            print('\nlist_load_balancer_pool_members() result:')
            # begin-list_load_balancer_pool_members

            load_balancer_pool_member_collection = vpc_service.list_load_balancer_pool_members(
                load_balancer_id=data['loadBalancerId'],
                pool_id=data['poolId']).get_result()

            # end-list_load_balancer_pool_members

            assert load_balancer_pool_member_collection is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_load_balancer_pool_member_example(self):
        """
        create_load_balancer_pool_member request example
        """
        try:
            print('\ncreate_load_balancer_pool_member() result:')
            # begin-create_load_balancer_pool_member

            load_balancer_pool_member_target_prototype_model_identity = {}
            load_balancer_pool_member_target_prototype_model_identity['address']='192.168.3.4'

            load_balancer_pool_member_target_prototype_model = {}
            load_balancer_pool_member_target_prototype_model['id'] = load_balancer_pool_member_target_prototype_model_identity

            load_balancer_pool_member = vpc_service.create_load_balancer_pool_member(
                load_balancer_id=data['loadBalancerId'],
                pool_id=data['poolId'],
                port=80,
                target=load_balancer_pool_member_target_prototype_model,
                weight=50
            ).get_result()

            # end-create_load_balancer_pool_member

            assert load_balancer_pool_member is not None
            data['poolMemberId']=load_balancer_pool_member['id']

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_load_balancer_pool_member_example(self):
        """
        get_load_balancer_pool_member request example
        """
        try:
            print('\nget_load_balancer_pool_member() result:')
            # begin-get_load_balancer_pool_member

            load_balancer_pool_member = vpc_service.get_load_balancer_pool_member(
                load_balancer_id=data['loadBalancerId'],
                pool_id=data['poolId'],
                id=data['poolMemberId']).get_result()

            # end-get_load_balancer_pool_member

            assert load_balancer_pool_member is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_load_balancer_pool_member_example(self):
        """
        update_load_balancer_pool_member request example
        """
        try:
            print('\nupdate_load_balancer_pool_member() result:')
            # begin-update_load_balancer_pool_member
            load_balancer_pool_member_target_prototype_model = {}
            load_balancer_pool_member_target_prototype_model[
                'address'] = '192.168.3.4'

            load_balancer_pool_member_patch_model = {}
            load_balancer_pool_member_patch_model['port'] = 1235
            load_balancer_pool_member_patch_model['weight'] = 50
            load_balancer_pool_member_patch_model['target'] = load_balancer_pool_member_target_prototype_model
            load_balancer_pool_member = vpc_service.update_load_balancer_pool_member(
                load_balancer_id=data['loadBalancerId'],
                pool_id=data['poolId'],
                id=data['poolMemberId'],
                load_balancer_pool_member_patch=
                load_balancer_pool_member_patch_model).get_result()

            # end-update_load_balancer_pool_member

            assert load_balancer_pool_member is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_replace_load_balancer_pool_members_example(self):
        """
        replace_load_balancer_pool_members request example
        """
        try:
            print('\nreplace_load_balancer_pool_members() result:')
            # begin-replace_load_balancer_pool_members

            load_balancer_pool_member_target_prototype_model = {}
            load_balancer_pool_member_target_prototype_model['address'] = '192.168.3.5'

            load_balancer_pool_member_prototype_model = {}
            load_balancer_pool_member_prototype_model['port'] = 1235
            load_balancer_pool_member_prototype_model['target'] = load_balancer_pool_member_target_prototype_model

            load_balancer_pool_member_collection = vpc_service.replace_load_balancer_pool_members(
                load_balancer_id=data['loadBalancerId'],
                pool_id=data['poolId'],
                members=[load_balancer_pool_member_prototype_model
                        ]).get_result()

            # end-replace_load_balancer_pool_members

            assert load_balancer_pool_member_collection is not None
            data['poolMemberId']=load_balancer_pool_member_collection['members'][0]['id']

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_load_balancer_pool_member_example(self):
        """
        delete_load_balancer_pool_member request example
        """
        try:
            # begin-delete_load_balancer_pool_member

            response = vpc_service.delete_load_balancer_pool_member(
                load_balancer_id=data['loadBalancerId'],
                pool_id=data['poolId'],
                id=data['poolMemberId'])

            # end-delete_load_balancer_pool_member
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_load_balancer_pool_example(self):
        """
        delete_load_balancer_pool request example
        """
        try:
            # begin-delete_load_balancer_pool

            response = vpc_service.delete_load_balancer_pool(
                load_balancer_id=data['loadBalancerId'], id=data['poolId'])

            # end-delete_load_balancer_pool
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_load_balancer_listener_policy_rule_example(self):
        """
        delete_load_balancer_listener_policy_rule request example
        """
        try:
            # begin-delete_load_balancer_listener_policy_rule

            response = vpc_service.delete_load_balancer_listener_policy_rule(
                load_balancer_id=data['loadBalancerId'],
                listener_id=data['listenerId'],
                policy_id=data['policyId'],
                id=data['policyRuleId'])

            # end-delete_load_balancer_listener_policy_rule
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_load_balancer_listener_policy_example(self):
        """
        delete_load_balancer_listener_policy request example
        """
        try:
            # begin-delete_load_balancer_listener_policy

            response = vpc_service.delete_load_balancer_listener_policy(
                load_balancer_id=data['loadBalancerId'],
                listener_id=data['listenerId'],
                id=data['policyId'])

            # end-delete_load_balancer_listener_policy
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_load_balancer_listener_example(self):
        """
        delete_load_balancer_listener request example
        """
        try:
            # begin-delete_load_balancer_listener

            response = vpc_service.delete_load_balancer_listener(
                load_balancer_id=data['loadBalancerId'], id=data['listenerId'])

            # end-delete_load_balancer_listener
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_load_balancer_example(self):
        """
        delete_load_balancer request example
        """
        try:
            # begin-delete_load_balancer

            response = vpc_service.delete_load_balancer(id=data['loadBalancerId'],
            if_match=data['created_load_balancer_etag'])

            # end-delete_load_balancer
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_endpoint_gateways_example(self):
        """
        list_endpoint_gateways request example
        """
        try:
            print('\nlist_endpoint_gateways() result:')
            # begin-list_endpoint_gateways

            all_results = []
            pager = EndpointGatewaysPager(
                client=vpc_service,
                limit=10,
            )
            while pager.has_next():
                next_page = pager.get_next()
                assert next_page is not None
                all_results.extend(next_page)


            # end-list_endpoint_gateways

            print(json.dumps(all_results, indent=2))

            assert all_results is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_endpoint_gateway_example(self):
        """
        create_endpoint_gateway request example
        """
        try:
            print('\ncreate_endpoint_gateway() result:')
            # begin-create_endpoint_gateway

            vpc_identity_model = {}
            vpc_identity_model['id'] = data['vpcID']

            endpoint_target={}
            endpoint_target['name'] = 'ibm-ntp-server'
            endpoint_target['resource_type'] = 'provider_infrastructure_service'

            endpoint_gateway = vpc_service.create_endpoint_gateway(
                target=endpoint_target,
                vpc=vpc_identity_model,
                name='my-endpoint-gateway').get_result()

            # end-create_endpoint_gateway

            assert endpoint_gateway is not None
            data['endpointGatewayId']=endpoint_gateway['id']

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_endpoint_gateway_ips_example(self):
        """
        list_endpoint_gateway_ips request example
        """
        try:
            print('\nlist_endpoint_gateway_ips() result:')
            # begin-list_endpoint_gateway_ips

            all_results = []
            pager = EndpointGatewayIpsPager(
                client=vpc_service,
                endpoint_gateway_id=data['endpointGatewayId'],
                limit=10,
                sort='name',
            )
            while pager.has_next():
                next_page = pager.get_next()
                assert next_page is not None
                all_results.extend(next_page)


            # end-list_endpoint_gateway_ips

            print(json.dumps(all_results, indent=2))

            assert all_results is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_add_endpoint_gateway_ip_example(self):
        """
        add_endpoint_gateway_ip request example
        """
        try:
            print('\nadd_endpoint_gateway_ip() result:')
            # begin-add_endpoint_gateway_ip

            reserved_ip = vpc_service.add_endpoint_gateway_ip(
                endpoint_gateway_id=data['endpointGatewayId'], id=data['subnetReservedIp']).get_result()

            # end-add_endpoint_gateway_ip

            assert reserved_ip is not None
            data['endpointGatewayTargetId']=reserved_ip['id']

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_endpoint_gateway_ip_example(self):
        """
        get_endpoint_gateway_ip request example
        """
        try:
            print('\nget_endpoint_gateway_ip() result:')
            # begin-get_endpoint_gateway_ip

            reserved_ip = vpc_service.get_endpoint_gateway_ip(
                endpoint_gateway_id=data['endpointGatewayId'], id=data['endpointGatewayTargetId']).get_result()
            # end-get_endpoint_gateway_ip

            assert reserved_ip is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_endpoint_gateway_example(self):
        """
        get_endpoint_gateway request example
        """
        try:
            print('\nget_endpoint_gateway() result:')
            # begin-get_endpoint_gateway

            endpoint_gateway = vpc_service.get_endpoint_gateway(
                id=data['endpointGatewayId']).get_result()

            # end-get_endpoint_gateway

            assert endpoint_gateway is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_endpoint_gateway_example(self):
        """
        update_endpoint_gateway request example
        """
        try:
            print('\nupdate_endpoint_gateway() result:')
            # begin-update_endpoint_gateway

            endpoint_gateway_patch_model = {}
            endpoint_gateway_patch_model['name'] = 'my-endpoint-gateway-modified'

            endpoint_gateway = vpc_service.update_endpoint_gateway(
                id=data['endpointGatewayId'],
                endpoint_gateway_patch=endpoint_gateway_patch_model).get_result(
                )

            # end-update_endpoint_gateway

            assert endpoint_gateway is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_remove_endpoint_gateway_ip_example(self):
        """
        remove_endpoint_gateway_ip request example
        """
        try:
            # begin-remove_endpoint_gateway_ip

            response = vpc_service.remove_endpoint_gateway_ip(
                endpoint_gateway_id=data['endpointGatewayId'], id=data['endpointGatewayTargetId'])

            # end-remove_endpoint_gateway_ip
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_subnet_reserved_ip_example(self):
        """
        delete_subnet_reserved_ip request example
        """
        try:
            # begin-delete_subnet_reserved_ip

            response = vpc_service.delete_subnet_reserved_ip(
                subnet_id=data['subnetId'], id=data['subnetReservedIp'])

            assert response is not None

            # end-delete_subnet_reserved_ip
            print('\ndelete_subnet_reserved_ip() response status code: ',
                  response.get_status_code())

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_endpoint_gateway_example(self):
        """
        delete_endpoint_gateway request example
        """
        try:
            # begin-delete_endpoint_gateway

            response = vpc_service.delete_endpoint_gateway(id=data['endpointGatewayId'])

            # end-delete_endpoint_gateway
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_bare_metal_server_profiles_example(self):
        """
        list_bare_metal_server_profiles request example
        """
        try:
            print('\nlist_bare_metal_server_profiles() result:')
            # begin-list_bare_metal_server_profiles

            all_results = []
            pager = BareMetalServerProfilesPager(
                client=vpc_service,
                limit=10,
            )
            while pager.has_next():
                next_page = pager.get_next()
                assert next_page is not None
                all_results.extend(next_page)


            # end-list_bare_metal_server_profiles

            print(json.dumps(all_results, indent=2))
            assert all_results is not None
        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_bare_metal_server_profile_example(self):
        """
        get_bare_metal_server_profile request example
        """
        try:
            print('\nget_bare_metal_server_profile() result:')
            # begin-get_bare_metal_server_profile

            bare_metal_server_profile = vpc_service.get_bare_metal_server_profile(
                name='bmhbx2-24x384').get_result()

            # end-get_bare_metal_server_profile
            assert bare_metal_server_profile is not None
        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_bare_metal_servers_example(self):
        """
        list_bare_metal_servers request example
        """
        try:
            print('\nlist_bare_metal_servers() result:')
            # begin-list_bare_metal_servers

            all_results = []
            pager = BareMetalServersPager(
                client=vpc_service,
                limit=10,
                vpc_id=data['vpcID'],
            )
            while pager.has_next():
                next_page = pager.get_next()
                assert next_page is not None
                all_results.extend(next_page)


            # end-list_bare_metal_servers

            print(json.dumps(all_results, indent=2))
            assert all_results is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_bare_metal_server_example(self):
        """
        create_bare_metal_server request example
        """
        try:
            print('\ncreate_bare_metal_server() result:')
            # begin-create_bare_metal_server

            image_identity_model = {
                'id': data['imageId'],
            }

            key_identity_model = {
                'id': data['keyId'],
            }

            bare_metal_server_initialization_prototype_model = {
                'image': image_identity_model,
                'keys': [key_identity_model],
            }

            bare_metal_server_primary_network_interface_prototype_model = {
                'subnet': {
                    'id': data['subnetId'],
                },
            }
            bare_metal_server_profile_identity_model = {
                'name': 'bmx2-48x768',
            }
            zone_identity_model = {
                'name': data['zone'],
            }
            bare_metal_server_prototype_model = {
                'bandwidth': 10000,
                'initialization': bare_metal_server_initialization_prototype_model,
                'primary_network_interface':
                bare_metal_server_primary_network_interface_prototype_model,
                'profile': bare_metal_server_profile_identity_model,
                'name':'my-baremetal-server',
                'zone':zone_identity_model
            }
            bare_metal_server = vpc_service.create_bare_metal_server(
                bare_metal_server_prototype=bare_metal_server_prototype_model,
                ).get_result()

            # end-create_bare_metal_server
            assert bare_metal_server is not None

            data['baremetalId'] = bare_metal_server['id']
        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    @pytest.mark.skip(reason="mock")
    def test_create_bare_metal_server_console_access_token_example(self):
        """
        create_bare_metal_server_console_access_token request example
        """
        try:
            print('\ncreate_bare_metal_server_console_access_token() result:')
            # begin-create_bare_metal_server_console_access_token

            bare_metal_server_console_access_token = vpc_service.create_bare_metal_server_console_access_token(
                bare_metal_server_id=data['baremetalId'],
                console_type='serial').get_result()

            # end-create_bare_metal_server_console_access_token
            assert bare_metal_server_console_access_token is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_bare_metal_server_disks_example(self):
        """
        list_bare_metal_server_disks request example
        """
        try:
            print('\nlist_bare_metal_server_disks() result:')
            # begin-list_bare_metal_server_disks

            bare_metal_server_disk_collection = vpc_service.list_bare_metal_server_disks(
                bare_metal_server_id=data['baremetalId']).get_result()
            # end-list_bare_metal_server_disks
            assert bare_metal_server_disk_collection is not None
            data['baremetalDiskId']=bare_metal_server_disk_collection['disks'][0]['id']
        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_bare_metal_server_disk_example(self):
        """
        get_bare_metal_server_disk request example
        """
        try:
            print('\nget_bare_metal_server_disk() result:')
            # begin-get_bare_metal_server_disk

            bare_metal_server_disk = vpc_service.get_bare_metal_server_disk(
                bare_metal_server_id=data['baremetalId'],
                id=data['baremetalDiskId']).get_result()

            # end-get_bare_metal_server_disk
            assert bare_metal_server_disk is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_bare_metal_server_disk_example(self):
        """
        update_bare_metal_server_disk request example
        """
        try:
            print('\nupdate_bare_metal_server_disk() result:')
            # begin-update_bare_metal_server_disk

            bare_metal_server_disk_patch_model = {}

            bare_metal_server_disk = vpc_service.update_bare_metal_server_disk(
                bare_metal_server_id=data['baremetalId'],
                id=data['baremetalDiskId'],
                bare_metal_server_disk_patch=bare_metal_server_disk_patch_model
            ).get_result()

            # end-update_bare_metal_server_disk
            assert bare_metal_server_disk is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_bare_metal_server_network_interfaces_example(self):
        """
        list_bare_metal_server_network_interfaces request example
        """
        try:
            print('\nlist_bare_metal_server_network_interfaces() result:')
            # begin-list_bare_metal_server_network_interfaces

            all_results = []
            pager = BareMetalServerNetworkInterfacesPager(
                client=vpc_service,
                bare_metal_server_id=data['baremetalId'],
                limit=10,
            )
            while pager.has_next():
                next_page = pager.get_next()
                assert next_page is not None
                all_results.extend(next_page)


            # end-list_bare_metal_server_network_interfaces

            print(json.dumps(all_results, indent=2))
            assert all_results is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_bare_metal_server_network_interface_example(self):
        """
        create_bare_metal_server_network_interface request example
        """
        try:
            print('\ncreate_bare_metal_server_network_interface() result:')
            # begin-create_bare_metal_server_network_interface

            bare_metal_server_network_interface_prototype_model = {
                'interface_type': 'vlan',
                'subnet': {
                    'id': data['subnetId']
                },
                'vlan': 4,
            }

            bare_metal_server_network_interface = vpc_service.create_bare_metal_server_network_interface(
                bare_metal_server_id=data['baremetalId'],
                bare_metal_server_network_interface_prototype=
                bare_metal_server_network_interface_prototype_model).get_result(
                )

            # end-create_bare_metal_server_network_interface
            assert bare_metal_server_network_interface is not None
            data['bm_nic_id']=bare_metal_server_network_interface['id']

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_bare_metal_server_network_interface_example(self):
        """
        get_bare_metal_server_network_interface request example
        """
        try:
            print('\nget_bare_metal_server_network_interface() result:')
            # begin-get_bare_metal_server_network_interface

            bare_metal_server_network_interface = vpc_service.get_bare_metal_server_network_interface(
                bare_metal_server_id=data['baremetalId'],
                id=data['bm_nic_id']).get_result()

            # end-get_bare_metal_server_network_interface
            assert bare_metal_server_network_interface is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_bare_metal_server_network_interface_example(self):
        """
        update_bare_metal_server_network_interface request example
        """
        try:
            print('\nupdate_bare_metal_server_network_interface() result:')
            # begin-update_bare_metal_server_network_interface

            bare_metal_server_network_interface_patch_model = {
                'name': 'my-network-interface'
            }

            bare_metal_server_network_interface = vpc_service.update_bare_metal_server_network_interface(
                bare_metal_server_id=data['baremetalId'],
                id=data['bm_nic_id'],
                bare_metal_server_network_interface_patch=
                bare_metal_server_network_interface_patch_model).get_result()

            # end-update_bare_metal_server_network_interface
            assert bare_metal_server_network_interface is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_add_bare_metal_server_network_interface_floating_ip_example(self):
        """
        add_bare_metal_server_network_interface_floating_ip request example
        """
        try:
            print(
                '\nadd_bare_metal_server_network_interface_floating_ip() result:'
            )
            # begin-add_bare_metal_server_network_interface_floating_ip

            floating_ip = vpc_service.add_bare_metal_server_network_interface_floating_ip(
                bare_metal_server_id=data['baremetalId'],
                network_interface_id=data['bm_nic_id'],
                id=data['floatingIpId']).get_result()

            # end-add_bare_metal_server_network_interface_floating_ip
            assert floating_ip is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_bare_metal_server_network_interface_floating_ips_example(
            self):
        """
        list_bare_metal_server_network_interface_floating_ips request example
        """
        try:
            print(
                '\nlist_bare_metal_server_network_interface_floating_ips() result:'
            )
            # begin-list_bare_metal_server_network_interface_floating_ips

            floating_ip_unpaginated_collection = vpc_service.list_bare_metal_server_network_interface_floating_ips(
                bare_metal_server_id=data['baremetalId'],
                network_interface_id=data['bm_nic_id']).get_result()

            # end-list_bare_metal_server_network_interface_floating_ips
            assert floating_ip_unpaginated_collection is not None
            data['bm_nic_fip_id'] = floating_ip_unpaginated_collection['floating_ips'][0]['id']
        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_bare_metal_server_network_interface_floating_ip_example(self):
        """
        get_bare_metal_server_network_interface_floating_ip request example
        """
        try:
            print(
                '\nget_bare_metal_server_network_interface_floating_ip() result:'
            )
            # begin-get_bare_metal_server_network_interface_floating_ip

            floating_ip = vpc_service.get_bare_metal_server_network_interface_floating_ip(
                bare_metal_server_id=data['baremetalId'],
                network_interface_id=data['bm_nic_id'],
                id=data['bm_nic_fip_id']).get_result()

            # end-get_bare_metal_server_network_interface_floating_ip
            assert floating_ip is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    @pytest.mark.skip(reason="mock")
    def test_list_bare_metal_server_network_interface_ips_example(self):
        """
        list_bare_metal_server_network_interface_ips request example
        """
        try:
            print('\nlist_bare_metal_server_network_interface_ips() result:')
            # begin-list_bare_metal_server_network_interface_ips

            reserved_ips = vpc_service.list_bare_metal_server_network_interface_ips(
                bare_metal_server_id=data['baremetalId'],
                network_interface_id=data['bm_nic_id']
            ).get_result()

            # end-list_bare_metal_server_network_interface_ips
            assert reserved_ips is not None
        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    @pytest.mark.skip(reason="mock")
    def test_get_bare_metal_server_network_interface_ip_example(self):
        """
        get_bare_metal_server_network_interface_ip request example
        """
        try:
            print('\nget_bare_metal_server_network_interface_ip() result:')
            # begin-get_bare_metal_server_network_interface_ip

            reserved_ip = vpc_service.get_bare_metal_server_network_interface_ip(
                bare_metal_server_id=data['baremetalId'],
                network_interface_id=data['bm_nic_id'],
                id=data['subnetReservedIp']
            ).get_result()

            # end-get_bare_metal_server_network_interface_ip

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_bare_metal_server_example(self):
        """
        get_bare_metal_server request example
        """
        try:
            print('\nget_bare_metal_server() result:')
            # begin-get_bare_metal_server

            bare_metal_server = vpc_service.get_bare_metal_server(
                id=data['baremetalId']).get_result()

            # end-get_bare_metal_server
            assert bare_metal_server is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_bare_metal_server_example(self):
        """
        update_bare_metal_server request example
        """
        try:
            print('\nupdate_bare_metal_server() result:')
            # begin-update_bare_metal_server

            bare_metal_server_patch_model = {
                'name': 'my-baremetal-server-updated'
            }

            bare_metal_server = vpc_service.update_bare_metal_server(
                id=data['baremetalId'],
                bare_metal_server_patch=bare_metal_server_patch_model
            ).get_result()

            # end-update_bare_metal_server
            assert bare_metal_server is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_bare_metal_server_initialization_example(self):
        """
        get_bare_metal_server_initialization request example
        """
        try:
            print('\nget_bare_metal_server_initialization() result:')
            # begin-get_bare_metal_server_initialization

            bare_metal_server_initialization = vpc_service.get_bare_metal_server_initialization(
                id=data['baremetalId']).get_result()

            # end-get_bare_metal_server_initialization
            assert bare_metal_server_initialization is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_restart_bare_metal_server_example(self):
        """
        restart_bare_metal_server request example
        """
        try:
            # begin-restart_bare_metal_server

            response = vpc_service.restart_bare_metal_server(
                id=data['baremetalId'])

            # end-restart_bare_metal_server
            assert response is not None
            print('\nrestart_bare_metal_server() response status code: ',
                  response.get_status_code())

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_start_bare_metal_server_example(self):
        """
        start_bare_metal_server request example
        """
        try:
            # begin-start_bare_metal_server

            response = vpc_service.start_bare_metal_server(
                id=data['baremetalId'])

            # end-start_bare_metal_server
            assert response is not None
            print('\nstart_bare_metal_server() response status code: ',
                  response.get_status_code())

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_stop_bare_metal_server_example(self):
        """
        stop_bare_metal_server request example
        """
        try:
            # begin-stop_bare_metal_server

            response = vpc_service.stop_bare_metal_server(
                id=data['baremetalId'], type='soft')

            # end-stop_bare_metal_server
            assert response is not None
            print('\nstop_bare_metal_server() response status code: ',
                  response.get_status_code())

        except ApiException as e:
            pytest.fail(str(e))


    @needscredentials
    def test_remove_bare_metal_server_network_interface_floating_ip_example(
            self):
        """
        remove_bare_metal_server_network_interface_floating_ip request example
        """
        try:
            # begin-remove_bare_metal_server_network_interface_floating_ip

            response = vpc_service.remove_bare_metal_server_network_interface_floating_ip(
                bare_metal_server_id=data['baremetalId'],
                network_interface_id=data['bm_nic_id'],
                id=data['bm_nic_fip_id'])

            # end-remove_bare_metal_server_network_interface_floating_ip
            assert response is not None
            print(
                '\nremove_bare_metal_server_network_interface_floating_ip() response status code: ',
                response.get_status_code())

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_bare_metal_server_network_interface_example(self):
        """
        delete_bare_metal_server_network_interface request example
        """
        try:
            # begin-delete_bare_metal_server_network_interface

            response = vpc_service.delete_bare_metal_server_network_interface(
                bare_metal_server_id=data['baremetalId'], id=data['bm_nic_id'])

            # end-delete_bare_metal_server_network_interface
            assert response is not None
            print(
                '\ndelete_bare_metal_server_network_interface() response status code: ',
                response.get_status_code())

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_bare_metal_server_example(self):
        """
        delete_bare_metal_server request example
        """
        try:
            # begin-delete_bare_metal_server

            response = vpc_service.delete_bare_metal_server(id=data['baremetalId'])

            # end-delete_bare_metal_server
            assert response is not None
            print('\ndelete_bare_metal_server() response status code: ',
                  response.get_status_code())

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_list_backup_policies_example(self):
        """
        list_backup_policies request example
        """
        try:
            print('\nlist_backup_policies() result:')
            # begin-list_backup_policies

            all_results = []
            pager = BackupPoliciesPager(
                client=vpc_service,
                limit=10,
            )
            while pager.has_next():
                next_page = pager.get_next()
                assert next_page is not None
                all_results.extend(next_page)


            # end-list_backup_policies

            print(json.dumps(all_results, indent=2))

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_backup_policy_example(self):
        """
        create_backup_policy request example
        """
        try:
            print('\ncreate_backup_policy() result:')
            # begin-create_backup_policy
            backup_policy_plan_deletion_trigger_prototype_model = {
                'delete_after': 20,
                'delete_over_count': 20,
            }

            backup_policy_plan_prototype_model = {
                'active': True,
                'attach_user_tags': ['my-daily-backup-plan'],
                'copy_user_tags': True,
                'cron_spec': '*/5 1,2,3 * * *',
                'deletion_trigger': backup_policy_plan_deletion_trigger_prototype_model,
                'name': 'my-backup-policy-plan',
            }
            backup_policy_prototype = {
                'match_user_tags': ['my-daily-backup-policy'],
                'match_resource_type':['volume'],
                'name':'my-backup-policy',
                'plans':[backup_policy_plan_prototype_model],
            }
            backup_policy_response = vpc_service.create_backup_policy(
                backup_policy_prototype = backup_policy_prototype
            )
            backup_policy = backup_policy_response.get_result()
            data['backupPolicyETag'] = backup_policy_response.get_headers()['ETag']
            # end-create_backup_policy

        except ApiException as e:
            pytest.fail(str(e))
        data['backupPolicyID'] = backup_policy['id']

    @needscredentials
    def test_list_backup_policy_plans_example(self):
        """
        list_backup_policy_plans request example
        """
        try:
            print('\nlist_backup_policy_plans() result:')
            # begin-list_backup_policy_plans

            backup_policy_plan_collection = vpc_service.list_backup_policy_plans(
                backup_policy_id=data['backupPolicyID']
            ).get_result()
            # end-list_backup_policy_plans

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_backup_policy_plan_example(self):
        """
        create_backup_policy_plan request example
        """
        try:
            print('\ncreate_backup_policy_plan() result:')
            zoneName = data['zone']
            # begin-create_backup_policy_plan

            backup_policy_plan_deletion_trigger_prototype_model = {
                'delete_after': 20,
                'delete_over_count': 20,
            }
            zone_identity_model = {
                'name': zoneName,
            }
            backup_policy_plan_clone_policy_prototype_model = {
                'max_snapshots': 38,
                'zones': [zone_identity_model],
            }
            backup_policy_plan_remote_region_policies_protoype_model = [
                {
                    'delete_over_count': 2,
                    'region': "us-south",
                },
                {
                    'delete_over_count': 2,
                    'region': "jp-tok",
                },
            ]
            backup_policy_plan_response = vpc_service.create_backup_policy_plan(
                backup_policy_id=data['backupPolicyID'],
                cron_spec='*/5 1,2,3 * * *',
                active=True,
                attach_user_tags=['my-daily-backup-plan'],
                copy_user_tags=True,
                remote_region_policies=backup_policy_plan_remote_region_policies_protoype_model,
                clone_policy=backup_policy_plan_clone_policy_prototype_model,
                deletion_trigger=backup_policy_plan_deletion_trigger_prototype_model,
                name='my-backup-policy-plan'
            )
            backup_policy_plan = backup_policy_plan_response.get_result()
            data['backupPolicyPlanETag'] = backup_policy_plan_response.get_headers()['ETag']
            # end-create_backup_policy_plan

        except ApiException as e:
            pytest.fail(str(e))
        data['backupPolicyPlanID'] = backup_policy_plan['id']

    @needscredentials
    def test_get_backup_policy_plan_example(self):
        """
        get_backup_policy_plan request example
        """
        try:
            print('\nget_backup_policy_plan() result:')
            # begin-get_backup_policy_plan

            backup_policy_plan = vpc_service.get_backup_policy_plan(
                backup_policy_id=data['backupPolicyID'],
                id=data['backupPolicyPlanID']
            ).get_result()

            print(json.dumps(backup_policy_plan, indent=2))

            # end-get_backup_policy_plan

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_backup_policy_plan_example(self):
        """
        update_backup_policy_plan request example
        """
        try:
            print('\nupdate_backup_policy_plan() result:')
            # begin-update_backup_policy_plan

            backup_policy_plan_patch_model = {}
            backup_policy_plan_patch_model['name'] = 'my-backup-policy-plan-updated'
            backup_policy_plan_remote_region_policies_updated = [
                {
                    'delete_over_count': 2,
                    'region': "us-south",
                },
                {
                    'delete_over_count': 3,
                    'region': "jp-tok",
                },
                {
                    'delete_over_count': 4,
                    'region': "eu-de",
                },
            ]
            backup_policy_plan_patch_model['remote_region_policies'] = backup_policy_plan_remote_region_policies_updated
            backup_policy_plan = vpc_service.update_backup_policy_plan(
                backup_policy_id=data['backupPolicyID'],
                id=data['backupPolicyPlanID'],
                backup_policy_plan_patch=backup_policy_plan_patch_model,
                if_match=data['backupPolicyPlanETag']
            ).get_result()

            print(json.dumps(backup_policy_plan, indent=2))

            # end-update_backup_policy_plan

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    @pytest.mark.skip(reason="mock")
    def test_list_backup_policy_jobs_example(self):
        """
        list_backup_policy_jobs request example
        """
        try:
            print('\nlist_backup_policy_jobs() result:')
            # begin-list_backup_policy_jobs

            all_results = []
            pager = BackupPolicyJobsPager(
                client=vpc_service,
                backup_policy_id=data['backupPolicyID'],
            )
            while pager.has_next():
                next_page = pager.get_next()
                assert next_page is not None
                all_results.extend(next_page)

            # end-list_backup_policy_jobs
            print(json.dumps(all_results, indent=2))
        except ApiException as e:
            pytest.fail(str(e))
        data['backupPolicyJobID'] = all_results[0]['id']

    @needscredentials
    @pytest.mark.skip(reason="mock")
    def test_get_backup_policy_job_example(self):
        """
        get_backup_policy_job request example
        """
        try:
            print('\nget_backup_policy_job() result:')
            # begin-get_backup_policy_job

            response = vpc_service.get_backup_policy_job(
                backup_policy_id=data['backupPolicyID'],
                id=data['backupPolicyJobID']
            )
            backup_policy_job = response.get_result()

            # end-get_backup_policy_job
            print(json.dumps(backup_policy_job, indent=2))
        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_backup_policy_example(self):
        """
        get_backup_policy request example
        """
        try:
            print('\nget_backup_policy() result:')
            # begin-get_backup_policy

            backup_policy = vpc_service.get_backup_policy(
                id=data['backupPolicyID']
            ).get_result()

            print(json.dumps(backup_policy, indent=2))

            # end-get_backup_policy

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_backup_policy_example(self):
        """
        update_backup_policy request example
        """
        try:
            print('\nupdate_backup_policy() result:')
            # begin-update_backup_policy

            backup_policy_patch_model = {}
            backup_policy_patch_model['name'] = 'my-backup-policy-updated'

            backup_policy = vpc_service.update_backup_policy(
                id=data['backupPolicyID'],
                backup_policy_patch=backup_policy_patch_model,
                if_match=data['backupPolicyETag']
            ).get_result()

            print(json.dumps(backup_policy, indent=2))

            # end-update_backup_policy

        except ApiException as e:
            pytest.fail(str(e))
            

    @needscredentials
    def test_delete_backup_policy_plan_example(self):
        """
        delete_backup_policy_plan request example
        """
        try:
            print('\ndelete_backup_policy_plan() result:')
            # begin-delete_backup_policy_plan

            backup_policy_plan = vpc_service.delete_backup_policy_plan(
                backup_policy_id=data['backupPolicyID'],
                id=data['backupPolicyPlanID'],
                if_match=data['backupPolicyPlanETag']
            ).get_result()

            print(json.dumps(backup_policy_plan, indent=2))

            # end-delete_backup_policy_plan

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_backup_policy_example(self):
        """
        delete_backup_policy request example
        """
        try:
            print('\ndelete_backup_policy() result:')
            # begin-delete_backup_policy

            backup_policy = vpc_service.delete_backup_policy(
                id=data['backupPolicyID'],
                if_match=data['backupPolicyETag']
            ).get_result()

            print(json.dumps(backup_policy, indent=2))

            # end-delete_backup_policy

        except ApiException as e:
            pytest.fail(str(e))
    @needscredentials
    def test_list_flow_log_collectors_example(self):
        """
        list_flow_log_collectors request example
        """
        try:
            print('\nlist_flow_log_collectors() result:')
            # begin-list_flow_log_collectors

            all_results = []
            pager = FlowLogCollectorsPager(
                client=vpc_service,
                limit=10,
            )
            while pager.has_next():
                next_page = pager.get_next()
                assert next_page is not None
                all_results.extend(next_page)

            # end-list_flow_log_collectors
            print(json.dumps(all_results, indent=2))

            assert all_results is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_create_flow_log_collector_example(self):
        """
        create_flow_log_collector request example
        """
        try:
            print('\ncreate_flow_log_collector() result:')
            # begin-create_flow_log_collector

            cloud_object_storage_bucket_identity_model = {}
            cloud_object_storage_bucket_identity_model['name'] = 'my-bucket-name'

            flow_log_collector_target_prototype_model = {}
            flow_log_collector_target_prototype_model['id'] = data['subnetId']

            flow_log_collector = vpc_service.create_flow_log_collector(
                storage_bucket=cloud_object_storage_bucket_identity_model,
                target=flow_log_collector_target_prototype_model,
                name='my-flow-log-collector').get_result()

            # end-create_flow_log_collector

            assert flow_log_collector is not None
            data['flowLogId']=flow_log_collector['id']

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_get_flow_log_collector_example(self):
        """
        get_flow_log_collector request example
        """
        try:
            print('\nget_flow_log_collector() result:')
            # begin-get_flow_log_collector

            flow_log_collector = vpc_service.get_flow_log_collector(
                id=data['flowLogId']).get_result()

            # end-get_flow_log_collector

            assert flow_log_collector is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_update_flow_log_collector_example(self):
        """
        update_flow_log_collector request example
        """
        try:
            print('\nupdate_flow_log_collector() result:')
            # begin-update_flow_log_collector

            flow_log_collector_patch_model = {}
            flow_log_collector_patch_model['name'] = 'my-flow-log-collector-updated'
            flow_log_collector_patch_model['active'] = True

            flow_log_collector = vpc_service.update_flow_log_collector(
                id=data['flowLogId'],
                flow_log_collector_patch=flow_log_collector_patch_model
            ).get_result()

            # end-update_flow_log_collector

            assert flow_log_collector is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_flow_log_collector_example(self):
        """
        delete_flow_log_collector request example
        """
        try:
            # begin-delete_flow_log_collector

            response = vpc_service.delete_flow_log_collector(id=data['flowLogId'])

            # end-delete_flow_log_collector
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_remove_vpn_gateway_connection_peer_cidr_example(self):
        """
        remove_vpn_gateway_connection_peer_cidr request example
        """
        try:
            # begin-remove_vpn_gateway_connection_peer_cidr

            response = vpc_service.remove_vpn_gateway_connections_peer_cidr(
                vpn_gateway_id=data['vpnGatewayId'],
                id=data['vpnGatewayConnectionId'],
                cidr='192.144.0.0/28')

            # end-remove_vpn_gateway_connection_peer_cidr
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_remove_vpn_gateway_connection_local_cidr_example(self):
        """
        remove_vpn_gateway_connection_local_cidr request example
        """
        try:
            # begin-remove_vpn_gateway_connection_local_cidr

            response = vpc_service.remove_vpn_gateway_connections_local_cidr(
                vpn_gateway_id=data['vpnGatewayId'],
                id=data['vpnGatewayConnectionId'],
                cidr='192.144.0.0/28')

            # end-remove_vpn_gateway_connection_local_cidr
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_remove_instance_network_interface_floating_ip_example(self):
        """
        remove_instance_network_interface_floating_ip request example
        """
        try:
            # begin-remove_instance_network_interface_floating_ip

            response = vpc_service.remove_instance_network_interface_floating_ip(
                instance_id=data['instanceId'],
                network_interface_id=data['eth2Id'],
                id=data['floatingIpId'])

            # end-remove_instance_network_interface_floating_ip
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_security_group_target_binding_example(self):
        """
        delete_security_group_target_binding request example
        """
        try:
            # begin-delete_security_group_target_binding

            response = vpc_service.delete_security_group_target_binding(
                security_group_id=data['securityGroupId'], id=data['targetId'])

            # end-delete_security_group_target_binding
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_instance_network_interface_example(self):
        """
        delete_instance_network_interface request example
        """
        try:
            # begin-delete_instance_network_interface

            response = vpc_service.delete_instance_network_interface(
                instance_id=data['instanceId'], id=data['eth2Id'])

            # end-delete_instance_network_interface
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_instance_volume_attachment_example(self):
        """
        delete_instance_volume_attachment request example
        """
        try:
            # begin-delete_instance_volume_attachment

            response = vpc_service.delete_instance_volume_attachment(
                instance_id=data['instanceId'], id=data['volumeAttachmentId'])

            # end-delete_instance_volume_attachment
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))



    @needscredentials
    def test_delete_floating_ip_example(self):
        """
        delete_floating_ip request example
        """
        try:
            # begin-delete_floating_ip

            response = vpc_service.delete_floating_ip(id=data['floatingIpId'])

            # end-delete_floating_ip
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_instance_example(self):
        """
        delete_instance request example
        """
        try:
            # begin-delete_instance

            response = vpc_service.delete_instance(id=data['instanceId'])

            # end-delete_instance
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_key_example(self):
        """
        delete_key request example
        """
        try:
            # begin-delete_key

            response = vpc_service.delete_key(id=data['keyId'])

            # end-delete_key
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_image_example(self):
        """
        delete_image request example
        """
        try:
            # begin-delete_image

            response = vpc_service.delete_image(id=data['imageId'])

            # end-delete_image
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_snapshot_clone_example(self):
        """
        delete_snapshot_clone request example
        """
        try:
            zoneName = data['zone']
            snapshotID = data['snapshotId']
            # begin-delete_snapshot_clone

            response = vpc_service.delete_snapshot_clone(
                id=snapshotID,
                zone_name=zoneName,
            )

            # end-delete_snapshot_clone
            print('\ndelete_snapshot_clone() response status code: ', response.get_status_code())

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_share_mount_target_example(self):
        """
        delete_share_mount_target request example
        """
        try:
            print('\ndelete_share_mount_target() result:')
            # begin-delete_share_mount_target

            response = vpc_service.delete_share_mount_target(
                share_id=data['shareId'],
                id=data['shareMountTargetId'],
            )
            share_mount_target = response.get_result()

            # end-delete_share_mount_target
            print('\ndelete_share_mount_target() response status code: ', response.get_status_code())

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    @pytest.mark.skip(reason="mock")
    def test_delete_share_source_example(self):
        """
        delete_share_source request example
        """
        try:
            # begin-delete_share_source

            response = vpc_service.delete_share_source(
                share_id=data['shareReplicaId'],
            )
            # end-delete_share_source
            print('\ndelete_share_source() response status code: ', response.get_status_code())

        except ApiException as e:
            pytest.fail(str(e))


    @needscredentials
    def test_delete_share_example(self):
        """
        delete_share request example
        """
        try:
            print('\ndelete_share() result:')
            # begin-delete_share

            response = vpc_service.delete_share(
                id=data['shareId'],
                if_match=data['shareETag'],
            )
            response_replica = vpc_service.delete_share(
                id=data['shareReplicaId'],
                if_match=data['shareReplicaETag'],
            )
            share = response.get_result()
            # end-delete_share
            print('\ndelete_share() response status code: ', response.get_status_code())
            print('\ndelete_share() response status code: ', response_replica.get_status_code())

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_snapshot_example(self):
        """
        delete_snapshot request example
        """
        try:
            # begin-delete_snapshot

            response = vpc_service.delete_snapshot(id=data['snapshotId'])

            # end-delete_snapshot
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    @pytest.mark.skip(reason="mock error")
    def test_delete_snapshots_example(self):
        
        """
        delete_snapshots request example
        """
        try:
            # begin-delete_snapshots

            response = vpc_service.delete_snapshots(
                source_volume_id=data['volumeId'])

            # end-delete_snapshots
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_volume_example(self):
        """
        delete_volume request example
        """
        try:
            # begin-delete_volume

            response = vpc_service.delete_volume(id=data['volumeId'])

            # end-delete_volume
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_security_group_rule_example(self):
        """
        delete_security_group_rule request example
        """
        try:
            # begin-delete_security_group_rule

            response = vpc_service.delete_security_group_rule(
                security_group_id=data['securityGroupId'], id=data['securityGroupRuleId'])

            # end-delete_security_group_rule
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_security_group_example(self):
        """
        delete_security_group request example
        """
        try:
            # begin-delete_security_group

            response = vpc_service.delete_security_group(id=data['securityGroupId'])

            # end-delete_security_group
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_public_gateway_example(self):
        """
        delete_public_gateway request example
        """
        try:
            # begin-delete_public_gateway

            response = vpc_service.delete_public_gateway(id=data['publicGatewayId'])

            # end-delete_public_gateway
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_network_acl_rule_example(self):
        """
        delete_network_acl_rule request example
        """
        try:
            # begin-delete_network_acl_rule

            response = vpc_service.delete_network_acl_rule(
                network_acl_id=data['networkACLId'], id=data['networkACLRuleId'])

            # end-delete_network_acl_rule
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_network_acl_example(self):
        """
        delete_network_acl request example
        """
        try:
            # begin-delete_network_acl

            response = vpc_service.delete_network_acl(id=data['networkACLId'])

            # end-delete_network_acl
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_instance_group_membership_example(self):
        """
        delete_instance_group_membership request example
        """
        try:
            # begin-delete_instance_group_membership

            response = vpc_service.delete_instance_group_membership(
                instance_group_id=data['instanceGroupId'], id=data['instanceGroupMembershipId'])

            # end-delete_instance_group_membership
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_instance_group_memberships_example(self):
        """
        delete_instance_group_memberships request example
        """
        try:
            # begin-delete_instance_group_memberships

            response = vpc_service.delete_instance_group_memberships(
                instance_group_id=data['instanceGroupId'])

            # end-delete_instance_group_memberships
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_instance_group_manager_policy_example(self):
        """
        delete_instance_group_manager_policy request example
        """
        try:
            # begin-delete_instance_group_manager_policy

            response = vpc_service.delete_instance_group_manager_policy(
                instance_group_id=data['instanceGroupId'],
                instance_group_manager_id=data['instanceGroupManagerId'],
                id=data['instanceGroupManagerPolicyId'])

            # end-delete_instance_group_manager_policy
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_instance_group_manager_action_example(self):
        """
        delete_instance_group_manager_action request example
        """
        try:
            # begin-delete_instance_group_manager_action

            response = vpc_service.delete_instance_group_manager_action(
                instance_group_id=data['instanceGroupId'],
                instance_group_manager_id=data['instanceGroupManagerId'],
                id=data['instanceGroupManagerActionId'])

            # end-delete_instance_group_manager_action
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_instance_group_manager_example(self):
        """
        delete_instance_group_manager request example
        """
        try:
            # begin-delete_instance_group_manager

            response = vpc_service.delete_instance_group_manager(
                instance_group_id=data['instanceGroupId'], id=data['instanceGroupManagerId'])

            # end-delete_instance_group_manager
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    @pytest.mark.skip(reason="mock")
    def test_delete_instance_group_load_balancer_example(self):
        """
        delete_instance_group_load_balancer request example
        """
        try:
            # begin-delete_instance_group_load_balancer

            response = vpc_service.delete_instance_group_load_balancer(
                instance_group_id=data['instanceGroupId'])

            # end-delete_instance_group_load_balancer
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_instance_group_example(self):
        """
        delete_instance_group request example
        """
        try:
            # begin-delete_instance_group

            response = vpc_service.delete_instance_group(id=data['instanceGroupId'])

            # end-delete_instance_group
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_instance_template_example(self):
        """
        delete_instance_template request example
        """
        try:
            # begin-delete_instance_template

            response = vpc_service.delete_instance_template(id=data['instanceTemplateId'])

            # end-delete_instance_template
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_dedicated_host_example(self):
        """
        delete_dedicated_host request example
        """
        try:
            # begin-delete_dedicated_host

            response = vpc_service.delete_dedicated_host(id=data['dedicatedHostId'])

            # end-delete_dedicated_host
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_dedicated_host_group_example(self):
        """
        delete_dedicated_host_group request example
        """
        try:
            # begin-delete_dedicated_host_group

            response = vpc_service.delete_dedicated_host_group(id=data['dedicatedHostGroupId'])

            # end-delete_dedicated_host_group
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_subnet_example(self):
        """
        delete_subnet request example
        """
        try:
            # begin-delete_subnet

            response = vpc_service.delete_subnet(id=data['subnetId'])

            # end-delete_subnet
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_ike_policy_example(self):
        """
        delete_ike_policy request example
        """
        try:
            # begin-delete_ike_policy

            response = vpc_service.delete_ike_policy(id=data['ikePolicyId'])

            # end-delete_ike_policy
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_ipsec_policy_example(self):
        """
        delete_ipsec_policy request example
        """
        try:
            # begin-delete_ipsec_policy

            response = vpc_service.delete_ipsec_policy(id=data['ipsecPolicyId'])

            # end-delete_ipsec_policy
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_vpn_gateway_connection_example(self):
        """
        delete_vpn_gateway_connection request example
        """
        try:
            # begin-delete_vpn_gateway_connection

            response = vpc_service.delete_vpn_gateway_connection(
                vpn_gateway_id=data['vpnGatewayId'], id=data['vpnGatewayConnectionId'])

            # end-delete_vpn_gateway_connection
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_vpn_gateway_example(self):
        """
        delete_vpn_gateway request example
        """
        try:
            # begin-delete_vpn_gateway

            response = vpc_service.delete_vpn_gateway(id=data['vpnGatewayId'])

            # end-delete_vpn_gateway
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_vpc_routing_table_route_example(self):
        """
        delete_vpc_routing_table_route request example
        """
        try:
            # begin-delete_vpc_routing_table_route

            response = vpc_service.delete_vpc_routing_table_route(
                vpc_id=data['vpcID'],
                routing_table_id=data['vpcRoutingTableId'],
                id=data['vpcRoutingTableRouteId'])

            # end-delete_vpc_routing_table_route
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_vpc_routing_table_example(self):
        """
        delete_vpc_routing_table request example
        """
        try:
            # begin-delete_vpc_routing_table

            response = vpc_service.delete_vpc_routing_table(vpc_id=data['vpcID'],
                                                            id=data['vpcRoutingTableId'])

            # end-delete_vpc_routing_table
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_vpc_address_prefix_example(self):
        """
        delete_vpc_address_prefix request example
        """
        try:
            # begin-delete_vpc_address_prefix

            response = vpc_service.delete_vpc_address_prefix(
                vpc_id=data['vpcID'], id=data['vpcAddressPrefixId'])

            # end-delete_vpc_address_prefix
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_vpc_dns_resolution_binding_example(self):
        """
        delete_vpc_dns_resolution_binding request example
        """
        try:
            # begin-delete_vpc_dns_resolution_binding

            response = vpc_service.delete_vpc_dns_resolution_binding(
                vpc_id=data['vpcID'],
                id=data['vpcDnsResolutionBindingID'],
            )

            # end-delete_vpc_dns_resolution_binding

        except ApiException as e:
            pytest.fail(str(e))

    @needscredentials
    def test_delete_vpc_example(self):
        """
        delete_vpc request example
        """
        try:
            # begin-delete_vpc

            response = vpc_service.delete_vpc(id=data['vpcID'])

            # end-delete_vpc
            assert response is not None

        except ApiException as e:
            pytest.fail(str(e))

# endregion
##############################################################################
# End of Examples for Service: VpcV1
##############################################################################
