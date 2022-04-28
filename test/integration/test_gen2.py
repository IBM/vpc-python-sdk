# coding: utf-8

# (C) Copyright IBM Corp. 2020, 2021, 2022.
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

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core.api_exception import ApiException
from ibm_cloud_sdk_core.authenticators.no_auth_authenticator import NoAuthAuthenticator
import json
import pytest
import namegenerator
from ibm_vpc.vpc_v1 import *

store = {}


class TestGeography():
    def test_regions(self, createGen2Service, env):
        regions = list_regions(createGen2Service)
        assert regions.status_code == 200
        region = regions.get_result()['regions'][0]
        store['region'] = region['name']
        if not env:
            store['zone'] = region['zones'][0]['name']

    def test_region(self, createGen2Service):
        region = get_region(createGen2Service, store['region'])
        assert region.status_code == 200

    def test_zones(self, createGen2Service, env):
        zones = list_region_zones(createGen2Service, store['region'])
        assert zones.status_code == 200
        if env:
            store['zone'] = zones.get_result()['zones'][0]['name']

    def test_zone(self, createGen2Service):
        zone = get_region_zone(
            createGen2Service, store['region'], store['zone'])
        assert zone.status_code == 200


class TestFloatingIPs():
    def test_create_floating_ip(self, createGen2Service):
        fip = create_floating_ip(createGen2Service)
        assertCreateResponse(fip)
        store['created_fip_id'] = fip.get_result()['id']

    def test_list_floating_ip(self, createGen2Service):
        fips = list_floating_ips(createGen2Service)
        assertListResponse(fips, 'floating_ips')

    def test_get_floating_ip(self, createGen2Service):
        fip = get_floating_ip(createGen2Service, store['created_fip_id'])
        assertGetPatchResponse(fip)

    def test_update_floating_ip(self, createGen2Service):
        fip = update_floating_ip(createGen2Service, store['created_fip_id'])
        assertGetPatchResponse(fip)


class TestImages():
    def test_create_images(self, createGen2Service):
        pytest.skip("no cos bucket")
        image = create_image(createGen2Service)
        assertCreateResponse(image)

    def test_list_images(self, createGen2Service):
        images = list_images(createGen2Service)
        assertListResponse(images, 'images')
        store['image_id'] = images.get_result()['images'][0]['id']

    def test_get_image(self, createGen2Service):
        image = get_image(createGen2Service, store['image_id'])
        assertGetPatchResponse(image)

    def test_update_image(self, createGen2Service):
        pytest.skip("no private image")
        image = update_image(createGen2Service, store['created_image'])
        assertGetPatchResponse(image)

    def test_delete_image(self, createGen2Service):
        pytest.skip("no private image")
        image = delete_image(createGen2Service, store['created_image'])
        assertDeleteResponse(image)

    def test_list_operating_systems(self, createGen2Service):
        oss = list_operating_systems(createGen2Service)
        assertListResponse(oss, 'operating_systems')
        store['operating_system_name'] = oss.get_result()[
            'operating_systems'][0]['name']

    def test_get_operating_system(self, createGen2Service):
        os = get_operating_system(
            createGen2Service, store['operating_system_name']).get_result()
        assert os['name'] == store['operating_system_name']


class TestSSHKeys():
    def test_create_ssh_keys(self, createGen2Service):
        key = create_key(createGen2Service)
        assertCreateResponse(key)
        store['created_key'] = key.get_result()['id']

    def test_list_ssh_keys(self, createGen2Service):
        keys = list_keys(createGen2Service)
        assertListResponse(keys, 'keys')

    def test_get_ssh_key(self, createGen2Service):
        key = get_key(createGen2Service, store['created_key'])
        assertGetPatchResponse(key)

    def test_update_key(self, createGen2Service):
        key = update_key(createGen2Service, store['created_key'])
        assertGetPatchResponse(key)


class TestNetworkACL():
    def test_list_nacl(self, createGen2Service):
        acls = list_network_acls(createGen2Service)
        assertListResponse(acls, 'network_acls')
        store['nacl_id'] = acls.get_result()['network_acls'][0]['id']

    def test_get_nacl(self, createGen2Service):
        acl = get_network_acl(createGen2Service, store['nacl_id'])
        assertGetPatchResponse(acl)

    def test_create_nacl(self, createGen2Service):
        acl = create_network_acl(createGen2Service, store['nacl_id'])
        assertCreateResponse(acl)
        store['created_nacl_id'] = acl.get_result()['id']

    def test_list_nacl_rules(self, createGen2Service):
        acl_rules = list_network_acl_rules(
            createGen2Service, store['created_nacl_id'])
        assertListResponse(acl_rules, 'rules')

    def test_create_nacl_rules(self, createGen2Service):
        acl_rule = create_network_acl_rule(
            createGen2Service, store['created_nacl_id'])
        assertCreateResponse(acl_rule)
        store['created_nacl_rule_id'] = acl_rule.get_result()['id']

    def test_get_nacl_rules(self, createGen2Service):
        acl_rules = get_network_acl_rule(
            createGen2Service, store['created_nacl_id'], store['created_nacl_rule_id'])
        assertGetPatchResponse(acl_rules)

    def test_update_nacl_rules(self, createGen2Service):
        acl_rule = update_network_acl_rule(
            createGen2Service, store['created_nacl_id'], store['created_nacl_rule_id'])
        assertGetPatchResponse(acl_rule)

    def test_delete_nacl_rules(self, createGen2Service):
        acl_rule = delete_network_acl_rule(
            createGen2Service, store['created_nacl_id'], store['created_nacl_rule_id'])
        assertDeleteResponse(acl_rule)

    def test_update_nacl(self, createGen2Service):
        acl = update_network_acl(createGen2Service, store['created_nacl_id'])
        assertGetPatchResponse(acl)


class TestVolume():
    def test_list_vol_profiles(self, createGen2Service):
        profiles = list_volume_profiles(createGen2Service)
        assertListResponse(profiles, 'profiles')
        store['vol_profile'] = profiles.get_result()['profiles'][0]['name']

    def test_get_vol_profile(self, createGen2Service):
        vol = get_volume_profile(createGen2Service, store['vol_profile'])
        assertGetPatchResponse(vol)

    def test_create_volume(self, createGen2Service):
        vol = create_volume(createGen2Service, store['zone'])
        assertCreateResponse(vol)
        store['created_vol'] = vol.get_result()['id']
        print('created_vol: ' + store['created_vol'])

    def test_list_vols(self, createGen2Service):
        vols = list_volumes(createGen2Service)
        assertListResponse(vols, 'volumes')

    def test_get_vol(self, createGen2Service):
        vol = get_volume(createGen2Service, store['created_vol'])
        assertGetPatchResponse(vol)

    def test_update_vol(self, createGen2Service):
        vol = update_volume(createGen2Service, store['created_vol'])
        assertGetPatchResponse(vol)


class TestVPC():
    def test_list_vpc(self, createGen2Service):
        vpcs = list_vpcs(createGen2Service)
        assertListResponse(vpcs, 'vpcs')

    def test_create_vpc(self, createGen2Service):
        vpc = create_vpc(createGen2Service)
        assertCreateResponse(vpc)
        store['created_vpc'] = vpc.get_result()['id']
        print('created_vpc: ' + store['created_vpc'])

    def test_get_vpc(self, createGen2Service):
        vpc = get_vpc(createGen2Service, store['created_vpc'])
        assertGetPatchResponse(vpc)

    def test_update_vpc(self, createGen2Service):
        vpc = update_vpc(createGen2Service, store['created_vpc'])
        assertGetPatchResponse(vpc)


class TestSubnet():
    def test_list_subnet(self, createGen2Service):
        subnets = list_subnets(createGen2Service)
        assertListResponse(subnets, 'subnets')
        subnet = subnets.get_result()['subnets'][0]
        # store['subnet_id'] = subnet['id']
        store['vpc_id'] = subnet['vpc']['id']
        store['zone'] = subnet['zone']['name']

    def test_create_subnet(self, createGen2Service):
        print(store['zone'], store['created_vpc'])
        subnet = create_subnet(
            createGen2Service, store['created_vpc'], store['zone'])
        assertCreateResponse(subnet)
        store['created_subnet'] = subnet.get_result()['id']
        print('created_subnet: ' + store['created_subnet'])

    def test_get_subnet(self, createGen2Service):
        subnet = get_subnet(createGen2Service, store['created_subnet'])
        assertGetPatchResponse(subnet)

    def test_update_subnet(self, createGen2Service):
        subnet = update_subnet(createGen2Service, store['created_subnet'])
        assertGetPatchResponse(subnet)

    def test_update_subnet_nacl(self, createGen2Service):
        subnet_nacl = replace_subnet_network_acl(
            createGen2Service, store['created_subnet'], store['created_nacl_id'])
        assertCreateResponse(subnet_nacl)

    def test_get_subnet_nacl(self, createGen2Service):
        subnet_nacl = get_subnet_network_acl(
            createGen2Service, store['created_subnet'])
        assertGetPatchResponse(subnet_nacl)

    def test_list_subnet_reserved_ips(self, createGen2Service):
        reserved_ips = list_subnet_reserved_ips(
            createGen2Service, store['created_subnet'])
        assertListResponse(reserved_ips, 'reserved_ips')

    def test_create_subnet_reserved_ip(self, createGen2Service):
        reserved_ip = create_subnet_reserved_ip(
            createGen2Service, store['created_subnet'])
        assertCreateResponse(reserved_ip)
        store['created_subnet_reserved_ip'] = reserved_ip.get_result()['id']

    def test_get_subnet_reserved_ip(self, createGen2Service):
        reserved_ip = get_subnet_reserved_ip(
            createGen2Service, store['created_subnet'],  store['created_subnet_reserved_ip'])
        assertGetPatchResponse(reserved_ip)

    def test_update_subnet_reserved_ip(self, createGen2Service):
        reserved_ip = update_subnet_reserved_ip(
            createGen2Service, store['created_subnet'],  store['created_subnet_reserved_ip'])
        assertGetPatchResponse(reserved_ip)


class TestVPCRoutingTables():
    def test_create_vpc_routing_table(self, createGen2Service):
        routing_table = create_vpc_routing_table(
            createGen2Service, store['created_vpc'], store['zone'])
        assertCreateResponse(routing_table)
        store['created_routing_table_id'] = routing_table.get_result()['id']

    def test_list_vpc_routing_tables(self, createGen2Service):
        routing_tables = list_vpc_routing_tables(
            createGen2Service, store['created_vpc'])
        assertListResponse(routing_tables, 'routing_tables')

    def test_create_vpc_routing_table_route(self, createGen2Service):
        route = create_vpc_routing_table_route(
            createGen2Service,
            store['created_vpc'],
            store['created_routing_table_id'],
            store['zone'])
        assertCreateResponse(route)
        store['created_route_id'] = route.get_result()['id']

    def test_list_vpc_routing_table_routes(self, createGen2Service):
        routes = list_vpc_routing_table_routes(
            createGen2Service, store['created_vpc'], store['created_routing_table_id'])
        assertListResponse(routes, 'routes')

    def test_get_vpc_routing_table(self, createGen2Service):
        route = get_vpc_routing_table(
            createGen2Service, store['created_vpc'], store['created_routing_table_id'])
        assertGetPatchResponse(route)

    def test_get_vpc_routing_table_route(self, createGen2Service):
        route = get_vpc_routing_table_route(
            createGen2Service, store['created_vpc'], store['created_routing_table_id'], store['created_route_id'])
        assertGetPatchResponse(route)

    def test_update_vpc_routing_table_route(self, createGen2Service):
        route = update_vpc_routing_table_route(
            createGen2Service, store['created_vpc'], store['created_routing_table_id'], store['created_route_id'])
        assertGetPatchResponse(route)

    def test_update_vpc_routing_table(self, createGen2Service):
        routing_table = update_vpc_routing_table(
            createGen2Service, store['created_vpc'], store['created_routing_table_id'])
        assertGetPatchResponse(routing_table)

    def test_delete_vpc_routing_table_route(self, createGen2Service):
        route = delete_vpc_routing_table_route(
            createGen2Service, store['created_vpc'], store['created_routing_table_id'], store['created_route_id'])
        assertDeleteResponse(route)

    def test_delete_vpc_routing_table(self, createGen2Service):
        routing_table = delete_vpc_routing_table(
            createGen2Service, store['created_vpc'], store['created_routing_table_id'])
        assertDeleteResponse(routing_table)


class TestEndpointGateways():
    def test_create_endpoint_gateway(self, createGen2Service):
        eg = create_endpoint_gateway(createGen2Service,  store['created_vpc'])
        assertCreateResponse(eg)
        store['created_eg_id'] = eg.get_result()['id']

    def test_list_endpoint_gateways(self, createGen2Service):
        egs = list_endpoint_gateways(createGen2Service)
        assertListResponse(egs, 'endpoint_gateways')

    def test_get_endpoint_gateway(self, createGen2Service):
        fip = get_endpoint_gateway(createGen2Service, store['created_eg_id'])
        assertGetPatchResponse(fip)

    def test_update_endpoint_gateway(self, createGen2Service):
        fip = update_endpoint_gateway(
            createGen2Service, store['created_eg_id'])
        assertGetPatchResponse(fip)

    def test_add_endpoint_gateway_ip(self, createGen2Service):
        eg_ip = add_endpoint_gateway_ip(
            createGen2Service, store['created_eg_id'], store['created_subnet_reserved_ip'])
        assertCreateResponse(eg_ip)
        store['created_eg_ip_id'] = eg_ip.get_result()['id']

    def test_list_endpoint_gateway_ips(self, createGen2Service):
        ips = list_endpoint_gateway_ips(
            createGen2Service, store['created_eg_id'])
        assertListResponse(ips, 'ips')

    def test_get_endpoint_gateway_ip(self, createGen2Service):
        fip = get_endpoint_gateway_ip(
            createGen2Service, store['created_eg_id'], store['created_eg_ip_id'])
        assertGetPatchResponse(fip)

    def test_remove_endpoint_gateway_ip(self, createGen2Service):
        vpc = remove_endpoint_gateway_ip(
            createGen2Service, store['created_eg_id'], store['created_eg_ip_id'])
        assertDeleteResponse(vpc)

    def test_delete_endpoint_gateway(self, createGen2Service):
        vpc = delete_endpoint_gateway(
            createGen2Service, store['created_eg_id'])
        assertDeleteResponse(vpc)


class TestPublicGateways():
    def test_create_pgw(self, createGen2Service):
        pgw = create_public_gateway(
            createGen2Service, store['created_vpc'], store['zone'])
        assertCreateResponse(pgw)
        store['created_pgw'] = pgw.get_result()['id']

    def test_list_pgws(self, createGen2Service):
        pgws = list_public_gateways(createGen2Service)
        assertListResponse(pgws, 'public_gateways')

    def test_get_pgw(self, createGen2Service):
        pgw = get_public_gateway(createGen2Service, store['created_pgw'])
        assertGetPatchResponse(pgw)

    def test_update_pgw(self, createGen2Service):
        pgw = update_public_gateway(createGen2Service, store['created_pgw'])
        assertGetPatchResponse(pgw)

    def test_update_subnet_pgw(self, createGen2Service):
        subnet = set_subnet_public_gateway(
            createGen2Service, store['created_subnet'], store['created_pgw'])
        assertCreateResponse(subnet)

    def test_get_subnet_pgw(self, createGen2Service):
        subnet = get_subnet_public_gateway(
            createGen2Service, store['created_subnet'])
        assertGetPatchResponse(subnet)

    def test_delete_subnet_pgw(self, createGen2Service):
        vpc = unset_subnet_public_gateway(
            createGen2Service, store['created_subnet'])
        assertDeleteResponse(vpc)


class TestBareMetalServers():

    def test_list_bare_metal_server_profiles(self, createGen2Service):
        profiles = list_bare_metal_server_profiles(createGen2Service)
        assertListResponse(profiles, 'profiles')
        store['bare_metal_server_profile'] = profiles.get_result()[
            'profiles'][0]['name']

    def test_get_bare_metal_server_profile(self, createGen2Service):
        prof = get_bare_metal_server_profile(
            createGen2Service, store['bare_metal_server_profile'])
        assert prof.status_code == 200
        assert prof.get_result() is not None

    def test_create_bare_metal_server(self, createGen2Service):
        bms = create_bare_metal_server(createGen2Service, store['bare_metal_server_profile'], store['created_subnet'],
                                       store['image_id'], store['created_key'], store['created_vpc'],
                                       store['zone'], 'testString', 'my-bare-metal-server')
        assertCreateResponse(bms)
        store['created_bare_metal_server_id'] = bms.get_result()['id']
        print('created_bare_metal_server_id -' + store['created_bare_metal_server_id'])

    def test_list_bare_metal_servers(self, createGen2Service):
        bare_metal_servers = list_bare_metal_servers(createGen2Service)
        assertListResponse(bare_metal_servers, 'bare_metal_servers')
        bare_metal_server = bare_metal_servers.get_result()['bare_metal_servers'][0]
        store['bare_metal_server_id'] = bare_metal_server['id']
        store['network_interface_id'] = bare_metal_server['primary_network_interface']['id']
        print("primary network interface is - " + store['network_interface_id'])

    def test_get_bare_metal_server(self, createGen2Service):
        bare_metal_server = get_bare_metal_server(
            createGen2Service, store['created_bare_metal_server_id'])
        assertGetPatchResponse(bare_metal_server)

    def test_update_bare_metal_server(self, createGen2Service):
        bare_metal_server = update_bare_metal_server(
            createGen2Service, store['created_bare_metal_server_id'], 'my-bare-metal-server-update', True)
        assertGetPatchResponse(bare_metal_server)

    def test_get_bare_metal_server_initialization(self, createGen2Service):
        bare_metal_server = get_bare_metal_server_initialization(
            createGen2Service, store['created_bare_metal_server_id'])
        assert bare_metal_server.status_code == 200
        assert bare_metal_server.get_result() is not None

    def test_create_bare_metal_server_console_access_token(self, createGen2Service):
        pytest.skip("no env")
        bare_metal_server_access_token = create_bare_metal_server_console_access_token(
            createGen2Service, store['created_bare_metal_server_id'],
            'serial'
        )
        assert bare_metal_server_access_token.status_code == 200
        assert bare_metal_server_access_token.get_result() is not None

    def test_list_bare_metal_server_disks(self, createGen2Service):
        bare_metal_server_disks = list_bare_metal_server_disks(
            createGen2Service, store['created_bare_metal_server_id'])
        bare_metal_server_disk = bare_metal_server_disks.get_result()['disks'][0]
        store['bare_metal_server_disk_id'] = bare_metal_server_disk['id']
        assert bare_metal_server_disks.status_code == 200
        assert bare_metal_server_disks.get_result() is not None

    def test_get_bare_metal_server_disk(self, createGen2Service):
        bare_metal_server_disk = get_bare_metal_server_disk(
            createGen2Service, store['created_bare_metal_server_id'], store['bare_metal_server_disk_id'])
        assert bare_metal_server_disk.status_code == 200
        assert bare_metal_server_disk.get_result() is not None

    def test_update_bare_metal_server_disk(self, createGen2Service):
        bare_metal_server_disk = update_bare_metal_server_disk(
            createGen2Service, store['created_bare_metal_server_id'], store['bare_metal_server_disk_id'],
            'my-bare-metal-server-disk-update'
        )
        assert bare_metal_server_disk.status_code == 200
        assert bare_metal_server_disk.get_result() is not None

    # create nic
    def test_create_bare_metal_server_network_interface(self, createGen2Service):
        nic = create_bare_metal_server_network_interface(
            createGen2Service, store['created_bare_metal_server_id'],
            [4, 4049], store['created_subnet'], 'pci', 'my-bms-nic', False, True)
        assertCreateResponse(nic)
        store['bare_metal_server_created_nic'] = nic.get_result()['id']

    def test_list_bare_metal_server_network_interfaces(self, createGen2Service):
        bare_metal_server_nics = list_bare_metal_server_network_interfaces(
            createGen2Service, store['created_bare_metal_server_id'])
        assertListResponse(bare_metal_server_nics, 'network_interfaces')
        store['bms_nic_id'] = bare_metal_server_nics.get_result()[
            'network_interfaces'][0]['id']

    def test_get_bare_metal_server_network_interface(self, createGen2Service):
        bare_metal_server_nic = get_bare_metal_server_network_interface(
            createGen2Service, store['created_bare_metal_server_id'], store['bms_nic_id'])
        assertGetPatchResponse(bare_metal_server_nic)

    # update nic
    def test_update_bare_metal_server_network_interface(self, createGen2Service):
        nic = update_bare_metal_server_network_interface(
            createGen2Service, store['created_bare_metal_server_id'], store['bare_metal_server_created_nic'],
            'my-bare-metal-server-network-interface-update', True, False)
        assertGetPatchResponse(nic)

    def test_create_bare_metal_server_nic_fip(self, createGen2Service):
        fip = add_bare_metal_server_network_interface_floating_ip(
            createGen2Service, store['created_bare_metal_server_id'], store['bms_nic_id'], store['created_fip_id'])
        assertCreateResponse(fip)
        store['created_bms_nic_fip'] = fip.get_result()['id']

    def test_get_bare_metal_server_nic_fips(self, createGen2Service):
        fips = list_bare_metal_server_network_interface_floating_ips(
            createGen2Service, store['created_bare_metal_server_id'], store['bms_nic_id'])
        assertListResponse(fips, 'floating_ips')

    def test_get_bare_metal_server_nic_fip(self, createGen2Service):
        fips = get_bare_metal_server_network_interface_floating_ip(
            createGen2Service, store['created_bare_metal_server_id'], store['bms_nic_id'], store['created_fip_id'])
        assertGetPatchResponse(fips)

    def test_list_bare_metal_server_network_interface_ips(self, createGen2Service):
        pytest.skip("no env")
        ips = list_bare_metal_server_network_interface_ips(
            createGen2Service, store['created_bare_metal_server_id'], store['bms_nic_id'])
        assertListResponse(ips, 'ips')

    def test_get_bare_metal_server_network_interface_ip(self, createGen2Service):
        pytest.skip("no env")
        ips = get_bare_metal_server_network_interface_ip(
            createGen2Service, store['created_bare_metal_server_id'], store['bms_nic_id'], store['created_subnet_reserved_ip'])
        assertGetPatchResponse(ips)
    
    def test_delete_bare_metal_server_nic_fip(self, createGen2Service):
        fips = remove_bare_metal_server_network_interface_floating_ip(
            createGen2Service, store['created_bare_metal_server_id'], store['bms_nic_id'], store['created_fip_id'])
        assertDeleteResponse(fips)

    def test_delete_bare_metal_server_network_interface(self, createGen2Service):
        nics = delete_bare_metal_server_network_interface(
            createGen2Service, store['created_bare_metal_server_id'], store['bms_nic_id'])
        assertDeleteResponse(nics)

    def test_create_bare_metal_server_restart(self, createGen2Service):
        bare_metal_server_restart = create_bare_metal_server_restart(
            createGen2Service, store['created_bare_metal_server_id'])
        assert bare_metal_server_restart.status_code == 204

    def test_create_bare_metal_server_stop(self, createGen2Service):
        bare_metal_server_stop = create_bare_metal_server_stop(
            createGen2Service, store['created_bare_metal_server_id'], 'hard')
        assert bare_metal_server_stop.status_code == 204

    def test_create_bare_metal_server_start(self, createGen2Service):
        bare_metal_server_start = create_bare_metal_server_start(
            createGen2Service, store['created_bare_metal_server_id'])
        assert bare_metal_server_start.status_code == 204

    def test_delete_bare_metal_server(self, createGen2Service):
        bare_metal_server_stop = create_bare_metal_server_stop(
            createGen2Service, store['created_bare_metal_server_id'], 'hard')
        assert bare_metal_server_stop.status_code == 204
        bms = delete_bare_metal_server(createGen2Service, store['created_bare_metal_server_id'])
        assertDeleteResponse(bms)

class TestInstances():
    def test_list_instances(self, createGen2Service):
        instances = list_instances(createGen2Service)
        assertListResponse(instances, 'instances')
        instance = instances.get_result()['instances'][0]
        store['instance_id'] = instance['id']
        store['network_interface_id'] = instance['primary_network_interface']['id']

    def test_list_instance_profiles(self, createGen2Service):
        profiles = list_instance_profiles(createGen2Service)
        assertListResponse(profiles, 'profiles')
        store['instance_profile'] = profiles.get_result()[
            'profiles'][0]['name']

    def test_get_instance_profile(self, createGen2Service):
        prof = get_instance_profile(
            createGen2Service, store['instance_profile'])
        assert prof.status_code == 200
        assert prof.get_result() is not None

    def test_create_instance(self, createGen2Service):
        ins = create_instance(createGen2Service, store['created_vpc'], store['instance_profile'],
                              store['zone'], store['image_id'], store['created_subnet'])
        assertCreateResponse(ins)
        store['created_instance_id'] = ins.get_result()['id']
        print('created_instance_id -' + store['created_instance_id'])

    def test_get_instance(self, createGen2Service):
        instance = get_instance(
            createGen2Service, store['created_instance_id'])
        assertGetPatchResponse(instance)

    def test_update_instance(self, createGen2Service):
        instance = update_instance(
            createGen2Service, store['created_instance_id'])
        assertGetPatchResponse(instance)

    def test_create_instance_action(self, createGen2Service):
        instance = create_instance_action(
            createGen2Service, store['created_instance_id'])
        assert instance.status_code == 201
        assert instance.get_result()['id'] is not None

    def test_get_instance_initialization(self, createGen2Service):
        instance = get_instance_initialization(
            createGen2Service, store['created_instance_id'])
        assert instance.status_code == 200
        assert instance.get_result() is not None

    def test_list_instance_network_interfaces(self, createGen2Service):
        instance_nics = list_instance_network_interfaces(
            createGen2Service, store['created_instance_id'])
        assertListResponse(instance_nics, 'network_interfaces')
        store['nic_id'] = instance_nics.get_result()[
            'network_interfaces'][0]['id']
    # create nic

    def test_create_instance_network_interface(self, createGen2Service):
        nic = create_instance_network_interface(
            createGen2Service, store['created_instance_id'], store['created_subnet'])
        assertCreateResponse(nic)
        store['created_nic'] = nic.get_result()['id']
    # update

    def test_update_instance_network_interface(self, createGen2Service):
        nic = update_instance_network_interface(
            createGen2Service, store['created_instance_id'], store['created_nic'])
        assertGetPatchResponse(nic)

    def test_get_instance_network_interface(self, createGen2Service):
        instance_nic = get_instance_network_interface(
            createGen2Service, store['created_instance_id'], store['nic_id'])
        assertGetPatchResponse(instance_nic)

    def test_create_instance_nic_fip(self, createGen2Service):
        fip = add_instance_network_interface_floating_ip(
            createGen2Service, store['created_instance_id'], store['nic_id'], store['created_fip_id'])
        assertCreateResponse(fip)
        store['created_nic_fip'] = fip.get_result()['id']

    def test_get_instance_nic_fips(self, createGen2Service):
        fips = list_instance_network_interface_floating_ips(
            createGen2Service, store['created_instance_id'], store['nic_id'])
        assertListResponse(fips, 'floating_ips')

    def test_get_instance_nic_fip(self, createGen2Service):
        fips = get_instance_network_interface_floating_ip(
            createGen2Service, store['created_instance_id'], store['nic_id'], store['created_fip_id'])
        assertGetPatchResponse(fips)

    def test_delete_instance_nic_fip(self, createGen2Service):
        fips = remove_instance_network_interface_floating_ip(
            createGen2Service, store['created_instance_id'], store['nic_id'], store['created_fip_id'])
        assertDeleteResponse(fips)

    def test_list_instance_network_interface_ips(self, createGen2Service):
        ips = list_instance_network_interface_ips(
            createGen2Service, store['created_instance_id'], store['nic_id'])
        assertListResponse(ips, 'ips')

    def test_get_instance_network_interface_ip(self, createGen2Service):
        fips = get_instance_network_interface_ip(
            createGen2Service, store['created_instance_id'], store['nic_id'], store['created_subnet_reserved_ip'])
        assertGetPatchResponse(fips)

    def test_delete_subnet_reserved_ip(self, createGen2Service):
        vpc = delete_subnet_reserved_ip(
            createGen2Service, store['created_subnet'], store['created_subnet_reserved_ip'])
        assertDeleteResponse(vpc)

    def test_delete_instance_network_interface(self, createGen2Service):
        nics = delete_instance_network_interface(
            createGen2Service, store['created_instance_id'], store['created_nic'])
        assertDeleteResponse(nics)

    def test_create_instance_vol_attachment(self, createGen2Service):
        vol_attach = create_instance_volume_attachment(
            createGen2Service, store['created_instance_id'], store['created_vol'])
        assertCreateResponse(vol_attach)
        store['created_vol_atchmt'] = vol_attach.get_result()['id']

    def test_list_instance_vol_attachment(self, createGen2Service):
        instance_vol_attachments = list_instance_volume_attachments(
            createGen2Service, store['created_instance_id'])
        assertListResponse(instance_vol_attachments, 'volume_attachments')

    def test_get_instance_vol_attachment(self, createGen2Service):
        vol_attach = get_instance_volume_attachment(
            createGen2Service, store['created_instance_id'], store['created_vol_atchmt'])
        assertGetPatchResponse(vol_attach)

    def test_update_instance_vol_attachment(self, createGen2Service):
        vol_attach = update_instance_volume_attachment(
            createGen2Service, store['created_instance_id'], store['created_vol_atchmt'])
        assertGetPatchResponse(vol_attach)

    def test_delete_instance_vol_attachment(self, createGen2Service):
        vol_attach = delete_instance_volume_attachment(
            createGen2Service, store['created_instance_id'], store['created_vol_atchmt'])
        assertDeleteResponse(vol_attach)

    def test_delete_instance(self, createGen2Service):
        ins = delete_instance(createGen2Service, store['created_instance_id'])
        assertDeleteResponse(ins)


class TestSecurityGroups():
    def test_create_sg(self, createGen2Service):
        sg = create_security_group(createGen2Service, store['created_vpc'])
        assertCreateResponse(sg)
        store['created_sg_id'] = sg.get_result()['id']

    def test_list_sgs(self, createGen2Service):
        sgs = list_security_groups(createGen2Service)
        assertListResponse(sgs, 'security_groups')

    def test_get_sg(self, createGen2Service):
        sg = get_security_group(createGen2Service, store['created_sg_id'])
        assertGetPatchResponse(sg)

    def test_create_sg_rule(self, createGen2Service):
        sg_rule = create_security_group_rule(
            createGen2Service, store['created_sg_id'])
        assertCreateResponse(sg_rule)
        store['created_sg_rule_id'] = sg_rule.get_result()['id']

    def test_list_sg_rules(self, createGen2Service):
        sg_rules = list_security_group_rules(
            createGen2Service, store['created_sg_id'])
        assertListResponse(sg_rules, 'rules')

    def test_get_sg_rule(self, createGen2Service):
        sg_rule = get_security_group_rule(
            createGen2Service, store['created_sg_id'], store['created_sg_rule_id'])
        assertGetPatchResponse(sg_rule)

    def test_update_sg_rule(self, createGen2Service):
        sg_rule = update_security_group_rule(
            createGen2Service, store['created_sg_id'], store['created_sg_rule_id'])
        assertGetPatchResponse(sg_rule)

    def test_delete_sg_rule(self, createGen2Service):
        sg_rule = delete_security_group_rule(
            createGen2Service, store['created_sg_id'], store['created_sg_rule_id'])
        assertDeleteResponse(sg_rule)

    def test_update_sg(self, createGen2Service):
        sg = update_security_group(createGen2Service, store['created_sg_id'])
        assertGetPatchResponse(sg)

    def test_delete_sg(self, createGen2Service):
        sg = delete_security_group(createGen2Service, store['created_sg_id'])
        assertDeleteResponse(sg)


class TestVPCDefaultSecurityGroup():
    def test_get_vpc_default_sg(self, createGen2Service):
        vpc_default_sg = get_vpc_default_security_group(
            createGen2Service, store['created_vpc'])
        assertGetPatchResponse(vpc_default_sg)


class TestVPCDefaultACL():
    def test_get_vpc_acl(self, createGen2Service):
        vpc_default_acl = get_vpc_default_network_acl(
            createGen2Service, store['created_vpc'])
        assertGetPatchResponse(vpc_default_acl)


class TestVPCRoutes():
    def test_create_route(self, createGen2Service):
        pytest.skip("no env")
        route = create_vpc_route(
            createGen2Service, store['created_vpc'], store['zone'])
        assertCreateResponse(route)
        store['created_route'] = route.get_result()['id']

    def test_list_routes(self, createGen2Service):
        pytest.skip("no env")
        routes = list_vpc_routes(createGen2Service, store['created_vpc'])
        assertListResponse(routes, 'routes')

    def test_get_route(self, createGen2Service):
        pytest.skip("no env")
        route = get_vpc_route(
            createGen2Service, store['created_vpc'], store['created_route'])
        assertGetPatchResponse(route)

    def test_update_route(self, createGen2Service):
        pytest.skip("no env")
        route = update_vpc_route(
            createGen2Service, store['created_vpc'], store['created_route'])
        assertGetPatchResponse(route)

    def test_delete_route(self, createGen2Service):
        pytest.skip("no env")
        route = delete_vpc_route(
            createGen2Service, store['created_vpc'], store['created_route'])
        assertDeleteResponse(route)


class TestAddressPrefix():
    def test_create_address_prefix(self, createGen2Service):
        address_prefix = create_vpc_address_prefix(
            createGen2Service, store['created_vpc'], store['zone'])
        assertCreateResponse(address_prefix)
        store['created_address_prefix'] = address_prefix.get_result()['id']

    def test_list_address_prefixes(self, createGen2Service):
        address_prefixs = list_vpc_address_prefixes(
            createGen2Service, store['created_vpc'])
        assertListResponse(address_prefixs, 'address_prefixes')

    def test_get_address_prefix(self, createGen2Service):
        address_prefix = get_vpc_address_prefix(
            createGen2Service, store['created_vpc'], store['created_address_prefix'])
        assertGetPatchResponse(address_prefix)

    def test_update_address_prefix(self, createGen2Service):
        address_prefix = update_vpc_address_prefix(
            createGen2Service, store['created_vpc'], store['created_address_prefix'])
        assertGetPatchResponse(address_prefix)

    def test_delete_address_prefix(self, createGen2Service):
        address_prefix = delete_vpc_address_prefix(
            createGen2Service, store['created_vpc'], store['created_address_prefix'])
        assertDeleteResponse(address_prefix)


class TestVPNGateways():
    def test_create_ike_policy(self, createGen2Service):
        ike_policy = create_ike_policy(createGen2Service)
        assertCreateResponse(ike_policy)
        store['created_ike_policy_id'] = ike_policy.get_result()['id']

    def test_list_ike_policies(self, createGen2Service):
        ike_policies = list_ike_policies(createGen2Service)
        assertListResponse(ike_policies, 'ike_policies')

    def test_get_ike_policy(self, createGen2Service):
        ike_policy = get_ike_policy(
            createGen2Service, store['created_ike_policy_id'])
        assertGetPatchResponse(ike_policy)

    def test_update_ike_policy(self, createGen2Service):
        ike_policy = update_ike_policy(
            createGen2Service, store['created_ike_policy_id'])
        assertGetPatchResponse(ike_policy)

    def test_list_ike_policy_connections(self, createGen2Service):
        ike_policies_conn = list_ike_policy_connections(
            createGen2Service, store['created_ike_policy_id'])
        assertListResponse(ike_policies_conn, 'connections')

    def test_create_ipsec_policy(self, createGen2Service):
        ipsec_policy = create_ipsec_policy(createGen2Service)
        assertCreateResponse(ipsec_policy)
        store['created_ipsec_policy_id'] = ipsec_policy.get_result()['id']

    def test_list_ike_policies(self, createGen2Service):
        ipsec_policies = list_ipsec_policies(createGen2Service)
        assertListResponse(ipsec_policies, 'ipsec_policies')

    def test_get_ipsec_policy(self, createGen2Service):
        ipsec_policy = get_ipsec_policy(
            createGen2Service, store['created_ipsec_policy_id'])
        assertGetPatchResponse(ipsec_policy)

    def test_update_ipsec_policy(self, createGen2Service):
        ipsec_policy = update_ipsec_policy(
            createGen2Service, store['created_ipsec_policy_id'])
        assertGetPatchResponse(ipsec_policy)

    def test_list_ipsec_policy_connections(self, createGen2Service):
        ipsec_policies_conn = list_ipsec_policy_connections(
            createGen2Service, store['created_ipsec_policy_id'])
        assertListResponse(ipsec_policies_conn, 'connections')
    # vpn_gateways

    def test_create_vpn_gateway(self, createGen2Service):
        vpn_gateway = create_vpn_gateway(
            createGen2Service, store['created_subnet'])
        assertCreateResponse(vpn_gateway)
        store['created_vpn_gateway_id'] = vpn_gateway.get_result()['id']

    def test_list_vpn_gateways(self, createGen2Service):
        ipsec_policies = list_vpn_gateways(createGen2Service)
        assertListResponse(ipsec_policies, 'vpn_gateways')

    def test_get_vpn_gateway(self, createGen2Service):
        vpn_gateway = get_vpn_gateway(
            createGen2Service, store['created_vpn_gateway_id'])
        assertGetPatchResponse(vpn_gateway)

    def test_update_vpn_gateway(self, createGen2Service):
        vpn_gateway = update_vpn_gateway(
            createGen2Service, store['created_vpn_gateway_id'])
        assertGetPatchResponse(vpn_gateway)
    # vpn_gateways_connections

    def test_create_vpn_gateway_connections(self, createGen2Service):
        vpn_gateway_connection = create_vpn_gateway_connection(
            createGen2Service, store['created_vpn_gateway_id'])
        assertCreateResponse(vpn_gateway_connection)
        store['created_vpn_gateway_connection_id'] = vpn_gateway_connection.get_result()[
            'id']

    def test_list_vpn_gateway_connections(self, createGen2Service):
        vpn_gateway_connections = list_vpn_gateway_connections(
            createGen2Service, store['created_vpn_gateway_id'])
        assertListResponse(vpn_gateway_connections, 'connections')

    def test_get_vpn_gateway_connection(self, createGen2Service):
        vpn_gateway_connection = get_vpn_gateway_connection(
            createGen2Service, store['created_vpn_gateway_id'], store['created_vpn_gateway_connection_id'])
        assertGetPatchResponse(vpn_gateway_connection)

    def test_update_vpn_gateway_connection(self, createGen2Service):
        vpn_gateway_connection = update_vpn_gateway_connection(
            createGen2Service, store['created_vpn_gateway_id'], store['created_vpn_gateway_connection_id'])
        assertGetPatchResponse(vpn_gateway_connection)

    # local_cidrs
    def test_create_vpn_gateway_connection_local_cidrs(self, createGen2Service):
        local_cidr = add_vpn_gateway_connection_local_cidr(
            createGen2Service, store['created_vpn_gateway_id'], store['created_vpn_gateway_connection_id'], "192.132.10.0", "28")
        assert local_cidr.status_code == 204

    def test_list_vpn_gateway_connection_local_cidrs(self, createGen2Service):
        local_cidr = list_vpn_gateway_connection_local_cidrs(
            createGen2Service, store['created_vpn_gateway_id'], store['created_vpn_gateway_connection_id'])
        assert local_cidr.status_code == 200

    def test_check_vpn_gateway_connection_local_cidr(self, createGen2Service):
        local_cidr = check_vpn_gateway_connection_local_cidr(
            createGen2Service, store['created_vpn_gateway_id'], store['created_vpn_gateway_connection_id'], "192.132.10.0", "28")
        assert local_cidr.status_code == 204

    def test_remove_vpn_gateway_connection_local_cidr(self, createGen2Service):
        local_cidr = remove_vpn_gateway_connection_local_cidr(
            createGen2Service, store['created_vpn_gateway_id'], store['created_vpn_gateway_connection_id'], "192.132.10.0", "28")
        assert local_cidr.status_code == 204
    # peer_cidrs

    def test_create_vpn_gateway_connection_peer_cidrs(self, createGen2Service):
        peer_cidr = add_vpn_gateway_connection_peer_cidr(
            createGen2Service, store['created_vpn_gateway_id'], store['created_vpn_gateway_connection_id'], "202.138.10.0", "28")
        assert peer_cidr.status_code == 204

    def test_list_vpn_gateway_connection_peer_cidrs(self, createGen2Service):
        peer_cidr = list_vpn_gateway_connection_peer_cidrs(
            createGen2Service, store['created_vpn_gateway_id'], store['created_vpn_gateway_connection_id'])
        assert peer_cidr.status_code == 200

    def test_check_vpn_gateway_connection_peer_cidr(self, createGen2Service):
        peer_cidr = check_vpn_gateway_connection_peer_cidr(
            createGen2Service, store['created_vpn_gateway_id'], store['created_vpn_gateway_connection_id'], "202.138.10.0", "28")
        assert peer_cidr.status_code == 204

    def test_remove_vpn_gateway_connection_peer_cidr(self, createGen2Service):
        peer_cidr = remove_vpn_gateway_connection_peer_cidr(
            createGen2Service, store['created_vpn_gateway_id'], store['created_vpn_gateway_connection_id'], "202.138.10.0", "28")
        assert peer_cidr.status_code == 204


class TestLoadBalancer():
    def test_list_load_balancer_profiles(self, createGen2Service):
        profiles = list_load_balancer_profiles(createGen2Service)
        assertListResponse(profiles, 'profiles')

    def test_get_load_balancer_profile(self, createGen2Service):
        pytest.skip("no env")
        profile = get_load_balancer_profile(createGen2Service)
        assertGetPatchResponse(profile)

    def test_list_load_balancer(self, createGen2Service):
        load_balancers = list_load_balancers(createGen2Service)
        assertListResponse(load_balancers, 'load_balancers')

    def test_create_load_balancer(self, createGen2Service):
        load_balancer = create_load_balancer(
            createGen2Service, store['created_subnet'])
        assertCreateResponse(load_balancer)
        store['created_load_balancer'] = load_balancer.get_result()['id']
        print('created_load_balancer: ' + store['created_load_balancer'])

    def test_get_load_balancer(self, createGen2Service):
        load_balancer = get_load_balancer(
            createGen2Service, store['created_load_balancer'])
        assertGetPatchResponse(load_balancer)

    def test_update_load_balancer(self, createGen2Service):
        load_balancer = update_load_balancer(
            createGen2Service, store['created_load_balancer'])
        assertGetPatchResponse(load_balancer)

    def test_get_load_balancer_statistics(self, createGen2Service):
        load_balancers = get_load_balancer_statistics(
            createGen2Service, store['created_load_balancer'])
        assert load_balancers.status_code == 200
    # listeners

    def test_list_load_balancer_listeners(self, createGen2Service):
        listeners = list_load_balancer_listeners(
            createGen2Service, store['created_load_balancer'])
        assertListResponse(listeners, 'listeners')

    def test_create_load_balancer_listener(self, createGen2Service):
        listener = create_load_balancer_listener(
            createGen2Service, store['created_load_balancer'])
        assertCreateResponse(listener)
        store['created_listener'] = listener.get_result()['id']

    def test_get_load_balancer_listener(self, createGen2Service):
        listener = get_load_balancer_listener(
            createGen2Service, store['created_load_balancer'], store['created_listener'])
        assertGetPatchResponse(listener)

    def test_update_load_balancer_listener(self, createGen2Service):
        listener = update_load_balancer_listener(
            createGen2Service, store['created_load_balancer'], store['created_listener'])
        assertGetPatchResponse(listener)

    # listener policies
    def test_list_listener_policies(self, createGen2Service):
        policies = list_load_balancer_listener_policies(
            createGen2Service, store['created_load_balancer'], store['created_listener'])
        assertListResponse(policies, 'policies')

    def test_create_listener_policy(self, createGen2Service):
        policy = create_load_balancer_listener_policy(
            createGen2Service, store['created_load_balancer'], store['created_listener'])
        assertCreateResponse(policy)
        store['created_listener_policy'] = policy.get_result()['id']
        print('created_listener_policy: ' + store['created_listener_policy'])

    def test_get_listener_policy(self, createGen2Service):
        policy = get_load_balancer_listener_policy(
            createGen2Service, store['created_load_balancer'], store['created_listener'], store['created_listener_policy'])
        assertGetPatchResponse(policy)

    def test_update_listener_policy(self, createGen2Service):
        policy = update_load_balancer_listener_policy(
            createGen2Service, store['created_load_balancer'], store['created_listener'], store['created_listener_policy'])
        assertGetPatchResponse(policy)

    # listener policy rules
    def test_list_listener_policies_rules(self, createGen2Service):
        rules = list_load_balancer_listener_policy_rules(
            createGen2Service, store['created_load_balancer'], store['created_listener'], store['created_listener_policy'])
        assertListResponse(rules, 'rules')

    def test_create_listener_policy_rule(self, createGen2Service):
        rule = create_load_balancer_listener_policy_rule(
            createGen2Service, store['created_load_balancer'], store['created_listener'], store['created_listener_policy'])
        assert rule.status_code == 201
        res = rule.get_result()
        assert res['id'] is not None
        store['created_listener_policy_rule'] = rule.get_result()['id']

    def test_get_listener_policy_rule(self, createGen2Service):
        rule = get_load_balancer_listener_policy_rule(
            createGen2Service, store['created_load_balancer'], store['created_listener'], store['created_listener_policy'],  store['created_listener_policy_rule'])
        assert rule.status_code == 200
        res = rule.get_result()
        assert res['id'] is not None

    def test_update_listener_policy_rule(self, createGen2Service):
        rule = update_load_balancer_listener_policy_rule(
            createGen2Service, store['created_load_balancer'], store['created_listener'], store['created_listener_policy'], store['created_listener_policy_rule'])
        assert rule.status_code == 200
        res = rule.get_result()
        assert res['id'] is not None

    def test_create_pool(self, createGen2Service):
        pool = create_load_balancer_pool(
            createGen2Service, store['created_load_balancer'])
        assertCreateResponse(pool)
        store['created_lb_pool'] = pool.get_result()['id']

    def test_list_lb_pools(self, createGen2Service):
        pools = list_load_balancer_pools(
            createGen2Service, store['created_load_balancer'])
        assertListResponse(pools, 'pools')

    def test_get_pool(self, createGen2Service):
        pool = get_load_balancer_pool(
            createGen2Service, store['created_load_balancer'], store['created_lb_pool'])
        assertGetPatchResponse(pool)

    def test_update_pool(self, createGen2Service):
        pool = update_load_balancer_pool(
            createGen2Service, store['created_load_balancer'], store['created_lb_pool'])
        assertGetPatchResponse(pool)

    def test_put_pool_member(self, createGen2Service):
        member = replace_load_balancer_pool_members(
            createGen2Service, store['created_load_balancer'], store['created_lb_pool'])
        assert member.status_code == 202

    def test_create_pool_member(self, createGen2Service):
        member = create_load_balancer_pool_member(
            createGen2Service, store['created_load_balancer'], store['created_lb_pool'])
        assert member.status_code == 201
        res = member.get_result()
        assert res['id'] is not None
        store['created_lb_pool_member'] = res['id']

    def test_list_lb_pool_member(self, createGen2Service):
        members = list_load_balancer_pool_members(
            createGen2Service, store['created_load_balancer'], store['created_lb_pool'])
        assertListResponse(members, 'members')

    def test_get_pool_member(self, createGen2Service):
        member = get_load_balancer_pool_member(
            createGen2Service, store['created_load_balancer'], store['created_lb_pool'], store['created_lb_pool_member'])
        assert member.status_code == 200
        assert member.get_result()['id'] is not None

    def test_update_pool_member(self, createGen2Service):
        member = update_load_balancer_pool_member(
            createGen2Service, store['created_load_balancer'], store['created_lb_pool'], store['created_lb_pool_member'])
        assert member.status_code == 200
        assert member.get_result()['id'] is not None

    #  delete listener policy rule
    def test_delete_listener_policy_rule(self, createGen2Service):
        rule = delete_load_balancer_listener_policy_rule(
            createGen2Service, store['created_load_balancer'], store['created_listener'], store['created_listener_policy'], store['created_listener_policy_rule'])
        assertDeleteResponse(rule)

    #  delete listener policy
    def test_delete_listener_policy(self, createGen2Service):
        policy = delete_load_balancer_listener_policy(
            createGen2Service, store['created_load_balancer'], store['created_listener'], store['created_listener_policy'])
        assertDeleteResponse(policy)

    # delete listener
    def test_delete_listener(self, createGen2Service):
        listener = delete_load_balancer_listener(
            createGen2Service, store['created_load_balancer'], store['created_listener'])
        assertDeleteResponse(listener)

    #  delete pool member
    def test_delete_pool_member(self, createGen2Service):
        pool = delete_load_balancer_pool_member(
            createGen2Service, store['created_load_balancer'], store['created_lb_pool'], store['created_lb_pool_member'])
        assertDeleteResponse(pool)

    #  delete pool
    def test_delete_pool(self, createGen2Service):
        pool = delete_load_balancer_pool(
            createGen2Service, store['created_load_balancer'], store['created_lb_pool'])
        assertDeleteResponse(pool)

    # delete load balancer
    def test_delete_load_balancer(self, createGen2Service):
        load_balancer = delete_load_balancer(
            createGen2Service, store['created_load_balancer'])
        assertDeleteResponse(load_balancer)


class TestVPCFlowLogs():
    def test_create_flow_log_collector(self, createGen2Service):
        fl = create_flow_log_collector(createGen2Service, store['created_vpc'])
        assertCreateResponse(fl)
        store['created_fl'] = fl.get_result()['id']

    def test_list_flow_log_collectors(self, createGen2Service):
        fls = list_flow_log_collectors(createGen2Service)
        assertListResponse(fls, 'flow_log_collectors')

    def test_get_flow_log_collector(self, createGen2Service):
        fl = get_flow_log_collector(createGen2Service, store['created_fl'])
        assertGetPatchResponse(fl)

    def test_update_flow_log_collector(self, createGen2Service):
        fl = update_flow_log_collector(createGen2Service, store['created_fl'])
        assertGetPatchResponse(fl)

    def test_delete_flow_log_collector(self, createGen2Service):
        fl = delete_flow_log_collector(createGen2Service, store['created_fl'])
        assertDeleteResponse(fl)


class TestVPCInstanceTemplates():
    def test_create_instance_template(self, createGen2Service):
        it = create_instance_template(
            createGen2Service, store['created_vpc'], store['instance_profile'], store['zone'], store['image_id'], store['created_subnet'])
        assertCreateResponse(it)
        store['created_it'] = it.get_result()['id']

    def test_list_instance_templates(self, createGen2Service):
        its = list_instance_templates(createGen2Service)
        assertListResponse(its, 'templates')

    def test_get_instance_template(self, createGen2Service):
        it = get_instance_template(createGen2Service, store['created_it'])
        assertGetPatchResponse(it)

    def test_update_instance_template(self, createGen2Service):
        it = update_instance_template(createGen2Service, store['created_it'])
        assertGetPatchResponse(it)


class TestVPCInstanceGroups():
    def test_create_instance_groups(self, createGen2Service):
        ig = create_instance_group(
            createGen2Service, store['created_it'], store['created_subnet'])
        assertCreateResponse(ig)
        store['created_ig'] = ig.get_result()['id']

    def test_list_instance_groups(self, createGen2Service):
        igs = list_instance_groups(createGen2Service)
        assertListResponse(igs, 'instance_groups')

    def test_get_instance_group(self, createGen2Service):
        ig = get_instance_group(createGen2Service, store['created_ig'])
        assertGetPatchResponse(ig)

    def test_update_instance_group(self, createGen2Service):
        ig = update_instance_group(createGen2Service, store['created_ig'])
        assertGetPatchResponse(ig)

    def test_create_instance_group_manager(self, createGen2Service):
        igm = create_instance_group_manager(
            createGen2Service, store['created_ig'])
        assertCreateResponse(igm)
        store['created_igm'] = igm.get_result()['id']

    def test_list_instance_group_managers(self, createGen2Service):
        igm = list_instance_group_managers(
            createGen2Service, store['created_ig'])
        assertListResponse(igm, 'managers')

    def test_get_instance_group_manager(self, createGen2Service):
        igm = get_instance_group_manager(
            createGen2Service, store['created_ig'], store['created_igm'])
        assertGetPatchResponse(igm)

    def test_update_instance_group_manager(self, createGen2Service):
        igm = update_instance_group_manager(
            createGen2Service, store['created_ig'], store['created_igm'])
        assertGetPatchResponse(igm)

    def test_create_instance_group_manager_policy(self, createGen2Service):
        igmp = create_instance_group_manager_policy(
            createGen2Service, store['created_ig'], store['created_igm'])
        assertCreateResponse(igmp)
        store['created_igmp'] = igmp.get_result()['id']

    def test_list_instance_group_manager_policies(self, createGen2Service):
        igmps = list_instance_group_manager_policies(
            createGen2Service, store['created_ig'], store['created_igm'])
        assertListResponse(igmps, 'policies')

    def test_get_instance_group_manager_policy(self, createGen2Service):
        igmp = get_instance_group_manager_policy(
            createGen2Service, store['created_ig'], store['created_igm'], store['created_igmp'])
        assertGetPatchResponse(igmp)

    def test_update_instance_group_manager_policy(self, createGen2Service):
        igmp = update_instance_group_manager_policy(
            createGen2Service, store['created_ig'], store['created_igm'], store['created_igmp'])
        assertGetPatchResponse(igmp)

    def test_list_instance_group_memberships(self, createGen2Service):
        igm = list_instance_group_memberships(
            createGen2Service, store['created_ig'])
        assertListResponse(igm, 'memberships')
        store['created_mbr'] = igm.get_result()['memberships'][0]['id']

    def test_get_instance_group_membership(self, createGen2Service):
        igm = get_instance_group_membership(
            createGen2Service, store['created_ig'], store['created_mbr'])
        assert igm.status_code == 200

    def test_update_instance_group_membership(self, createGen2Service):
        igm = update_instance_group_membership(
            createGen2Service, store['created_ig'], store['created_mbr'])
        response = igm.get_result()
        assert igm.status_code == 200
        assert response['id'] is not None

    def test_delete_instance_group_membership(self, createGen2Service):
        igm = delete_instance_group_membership(
            createGen2Service, store['created_ig'], store['created_mbr'])
        assertDeleteResponse(igm)

    def test_delete_instance_group_memberships(self, createGen2Service):
        igm = delete_instance_group_memberships(
            createGen2Service, store['created_ig'])
        assertDeleteResponse(igm)


class TestDedicatedHost():
    def test_create_dedicated_host_group(self, createGen2Service):
        dhg = create_dedicated_host_group(createGen2Service)
        assertCreateResponse(dhg)
        store['created_dhg'] = dhg.get_result()['id']

    def test_list_dedicated_host_profiles(self, createGen2Service):
        igs = list_dedicated_host_profiles(createGen2Service)
        assertListResponse(igs, 'profiles')

    def test_get_dedicated_host_profile(self, createGen2Service):
        ig = get_dedicated_host_profile(createGen2Service, 'bx2-host-152x608')
        response = ig.get_result()
        assert ig.status_code == 200

    def test_create_dedicated_host(self, createGen2Service):
        dh = create_dedicated_host(
            createGen2Service,  'bx2-host-152x608', store['created_dhg'])
        assertCreateResponse(dh)
        store['created_dh'] = dh.get_result()['id']

    def test_list_dedicated_host_groups(self, createGen2Service):
        igs = list_dedicated_host_groups(createGen2Service)
        assertListResponse(igs, 'groups')

    def test_list_dedicated_hosts(self, createGen2Service):
        igs = list_dedicated_hosts(createGen2Service)
        assertListResponse(igs, 'dedicated_hosts')

    def test_get_dedicated_host_group(self, createGen2Service):
        ig = get_dedicated_host_group(createGen2Service, store['created_dhg'])
        assertGetPatchResponse(ig)

    def test_get_dedicated_host(self, createGen2Service):
        ig = get_dedicated_host(createGen2Service, store['created_dh'])
        assertGetPatchResponse(ig)

    def test_update_dedicated_host_group(self, createGen2Service):
        ig = update_dedicated_host_group(
            createGen2Service, store['created_dhg'])
        assertGetPatchResponse(ig)

    def test_update_dedicated_host(self, createGen2Service):
        ig = update_dedicated_host(createGen2Service, store['created_dh'])
        assertGetPatchResponse(ig)

    def test_delete_dedicated_host_group(self, createGen2Service):
        igm = delete_dedicated_host_group(
            createGen2Service, store['created_dhg'])
        assertDeleteResponse(igm)

    def test_delete_dedicated_host(self, createGen2Service):
        igm = delete_dedicated_host(
            createGen2Service, store['created_dh'])
        assertDeleteResponse(igm)

class TestPlacementGroup():
    def test_create_placement_group(self, createGen2Service):
        name = 'my-placement-group'
        pg = create_placement_group(createGen2Service, name)
        assertCreateResponse(pg)
        store['created_placement_group'] = pg.get_result()['id']

    def test_list_placement_groups(self, createGen2Service):
        pgc = list_placement_groups(createGen2Service)
        assertListResponse(pgc, 'placement_groups')

    def test_get_placement_group(self, createGen2Service):
        pg = get_placement_group(createGen2Service, store['created_placement_group'])
        assert pg.status_code == 200
        assert pg.get_result() is not None

    def test_update_placement_group(self, createGen2Service):
        pg = update_placement_group(
            createGen2Service, store['created_placement_group'], 'my-placement-group1')
        assertGetPatchResponse(pg)

    def test_delete_placement_group(self, createGen2Service):
        pg = delete_placement_group(createGen2Service, store['created_placement_group'])
        assertDeleteResponse(pg)

class TestTeardown():
    def test_delete_instance_group_manager_policy(self, createGen2Service):
        igmp = delete_instance_group_manager_policy(
            createGen2Service, store['created_ig'], store['created_igm'], store['created_igmp'])
        assertDeleteResponse(igmp)

    def test_delete_instance_group_manager(self, createGen2Service):
        igm = delete_instance_group_manager(
            createGen2Service, store['created_ig'], store['created_igm'])
        assertDeleteResponse(igm)

    def test_delete_instance_group(self, createGen2Service):
        ig = delete_instance_group(createGen2Service, store['created_ig'])
        assertDeleteResponse(ig)

    def test_delete_instance_template(self, createGen2Service):
        it = delete_instance_template(createGen2Service, store['created_it'])
        assertDeleteResponse(it)

    def test_delete_ipsec_policy(self, createGen2Service):
        ipsec_policy = delete_ipsec_policy(
            createGen2Service, store['created_ipsec_policy_id'])
        assertDeleteResponse(ipsec_policy)

    def test_delete_ike_policy(self, createGen2Service):
        ike_policy = delete_ike_policy(
            createGen2Service, store['created_ike_policy_id'])
        assertDeleteResponse(ike_policy)

    def test_delete_vpn_gateway_connection(self, createGen2Service):
        vpn_gateway_connection = delete_vpn_gateway_connection(
            createGen2Service, store['created_vpn_gateway_id'], store['created_vpn_gateway_connection_id'])
        assertDeleteResponse(vpn_gateway_connection)

    def test_delete_vpn_gateway(self, createGen2Service):
        vpn_gateway = delete_vpn_gateway(
            createGen2Service, store['created_vpn_gateway_id'])
        assert vpn_gateway.status_code == 202

    def test_delete_floating_ip(self, createGen2Service):
        fip = delete_floating_ip(createGen2Service, store['created_fip_id'])
        assertDeleteResponse(fip)

    def test_delete_pgw(self, createGen2Service):
        pgw = delete_public_gateway(createGen2Service, store['created_pgw'])
        assertDeleteResponse(pgw)

    def test_delete_key(self, createGen2Service):
        key = delete_key(createGen2Service, store['created_key'])
        assertDeleteResponse(key)

    def test_delete_vol(self, createGen2Service):
        vol = delete_volume(createGen2Service, store['created_vol'])
        assertDeleteResponse(vol)

    def test_delete_subnet(self, createGen2Service):
        subnet = delete_subnet(createGen2Service, store['created_subnet'])
        assertDeleteResponse(subnet)

    def test_delete_nacl(self, createGen2Service):
        acl = delete_network_acl(createGen2Service, store['created_nacl_id'])
        assertDeleteResponse(acl)

    def test_delete_vpc(self, createGen2Service):
        vpc = delete_vpc(createGen2Service, store['created_vpc'])
        assertDeleteResponse(vpc)


# --------------------------------------------------------
#  test helpers
# --------------------------------------------------------

# --------------------------------------------------------
# list_floating_ips()
# --------------------------------------------------------


def list_floating_ips(service):
    response = service.list_floating_ips()
    return response

# --------------------------------------------------------
# create_floating_ip()
# --------------------------------------------------------


def create_floating_ip(service):

    # Construct a dict representation of a ResourceGroupIdentityById model
    resource_group_identity_model = {}
    resource_group_identity_model['id'] = 'fee82deba12e4c0fb69c3b09d1f12345'

    # Construct a dict representation of a ZoneIdentityByName model
    zone_identity_model = {}
    zone_identity_model['name'] = store['zone']

    # Construct a dict representation of a FloatingIPPrototypeFloatingIPByZone model
    floating_ip_prototype_model = {}
    floating_ip_prototype_model['name'] = generate_name("fip")
    floating_ip_prototype_model[
        'resource_group'] = resource_group_identity_model
    floating_ip_prototype_model['zone'] = zone_identity_model

    # Set up parameter values
    floating_ip_prototype = floating_ip_prototype_model

    response = service.create_floating_ip(floating_ip_prototype)
    return response
# --------------------------------------------------------
# delete_floating_ip()
# --------------------------------------------------------


def delete_floating_ip(service, id):
    response = service.delete_floating_ip(id)
    return response

# --------------------------------------------------------
# get_floating_ip()
# --------------------------------------------------------


def get_floating_ip(service, id):
    response = service.get_floating_ip(id)
    return response

# --------------------------------------------------------
# update_floating_ip()
# --------------------------------------------------------


def update_floating_ip(service, id):
    floating_ip_patch = {}
    floating_ip_patch['name'] = generate_name('fip')
    response = service.update_floating_ip(
        id,
        floating_ip_patch,
    )
    return response

# --------------------------------------------------------
# list_regions()
# --------------------------------------------------------


def list_regions(service):
    response = service.list_regions()
    return response

# --------------------------------------------------------
# get_region()
# --------------------------------------------------------


def get_region(service, name):
    response = service.get_region(name)
    return response

# --------------------------------------------------------
# list_region_zones()
# --------------------------------------------------------


def list_region_zones(service, region_name):
    response = service.list_region_zones(region_name)
    return response

# --------------------------------------------------------
# get_region_zone()
# --------------------------------------------------------


def get_region_zone(service, region_name, zone_name):
    response = service.get_region_zone(region_name, zone_name)
    return response


# --------------------------------------------------------
# Bare Metal Servers
# --------------------------------------------------------

def list_bare_metal_server_profiles(service):
    list_bare_metal_server_profiles_response = service.list_bare_metal_server_profiles()
    return list_bare_metal_server_profiles_response


def get_bare_metal_server_profile(service, profile_name):
    get_bare_metal_server_profile_response = service.get_bare_metal_server_profile(profile_name)
    return get_bare_metal_server_profile_response


def list_bare_metal_servers(service):
    list_bare_metal_servers_response = service.list_bare_metal_servers()
    return list_bare_metal_servers_response


def create_bare_metal_server(service, profile_name, subnet_id, image_id, key_id, vpc_id, zone_name, user_data,
                             bare_metal_server_name):
    bare_metal_server_profile_identity_model = {}
    bare_metal_server_profile_identity_model['name'] = profile_name

    subnet_identity_model = {}
    subnet_identity_model['id'] = subnet_id

    bare_metal_server_primary_network_interface_model = {}
    bare_metal_server_primary_network_interface_model['subnet'] = subnet_identity_model

    image_identity_model = {}
    image_identity_model['id'] = image_id

    key_identity_model = {}
    key_identity_model['id'] = key_id

    vpc_identity_model = {}
    vpc_identity_model['id'] = vpc_id

    zone_identity_model = {}
    zone_identity_model['name'] = zone_name

    bare_metal_server_initialization_model = {}
    bare_metal_server_initialization_model['image'] = image_identity_model
    bare_metal_server_initialization_model['keys'] = [key_identity_model]
    bare_metal_server_initialization_model['user_data'] = user_data

    create_bare_metal_server_response = service.create_bare_metal_server(
        initialization=bare_metal_server_initialization_model,
        primary_network_interface=bare_metal_server_primary_network_interface_model,
        profile=bare_metal_server_profile_identity_model,
        zone=zone_identity_model,
        name=bare_metal_server_name,
        vpc=vpc_identity_model,
        #enable_secure_boot=True
    )
    return create_bare_metal_server_response


def get_bare_metal_server_console(service, bare_metal_server_id):
    get_bare_metal_server_console_response = service.get_bare_metal_server_console(bare_metal_server_id)
    return get_bare_metal_server_console_response


def create_bare_metal_server_console_access_token(service, bare_metal_server_id, console_type):
    create_bare_metal_server_console_access_token_response = service.create_bare_metal_server_console_access_token(
        bare_metal_server_id,
        console_type=console_type,
        force=True
    )
    return create_bare_metal_server_console_access_token_response


def list_bare_metal_server_disks(service, bare_metal_server_id):
    list_bare_metal_server_disks_response = service.list_bare_metal_server_disks(bare_metal_server_id)
    return list_bare_metal_server_disks_response


def get_bare_metal_server_disk(service, bare_metal_server_id, id):
    get_bare_metal_server_disk_response = service.get_bare_metal_server_disk(bare_metal_server_id, id)
    return get_bare_metal_server_disk_response


def update_bare_metal_server_disk(service, bare_metal_server_id, id, disk_name):
    bare_metal_server_disk_patch_model = {}
    bare_metal_server_disk_patch_model['name'] = disk_name
    update_bare_metal_server_disk_response = service.update_bare_metal_server_disk(
        bare_metal_server_id,
        id,
        bare_metal_server_disk_patch=bare_metal_server_disk_patch_model
    )
    return update_bare_metal_server_disk_response


def list_bare_metal_server_network_interfaces(service, bare_metal_server_id):
    list_bare_metal_server_network_interfaces_response = service.list_bare_metal_server_network_interfaces(
        bare_metal_server_id
    )
    return list_bare_metal_server_network_interfaces_response


def create_bare_metal_server_network_interface(service, bare_metal_server_id, vlans, subnet_id, inetrface_type,
                                               nic_name, allow_ip_spoofing, enable_infrastructure_nat):
    allowed_vlans = vlans
    subnet_identity_model = {}
    subnet_identity_model['id'] = subnet_id
    bare_metal_server_network_interface_prototype_model = {}
    bare_metal_server_network_interface_prototype_model['interface_type'] = inetrface_type
    bare_metal_server_network_interface_prototype_model['name'] = nic_name
    bare_metal_server_network_interface_prototype_model['allowed_vlans'] = allowed_vlans
    bare_metal_server_network_interface_prototype_model['allow_ip_spoofing'] = allow_ip_spoofing
    bare_metal_server_network_interface_prototype_model['enable_infrastructure_nat'] = enable_infrastructure_nat
    bare_metal_server_network_interface_prototype_model['subnet'] = subnet_identity_model

    create_bare_metal_server_network_interface_response = service.create_bare_metal_server_network_interface(
        bare_metal_server_id,
        bare_metal_server_network_interface_prototype=bare_metal_server_network_interface_prototype_model
    )
    return create_bare_metal_server_network_interface_response


def get_bare_metal_server_network_interface(service, bare_metal_server_id, id):
    get_bare_metal_server_network_interface_response = service.get_bare_metal_server_network_interface(
        bare_metal_server_id,
        id
    )
    return get_bare_metal_server_network_interface_response


def update_bare_metal_server_network_interface(service, bare_metal_server_id, id, bms_nic_name, allow_ip_spoofing,
                                               enable_infrastructure_nat):
    bare_metal_server_network_interface_patch_model = {}
    bare_metal_server_network_interface_patch_model['name'] = bms_nic_name
    bare_metal_server_network_interface_patch_model['allow_ip_spoofing'] = allow_ip_spoofing
    bare_metal_server_network_interface_patch_model['enable_infrastructure_nat'] = enable_infrastructure_nat
    update_bare_metal_server_network_interface_response = service.update_bare_metal_server_network_interface(
        bare_metal_server_id,
        id,
        bare_metal_server_network_interface_patch=bare_metal_server_network_interface_patch_model
    )
    return update_bare_metal_server_network_interface_response


def delete_bare_metal_server_network_interface(service, bare_metal_server_id, id):
    delete_bare_metal_server_network_interface_response = service.delete_bare_metal_server_network_interface(
        bare_metal_server_id,
        id
    )
    return delete_bare_metal_server_network_interface_response


def list_bare_metal_server_network_interface_floating_ips(service, bare_metal_server_id, network_interface_id, ):
    list_bare_metal_server_network_interface_floating_ips_response = service.list_bare_metal_server_network_interface_floating_ips(
        bare_metal_server_id,
        network_interface_id
    )
    return list_bare_metal_server_network_interface_floating_ips_response


def get_bare_metal_server_network_interface_floating_ip(service, bare_metal_server_id, network_interface_id, id):
    get_bare_metal_server_network_interface_floating_ip_response = service.get_bare_metal_server_network_interface_floating_ip(
        bare_metal_server_id,
        network_interface_id,
        id
    )
    return get_bare_metal_server_network_interface_floating_ip_response


def add_bare_metal_server_network_interface_floating_ip(service, bare_metal_server_id, network_interface_id, id):
    add_bare_metal_server_network_interface_floating_ip_response = service.add_bare_metal_server_network_interface_floating_ip(
        bare_metal_server_id,
        network_interface_id,
        id
    )
    return add_bare_metal_server_network_interface_floating_ip_response

def list_bare_metal_server_network_interface_ips(service, bare_metal_server_id, network_interface_id):
    list_bare_metal_server_network_interface_floating_ip_response = service.list_bare_metal_server_network_interface_ips(
        bare_metal_server_id,
        network_interface_id
    )
    return list_bare_metal_server_network_interface_floating_ip_response


def get_bare_metal_server_network_interface_ip(service, bare_metal_server_id, network_interface_id, id):
    get_bare_metal_server_network_interface_ip_response = service.get_bare_metal_server_network_interface_ip(
        bare_metal_server_id,
        network_interface_id,
        id
    )
    return get_bare_metal_server_network_interface_ip_response


def remove_bare_metal_server_network_interface_floating_ip(service, bare_metal_server_id, network_interface_id, id):
    remove_bare_metal_server_network_interface_floating_ip_response = service.remove_bare_metal_server_network_interface_floating_ip(
        bare_metal_server_id,
        network_interface_id,
        id
    )
    return remove_bare_metal_server_network_interface_floating_ip_response


def get_bare_metal_server(service, id):
    get_bare_metal_server_response = service.get_bare_metal_server(id)
    return get_bare_metal_server_response


def update_bare_metal_server(service, id, name, enable_secure_boot):
    bare_metal_server_patch_model = {}
    bare_metal_server_patch_model['name'] = name
    bare_metal_server_patch_model['enable_secure_boot'] = enable_secure_boot

    update_bare_metal_server_response = service.update_bare_metal_server(
        id,
        bare_metal_server_patch=bare_metal_server_patch_model
    )
    return update_bare_metal_server_response


def delete_bare_metal_server(service, id):
    delete_bare_metal_server_response = service.delete_bare_metal_server(id)
    return delete_bare_metal_server_response


def get_bare_metal_server_initialization(service, id):
    get_bare_metal_server_initialization_response = service.get_bare_metal_server_initialization(id)
    return get_bare_metal_server_initialization_response


def create_bare_metal_server_restart(service, id):
    create_bare_metal_server_restart_response = service.restart_bare_metal_server(id)
    return create_bare_metal_server_restart_response


def create_bare_metal_server_start(service, id):
    create_bare_metal_server_start_response = service.start_bare_metal_server(id)
    return create_bare_metal_server_start_response


def create_bare_metal_server_stop(service, id, stopping_type):
    create_bare_metal_server_stop_response = service.stop_bare_metal_server(
        id,
        stopping_type
    )
    return create_bare_metal_server_stop_response

# --------------------------------------------------------
# list_images()
# --------------------------------------------------------


def list_images(service):
    response = service.list_images()
    return response

# --------------------------------------------------------
# create_image()
# --------------------------------------------------------


def create_image(service):

    # Construct a dict representation of a ImageFilePrototype model
    image_file_prototype_model = {}
    image_file_prototype_model[
        'href'] = 'cos://us-south/custom-image-vpc-bucket/customImage-0.vhd'

    # Construct a dict representation of a OperatingSystemIdentityByName model
    operating_system_identity_model = {}
    operating_system_identity_model['name'] = 'ubuntu-16-amd64'

    # Construct a dict representation of a ResourceGroupIdentityById model
    resource_group_identity_model = {}
    resource_group_identity_model['id'] = 'fee82deba12e4c0fb69c3b09d1f12345'

    # Construct a dict representation of a ImagePrototypeImageByFile model
    image_prototype_model = {}
    image_prototype_model['name'] = generate_name('image')
    image_prototype_model['resource_group'] = resource_group_identity_model
    image_prototype_model['file'] = image_file_prototype_model
    image_prototype_model[
        'operating_system'] = operating_system_identity_model

    # Set up parameter values
    image_prototype = image_prototype_model

    response = service.create_image(image_prototype)
    return response

# --------------------------------------------------------
# delete_image()
# --------------------------------------------------------


def delete_image(service, id):
    response = service.delete_image(id)
    return response

# --------------------------------------------------------
# get_image()
# --------------------------------------------------------


def get_image(service, id):
    response = service.get_image(id)
    return response

# --------------------------------------------------------
# update_image()
# --------------------------------------------------------


def update_image(service, id):
    image_patch = {}
    image_patch['name'] = generate_name('image')
    response = service.update_image(
        id,
        image_patch,
    )
    return response

# --------------------------------------------------------
# list_operating_systems()
# --------------------------------------------------------


def list_operating_systems(service):
    response = service.list_operating_systems()
    return response

# --------------------------------------------------------
# get_operating_system()
# --------------------------------------------------------


def get_operating_system(service, name):
    response = service.get_operating_system(name)
    return response

# --------------------------------------------------------
# list_instance_profiles()
# --------------------------------------------------------


def list_instance_profiles(service):
    response = service.list_instance_profiles()
    return response

# --------------------------------------------------------
# get_instance_profile()
# --------------------------------------------------------


def get_instance_profile(service, name):
    response = service.get_instance_profile(name)
    return response

# --------------------------------------------------------
# list_instances()
# --------------------------------------------------------


def list_instances(service):
    response = service.list_instances()
    return response

# --------------------------------------------------------
# create_instance()
# --------------------------------------------------------


def create_instance(service, vpc, profile, zone, image, subnet):

    # Construct a dict representation of a VolumeProfileIdentityByName model
    # volume_profile_identity_model = {}
    # volume_profile_identity_model['name'] = 'general-purpose'

    # # Construct a dict representation of a SecurityGroupIdentityById model
    # security_group_identity_model = {}
    # security_group_identity_model[
    #     'id'] = 'be5df5ca-12a0-494b-907e-aa6ec2bfa271'

    # Construct a dict representation of a SubnetIdentityById model
    subnet_identity_model = {}
    subnet_identity_model['id'] = subnet

    # Construct a dict representation of a VolumeAttachmentPrototypeInstanceContextVolumeVolumeIdentityVolumeIdentityById model
    # volume_attachment_prototype_instance_context_volume_model = {}
    # volume_attachment_prototype_instance_context_volume_model[
    #     'id'] = '1a6b7274-678d-4dfb-8981-c71dd9d4daa5'

    # Construct a dict representation of a VolumePrototypeInstanceByImageContext model
    # volume_prototype_instance_by_image_context_model = {}
    # volume_prototype_instance_by_image_context_model['capacity'] = 100
    # volume_prototype_instance_by_image_context_model['iops'] = 10000
    # volume_prototype_instance_by_image_context_model['name'] = 'my-volume'
    # volume_prototype_instance_by_image_context_model[
    #     'profile'] = volume_profile_identity_model

    # Construct a dict representation of a ImageIdentityById model
    image_identity_model = {}
    image_identity_model['id'] = image

    # Construct a dict representation of a InstanceProfileIdentityByName model
    instance_profile_identity_model = {}
    instance_profile_identity_model['name'] = profile

    # Construct a dict representation of a KeyIdentityById model
    # key_identity_model = {}
    # key_identity_model['id'] = 'a6b1a881-2ce8-41a3-80fc-36316a73f803'

    # Construct a dict representation of a NetworkInterfacePrototype model
    network_interface_prototype_model = {}
    # network_interface_prototype_model['name'] = 'my-network-interface'
    # network_interface_prototype_model['primary_ipv4_address'] = '10.0.0.5'
    # network_interface_prototype_model['security_groups'] = [
    #     security_group_identity_model
    # ]
    network_interface_prototype_model['subnet'] = subnet_identity_model

    # Construct a dict representation of a ResourceGroupIdentityById model
    # resource_group_identity_model = {}
    # resource_group_identity_model['id'] = 'fee82deba12e4c0fb69c3b09d1f12345'

    # Construct a dict representation of a VPCIdentityById model
    vpc_identity_model = {}
    vpc_identity_model['id'] = vpc

    # Construct a dict representation of a VolumeAttachmentPrototypeInstanceByImageContext model
    # volume_attachment_prototype_instance_by_image_context_model = {}
    # volume_attachment_prototype_instance_by_image_context_model[
    #     'delete_volume_on_instance_delete'] = True
    # volume_attachment_prototype_instance_by_image_context_model[
    #     'name'] = 'my-volume-attachment'
    # volume_attachment_prototype_instance_by_image_context_model[
    #     'volume'] = volume_prototype_instance_by_image_context_model

    # Construct a dict representation of a VolumeAttachmentPrototypeInstanceContext model
    # volume_attachment_prototype_instance_context_model = {}
    # volume_attachment_prototype_instance_context_model[
    #     'delete_volume_on_instance_delete'] = True
    # volume_attachment_prototype_instance_context_model[
    #     'name'] = 'my-volume-attachment'
    # volume_attachment_prototype_instance_context_model[
    #     'volume'] = volume_attachment_prototype_instance_context_volume_model

    # Construct a dict representation of a ZoneIdentityByName model
    zone_identity_model = {}
    zone_identity_model['name'] = zone

    # Construct a dict representation of a InstancePrototypeInstanceByImage model
    instance_prototype_model = {}
    # instance_prototype_model['keys'] = [key_identity_model]
    instance_prototype_model['name'] = generate_name('vsi')
    # instance_prototype_model['network_interfaces'] = [
    #     network_interface_prototype_model
    # ]
    instance_prototype_model['profile'] = instance_profile_identity_model
    # instance_prototype_model[
    #     'resource_group'] = resource_group_identity_model
    # instance_prototype_model['user_data'] = 'testString'
    # instance_prototype_model['volume_attachments'] = [
    #     volume_attachment_prototype_instance_context_model
    # ]
    instance_prototype_model['vpc'] = vpc_identity_model
    # instance_prototype_model[
    #     'boot_volume_attachment'] = volume_attachment_prototype_instance_by_image_context_model
    instance_prototype_model['image'] = image_identity_model
    instance_prototype_model[
        'primary_network_interface'] = network_interface_prototype_model
    instance_prototype_model['zone'] = zone_identity_model

    # Set up parameter values
    instance_prototype = instance_prototype_model

    response = service.create_instance(instance_prototype)
    return response

# --------------------------------------------------------
# delete_instance()
# --------------------------------------------------------


def delete_instance(service, id):
    response = service.delete_instance(id)
    return response

# --------------------------------------------------------
# get_instance()
# --------------------------------------------------------


def get_instance(service, id):
    response = service.get_instance(id)
    return response

# --------------------------------------------------------
# update_instance()
# --------------------------------------------------------


def update_instance(service, id):
    instance_patch = {}
    instance_patch['name'] = generate_name('instance')
    response = service.update_instance(
        id,
        instance_patch,
    )
    return response


# --------------------------------------------------------
# get_instance_initialization()
# --------------------------------------------------------
def get_instance_initialization(service, id):
    response = service.get_instance_initialization(id)
    return response

# --------------------------------------------------------
# create_instance_action()
# --------------------------------------------------------


def create_instance_action(service, instance_id):
    type = 'reboot'
    response = service.create_instance_action(
        instance_id,
        type,
    )
    return response

# --------------------------------------------------------
# list_instance_network_interfaces()
# --------------------------------------------------------


def list_instance_network_interfaces(service, instance_id):
    response = service.list_instance_network_interfaces(instance_id)
    return response


# --------------------------------------------------------
# create_instance_network_interface()
# --------------------------------------------------------
def create_instance_network_interface(service, instance_id, subnet_id):
    # Construct a dict representation of a SubnetIdentityById model
    subnet_identity_model = {}
    subnet_identity_model['id'] = subnet_id

    # Construct a dict representation of a SecurityGroupIdentityById model
    # security_group_identity_model = {}
    # security_group_identity_model[
    #     'id'] = 'be5df5ca-12a0-494b-907e-aa6ec2bfa271'

    # Set up parameter values
    subnet = subnet_identity_model
    name = generate_name('nic')
    # primary_ipv4_address = '10.0.0.5'
    # security_groups = [security_group_identity_model]

    response = service.create_instance_network_interface(
        instance_id,
        subnet,
        name=name,
        # primary_ipv4_address=primary_ipv4_address,
        # security_groups=security_groups,
    )
    return response


# --------------------------------------------------------
# delete_instance_network_interface()
# --------------------------------------------------------
def delete_instance_network_interface(service, instance_id, id):
    response = service.delete_instance_network_interface(instance_id, id)
    return response

# --------------------------------------------------------
# get_instance_network_interface()
# --------------------------------------------------------


def get_instance_network_interface(service, instance_id, id):
    response = service.get_instance_network_interface(instance_id, id)
    return response

# --------------------------------------------------------
# update_instance_network_interface()
# --------------------------------------------------------


def update_instance_network_interface(service, instance_id, id):
    network_interface_patch_model = {}
    network_interface_patch_model['name'] = generate_name('nic')
    response = service.update_instance_network_interface(
        instance_id,
        id,
        network_interface_patch=network_interface_patch_model,
    )
    return response

# --------------------------------------------------------
# list_instance_network_interface_floating_ips()
# --------------------------------------------------------


def list_instance_network_interface_floating_ips(service, instance_id, network_interface_id):
    response = service.list_instance_network_interface_floating_ips(
        instance_id, network_interface_id)
    return response

# --------------------------------------------------------
# remove_instance_network_interface_floating_ip()
# --------------------------------------------------------


def remove_instance_network_interface_floating_ip(service, instance_id, network_interface_id, id):
    response = service.remove_instance_network_interface_floating_ip(
        instance_id, network_interface_id, id)
    return response
# --------------------------------------------------------
# get_instance_network_interface_floating_ip()
# --------------------------------------------------------


def get_instance_network_interface_floating_ip(service, instance_id, network_interface_id, id):
    response = service.get_instance_network_interface_floating_ip(
        instance_id, network_interface_id, id)
    return response

# --------------------------------------------------------
# add_instance_network_interface_floating_ip()
# --------------------------------------------------------


def add_instance_network_interface_floating_ip(service, instance_id, network_interface_id, id):
    response = service.add_instance_network_interface_floating_ip(
        instance_id, network_interface_id, id)
    return response

# --------------------------------------------------------
# list_instance_network_interface_ips()
# --------------------------------------------------------


def list_instance_network_interface_ips(service, instance_id, network_interface_id):
    response = service.list_instance_network_interface_ips(
        instance_id, network_interface_id)
    return response

# --------------------------------------------------------
# get_instance_network_interface_ip()
# --------------------------------------------------------


def get_instance_network_interface_ip(service, instance_id, network_interface_id, id):
    response = service.get_instance_network_interface_ip(
        instance_id, network_interface_id, id)
    return response

# --------------------------------------------------------
# list_instance_volume_attachments()
# --------------------------------------------------------


def list_instance_volume_attachments(service, instance_id):
    response = service.list_instance_volume_attachments(instance_id)
    return response

# --------------------------------------------------------
# create_instance_volume_attachment()
# --------------------------------------------------------


def create_instance_volume_attachment(service, instance_id, vol_id):
    # Construct a dict representation of a VolumeIdentityById model
    volume_identity_model = {}
    volume_identity_model['id'] = vol_id

    volume = volume_identity_model
    delete_volume_on_instance_delete = True
    name = generate_name('vol-att')

    response = service.create_instance_volume_attachment(
        instance_id,
        volume,
        delete_volume_on_instance_delete=delete_volume_on_instance_delete,
        name=name,
    )
    return response


# --------------------------------------------------------
# delete_instance_volume_attachment()
# --------------------------------------------------------
def delete_instance_volume_attachment(service, instance_id, id):
    response = service.delete_instance_volume_attachment(instance_id, id)
    return response

# --------------------------------------------------------
# get_instance_volume_attachment()
# --------------------------------------------------------


def get_instance_volume_attachment(service, instance_id, id):
    response = service.get_instance_volume_attachment(instance_id, id)
    return response

# --------------------------------------------------------
# update_instance_volume_attachment()
# --------------------------------------------------------


def update_instance_volume_attachment(service, instance_id, id):
    volume_attachment_patch = {}
    volume_attachment_patch['delete_volume_on_instance_delete'] = True
    volume_attachment_patch['name'] = generate_name('vol-att')
    response = service.update_instance_volume_attachment(
        instance_id,
        id,
        volume_attachment_patch,
    )
    return response

# --------------------------------------------------------
# test_list_load_balancer_profiles_()
# --------------------------------------------------------


def list_load_balancer_profiles(service):
    response = service.list_load_balancer_profiles()
    return response
# --------------------------------------------------------
# test_get_load_balancer_profile_()
# --------------------------------------------------------


def get_load_balancer_profile(service):
    name = 'network-fixed'
    response = service.get_load_balancer_profile(name)
    return response
# --------------------------------------------------------
# list_load_balancers()
# --------------------------------------------------------


def list_load_balancers(service):
    response = service.list_load_balancers()
    return response

# --------------------------------------------------------
# create_load_balancer()
# --------------------------------------------------------


def create_load_balancer(service, subnet):

    # Construct a dict representation of a SubnetIdentityById model
    subnet_identity_model = {}
    subnet_identity_model['id'] = subnet

    # Construct a dict representation of a LoadBalancerPoolIdentityByName model
    # load_balancer_pool_identity_by_name_model = {}
    # load_balancer_pool_identity_by_name_model[
    #     'name'] = 'my-load-balancer-pool'

    # Construct a dict representation of a LoadBalancerListenerPrototypeLoadBalancerContext model
    # load_balancer_listener_prototype_load_balancer_context_model = {}
    # load_balancer_listener_prototype_load_balancer_context_model[
    #     'connection_limit'] = 2000
    # load_balancer_listener_prototype_load_balancer_context_model[
    #     'default_pool'] = load_balancer_pool_identity_by_name_model
    # load_balancer_listener_prototype_load_balancer_context_model[
    #     'port'] = 443
    # load_balancer_listener_prototype_load_balancer_context_model[
    #     'protocol'] = 'http'

    # Construct a dict representation of a LoadBalancerPoolMemberTargetPrototypeByAddress model
    # load_balancer_pool_member_target_prototype_model = {}
    # load_balancer_pool_member_target_prototype_model[
    #     'address'] = '192.168.3.4'

    # Construct a dict representation of a LoadBalancerPoolHealthMonitorPrototype model
    # load_balancer_pool_health_monitor_prototype_model = {}
    # load_balancer_pool_health_monitor_prototype_model['delay'] = 5
    # load_balancer_pool_health_monitor_prototype_model['max_retries'] = 2
    # load_balancer_pool_health_monitor_prototype_model['port'] = 22
    # load_balancer_pool_health_monitor_prototype_model['timeout'] = 2
    # load_balancer_pool_health_monitor_prototype_model['type'] = 'http'
    # load_balancer_pool_health_monitor_prototype_model['url_path'] = '/'

    # Construct a dict representation of a LoadBalancerPoolMemberPrototype model
    # load_balancer_pool_member_prototype_model = {}
    # load_balancer_pool_member_prototype_model['port'] = 80
    # # load_balancer_pool_member_prototype_model[
    # #     'target'] = load_balancer_pool_member_target_prototype_model
    # load_balancer_pool_member_prototype_model['weight'] = 50

    # Construct a dict representation of a LoadBalancerPoolSessionPersistencePrototype model
    # load_balancer_pool_session_persistence_prototype_model = {}
    # load_balancer_pool_session_persistence_prototype_model[
    #     'type'] = 'source_ip'

    # Construct a dict representation of a LoadBalancerPoolPrototype model
    # load_balancer_pool_prototype_model = {}
    # load_balancer_pool_prototype_model['algorithm'] = 'least_connections'
    # load_balancer_pool_prototype_model[
    #     'health_monitor'] = load_balancer_pool_health_monitor_prototype_model
    # load_balancer_pool_prototype_model['members'] = [
    #     load_balancer_pool_member_prototype_model
    # ]
    # load_balancer_pool_prototype_model['name'] = 'my-load-balancer-pool'
    # load_balancer_pool_prototype_model['protocol'] = 'http'
    # load_balancer_pool_prototype_model[
    #     'session_persistence'] = load_balancer_pool_session_persistence_prototype_model

    # Construct a dict representation of a ResourceGroupIdentityById model
    # resource_group_identity_model = {}
    # resource_group_identity_model['id'] = 'fee82deba12e4c0fb69c3b09d1f12345'

    is_public = True
    subnets = [subnet_identity_model]
    # listeners = [
    #     load_balancer_listener_prototype_load_balancer_context_model
    # ]
    name = generate_name('lb')
    # pools = [load_balancer_pool_prototype_model]
    # resource_group = resource_group_identity_model

    response = service.create_load_balancer(
        is_public,
        subnets,
        # listeners=listeners,
        name=name,
        # pools=pools,
        # resource_group=resource_group,
    )
    return response

# --------------------------------------------------------
# delete_load_balancer()
# --------------------------------------------------------


def delete_load_balancer(service, id):
    response = service.delete_load_balancer(id)
    return response

# --------------------------------------------------------
# get_load_balancer()
# --------------------------------------------------------


def get_load_balancer(service, id):
    response = service.get_load_balancer(id)
    return response


# --------------------------------------------------------
# update_load_balancer()
# --------------------------------------------------------
def update_load_balancer(service, id):
    load_balancer_patch = {}
    load_balancer_patch['name'] = generate_name('lb')
    response = service.update_load_balancer(
        id,
        load_balancer_patch,
    )
    return response

# --------------------------------------------------------
# get_load_balancer_statistics()
# --------------------------------------------------------


def get_load_balancer_statistics(service, id):
    response = service.get_load_balancer_statistics(id)
    return response

# --------------------------------------------------------
# list_load_balancer_listeners()
# --------------------------------------------------------


def list_load_balancer_listeners(service, load_balancer_id):
    response = service.list_load_balancer_listeners(load_balancer_id)
    return response

# --------------------------------------------------------
# create_load_balancer_listener()
# --------------------------------------------------------


def create_load_balancer_listener(service, load_balancer_id):
    # Construct a dict representation of a CertificateInstanceIdentityByCRN model
    # certificate_instance_identity_model = {}
    # certificate_instance_identity_model[
    #     'crn'] = 'crn:v1:bluemix:public:cloudcerts:us-south:a/123456:b8866ea4-b8df-467e-801a-da1db7e020bf:certificate:78ff9c4c97d013fb2a95b21dddde7758'

    # Construct a dict representation of a LoadBalancerPoolIdentityById model
    # load_balancer_pool_identity_model = {}
    # load_balancer_pool_identity_model[
    #     'id'] = '70294e14-4e61-11e8-bcf4-0242ac110004'

    # Construct a dict representation of a LoadBalancerListenerPolicyPrototypeTargetLoadBalancerPoolIdentityLoadBalancerPoolIdentityById model
    # load_balancer_listener_policy_prototype_target_model = {}
    # load_balancer_listener_policy_prototype_target_model[
    #     'id'] = '70294e14-4e61-11e8-bcf4-0242ac110004'

    # Construct a dict representation of a LoadBalancerListenerPolicyRulePrototype model
    # load_balancer_listener_policy_rule_prototype_model = {}
    # load_balancer_listener_policy_rule_prototype_model[
    #     'condition'] = 'contains'
    # load_balancer_listener_policy_rule_prototype_model[
    #     'field'] = 'MY-APP-HEADER'
    # load_balancer_listener_policy_rule_prototype_model['type'] = 'header'
    # load_balancer_listener_policy_rule_prototype_model[
    #     'value'] = 'testString'

    # Construct a dict representation of a LoadBalancerListenerPolicyPrototype model
    # load_balancer_listener_policy_prototype_model = {}
    # load_balancer_listener_policy_prototype_model['action'] = 'forward'
    # load_balancer_listener_policy_prototype_model['name'] = 'my-policy'
    # load_balancer_listener_policy_prototype_model['priority'] = 5
    # load_balancer_listener_policy_prototype_model['rules'] = [
    #     load_balancer_listener_policy_rule_prototype_model
    # ]
    # load_balancer_listener_policy_prototype_model[
    #     'target'] = load_balancer_listener_policy_prototype_target_model

    port = 443
    protocol = 'http'
    # certificate_instance = certificate_instance_identity_model
    # connection_limit = 2000
    # default_pool = load_balancer_pool_identity_model
    # policies = [load_balancer_listener_policy_prototype_model]

    response = service.create_load_balancer_listener(
        load_balancer_id,
        protocol,
        port=port,
        #     certificate_instance=certificate_instance,
        #     connection_limit=connection_limit,
        #     default_pool=default_pool,
        #     policies=policies,
    )
    return response


# --------------------------------------------------------
# delete_load_balancer_listener()
# --------------------------------------------------------
def delete_load_balancer_listener(service, load_balancer_id, id):
    response = service.delete_load_balancer_listener(load_balancer_id, id)
    return response


# --------------------------------------------------------
# get_load_balancer_listener()
# --------------------------------------------------------
def get_load_balancer_listener(service, load_balancer_id, id):
    response = service.get_load_balancer_listener(load_balancer_id, id)
    return response

# --------------------------------------------------------
# update_load_balancer_listener()
# --------------------------------------------------------


def update_load_balancer_listener(service, load_balancer_id, id):
    load_balancer_listener_patch = {}
    load_balancer_listener_patch['connection_limit'] = 2000

    response = service.update_load_balancer_listener(
        load_balancer_id,
        id,
        load_balancer_listener_patch,
    )
    return response
# --------------------------------------------------------
# list_load_balancer_listener_policies()
# --------------------------------------------------------


def list_load_balancer_listener_policies(service, load_balancer_id, listener_id):
    response = service.list_load_balancer_listener_policies(
        load_balancer_id, listener_id)
    return response


# --------------------------------------------------------
# create_load_balancer_listener_policy()
# --------------------------------------------------------
def create_load_balancer_listener_policy(service, load_balancer_id, listener_id):

    # Construct a dict representation of a LoadBalancerListenerPolicyRulePrototype model
    # load_balancer_listener_policy_rule_prototype_model = {}
    # load_balancer_listener_policy_rule_prototype_model[
    #     'condition'] = 'contains'
    # load_balancer_listener_policy_rule_prototype_model[
    #     'field'] = 'MY-APP-HEADER'
    # load_balancer_listener_policy_rule_prototype_model['type'] = 'header'
    # load_balancer_listener_policy_rule_prototype_model[
    #     'value'] = 'testString'

    # Construct a dict representation of a LoadBalancerListenerPolicyPrototypeTargetLoadBalancerPoolIdentityLoadBalancerPoolIdentityById model
    # load_balancer_listener_policy_prototype_target_model = {}
    # load_balancer_listener_policy_prototype_target_model[
    #     'id'] = '70294e14-4e61-11e8-bcf4-0242ac110004'

    action = 'forward'
    priority = 5
    name = generate_name('list-pol')
    # rules = [load_balancer_listener_policy_rule_prototype_model]
    # target = load_balancer_listener_policy_prototype_target_model

    response = service.create_load_balancer_listener_policy(
        load_balancer_id,
        listener_id,
        action,
        priority,
        name=name,
        # rules=rules,
        # target=target,
    )
    return response

# --------------------------------------------------------
# delete_load_balancer_listener_policy()
# --------------------------------------------------------


def delete_load_balancer_listener_policy(service, load_balancer_id, listener_id, id):
    response = service.delete_load_balancer_listener_policy(
        load_balancer_id, listener_id, id)
    return response

# --------------------------------------------------------
# get_load_balancer_listener_policy()
# --------------------------------------------------------


def get_load_balancer_listener_policy(service, load_balancer_id, listener_id, id):
    response = service.get_load_balancer_listener_policy(
        load_balancer_id, listener_id, id)
    return response

# --------------------------------------------------------
# update_load_balancer_listener_policy()
# --------------------------------------------------------


def update_load_balancer_listener_policy(service, load_balancer_id, listener_id, id):

    load_balancer_listener_policy_patch = {}
    load_balancer_listener_policy_patch['name'] = generate_name('list-pol')
    load_balancer_listener_policy_patch['priority'] = 5

    response = service.update_load_balancer_listener_policy(
        load_balancer_id,
        listener_id,
        id,
        load_balancer_listener_policy_patch,
    )

    return response

# --------------------------------------------------------
# list_load_balancer_listener_policy_rules()
# --------------------------------------------------------


def list_load_balancer_listener_policy_rules(service, load_balancer_id, listener_id, policy_id):
    response = service.list_load_balancer_listener_policy_rules(
        load_balancer_id, listener_id, policy_id)
    return response

# --------------------------------------------------------
# create_load_balancer_listener_policy_rule()
# --------------------------------------------------------


def create_load_balancer_listener_policy_rule(service, load_balancer_id, listener_id, policy_id):
    condition = 'contains'
    type = 'header'
    value = 'test'
    field = 'MY-APP-HEADER'

    response = service.create_load_balancer_listener_policy_rule(
        load_balancer_id,
        listener_id,
        policy_id,
        condition,
        type,
        value,
        field=field,
    )
    return response

# --------------------------------------------------------
# delete_load_balancer_listener_policy_rule()
# --------------------------------------------------------


def delete_load_balancer_listener_policy_rule(service, load_balancer_id, listener_id, policy_id, id):
    response = service.delete_load_balancer_listener_policy_rule(
        load_balancer_id, listener_id, policy_id, id)
    return response

# --------------------------------------------------------
# get_load_balancer_listener_policy_rule()
# --------------------------------------------------------


def get_load_balancer_listener_policy_rule(service, load_balancer_id, listener_id, policy_id, id):
    response = service.get_load_balancer_listener_policy_rule(
        load_balancer_id, listener_id, policy_id, id)
    return response


# --------------------------------------------------------
# update_load_balancer_listener_policy_rule()
# --------------------------------------------------------
def update_load_balancer_listener_policy_rule(service, load_balancer_id, listener_id, policy_id, id):
    load_balancer_listener_policy_rule_patch_model = {}
    load_balancer_listener_policy_rule_patch_model['condition'] = 'contains'
    load_balancer_listener_policy_rule_patch_model[
        'field'] = 'MY-APP-HEADER'
    load_balancer_listener_policy_rule_patch_model['type'] = 'header'
    load_balancer_listener_policy_rule_patch_model['value'] = 'some-value'

    response = service.update_load_balancer_listener_policy_rule(
        load_balancer_id,
        listener_id,
        policy_id,
        id,
        load_balancer_listener_policy_rule_patch=load_balancer_listener_policy_rule_patch_model,
    )

    return response


# --------------------------------------------------------
# list_load_balancer_pools()
# --------------------------------------------------------
def list_load_balancer_pools(service, load_balancer_id):
    response = service.list_load_balancer_pools(load_balancer_id)
    return response

# --------------------------------------------------------
# create_load_balancer_pool()
# --------------------------------------------------------


def create_load_balancer_pool(service, load_balancer_id):

    # Construct a dict representation of a LoadBalancerPoolHealthMonitorPrototype model
    load_balancer_pool_health_monitor_prototype_model = {}
    load_balancer_pool_health_monitor_prototype_model['delay'] = 5
    load_balancer_pool_health_monitor_prototype_model['max_retries'] = 2
    load_balancer_pool_health_monitor_prototype_model['port'] = 22
    load_balancer_pool_health_monitor_prototype_model['timeout'] = 2
    load_balancer_pool_health_monitor_prototype_model['type'] = 'http'
    load_balancer_pool_health_monitor_prototype_model['url_path'] = '/'

    # Construct a dict representation of a LoadBalancerPoolMemberTargetPrototypeByAddress model
    load_balancer_pool_member_target_prototype_model = {}
    load_balancer_pool_member_target_prototype_model[
        'address'] = '192.168.3.4'

    # Construct a dict representation of a LoadBalancerPoolMemberPrototype model
    # load_balancer_pool_member_prototype_model = {}
    # load_balancer_pool_member_prototype_model['port'] = 80
    # load_balancer_pool_member_prototype_model[
    #     'target'] = load_balancer_pool_member_target_prototype_model
    # load_balancer_pool_member_prototype_model['weight'] = 50

    # Construct a dict representation of a LoadBalancerPoolSessionPersistencePrototype model
    load_balancer_pool_session_persistence_prototype_model = {}
    load_balancer_pool_session_persistence_prototype_model[
        'type'] = 'source_ip'

    algorithm = 'least_connections'
    health_monitor = load_balancer_pool_health_monitor_prototype_model
    protocol = 'http'
    # members = [load_balancer_pool_member_prototype_model]
    name = generate_name('lb-pool')
    session_persistence = load_balancer_pool_session_persistence_prototype_model

    response = service.create_load_balancer_pool(
        load_balancer_id,
        algorithm,
        health_monitor,
        protocol,
        # members=members,
        name=name,
        # session_persistence=session_persistence,
    )
    return response
# --------------------------------------------------------
# delete_load_balancer_pool()
# --------------------------------------------------------


def delete_load_balancer_pool(service, load_balancer_id, id):
    response = service.delete_load_balancer_pool(load_balancer_id, id)
    return response

# --------------------------------------------------------
# get_load_balancer_pool()
# --------------------------------------------------------


def get_load_balancer_pool(service, load_balancer_id, id):
    response = service.get_load_balancer_pool(load_balancer_id, id)
    return response

# --------------------------------------------------------
# update_load_balancer_pool()
# --------------------------------------------------------


def update_load_balancer_pool(service, load_balancer_id, id):
    load_balancer_pool_patch = {}
    load_balancer_pool_patch['name'] = generate_name('lb-pool')

    response = service.update_load_balancer_pool(
        load_balancer_id,
        id,
        load_balancer_pool_patch,
    )
    return response

# --------------------------------------------------------
# list_load_balancer_pool_members()
# --------------------------------------------------------


def list_load_balancer_pool_members(service, load_balancer_id, pool_id):
    response = service.list_load_balancer_pool_members(
        load_balancer_id, pool_id)
    return response

# --------------------------------------------------------
# create_load_balancer_pool_member()
# --------------------------------------------------------


def create_load_balancer_pool_member(service, load_balancer_id, pool_id):
    # Construct a dict representation of a LoadBalancerPoolMemberTargetPrototypeByAddress model
    load_balancer_pool_member_target_prototype_model = {}
    load_balancer_pool_member_target_prototype_model[
        'address'] = '192.168.3.4'

    port = 80
    target = load_balancer_pool_member_target_prototype_model
    weight = 50

    response = service.create_load_balancer_pool_member(
        load_balancer_id,
        pool_id,
        port,
        target,
        weight=weight,
    )
    return response

# --------------------------------------------------------
# replace_load_balancer_pool_members()
# --------------------------------------------------------


def replace_load_balancer_pool_members(service, load_balancer_id, pool_id):
    # Construct a dict representation of a LoadBalancerPoolMemberTargetPrototypeByAddress model
    # load_balancer_pool_member_target_prototype_model = {}
    # load_balancer_pool_member_target_prototype_model[
    #     'address'] = '192.168.3.4'

    # Construct a dict representation of a LoadBalancerPoolMemberPrototype model
    load_balancer_pool_member_prototype_model = {}
    load_balancer_pool_member_prototype_model['port'] = 82
    # load_balancer_pool_member_prototype_model[
    #     'target'] = load_balancer_pool_member_target_prototype_model
    # load_balancer_pool_member_prototype_model['weight'] = 50

    members = [load_balancer_pool_member_prototype_model]

    response = service.replace_load_balancer_pool_members(
        load_balancer_id,
        pool_id,
        members,
    )
    return response
# --------------------------------------------------------
# delete_load_balancer_pool_member()
# --------------------------------------------------------


def delete_load_balancer_pool_member(service, load_balancer_id, pool_id, id):
    response = service.delete_load_balancer_pool_member(
        load_balancer_id, pool_id, id)
    return response

# --------------------------------------------------------
# get_load_balancer_pool_member()
# --------------------------------------------------------


def get_load_balancer_pool_member(service, load_balancer_id, pool_id, id):
    response = service.get_load_balancer_pool_member(
        load_balancer_id, pool_id, id)
    return response

# --------------------------------------------------------
# update_load_balancer_pool_member()
# --------------------------------------------------------


def update_load_balancer_pool_member(service, load_balancer_id, pool_id, id):

    load_balancer_pool_member_patch = {}
    load_balancer_pool_member_patch['port'] = 80
    load_balancer_pool_member_patch['weight'] = 50

    response = service.update_load_balancer_pool_member(
        load_balancer_id,
        pool_id,
        id,
        load_balancer_pool_member_patch,
    )
    return response

# --------------------------------------------------------
# list_network_acls()
# --------------------------------------------------------


def list_network_acls(service):
    response = service.list_network_acls()
    return response

# --------------------------------------------------------
# create_network_acl()
# --------------------------------------------------------


def create_network_acl(service, source_nacl_id):

    # # Construct a dict representation of a NetworkACLRuleReference model
    # network_acl_rule_reference_model = {}
    # network_acl_rule_reference_model[
    #     'href'] = 'https://us-south.iaas.cloud.ibm.com/v1/network_acls/a4e28308-8ee7-46ab-8108-9f881f22bdbf/rules/8daca77a-4980-4d33-8f3e-7038797be8f9'
    # network_acl_rule_reference_model[
    #     'id'] = '8daca77a-4980-4d33-8f3e-7038797be8f9'
    # network_acl_rule_reference_model['name'] = 'my-rule-1'

    # # Construct a dict representation of a NetworkACLRulePrototypeNetworkACLContextNetworkACLRuleProtocolTCPUDP model
    # network_acl_rule_prototype_network_acl_context_model = {}
    # network_acl_rule_prototype_network_acl_context_model['action'] = 'allow'
    # network_acl_rule_prototype_network_acl_context_model[
    #     'before'] = network_acl_rule_reference_model
    # network_acl_rule_prototype_network_acl_context_model[
    #     'created_at'] = '2020-01-28T18:40:40.123456Z'
    # network_acl_rule_prototype_network_acl_context_model[
    #     'destination'] = '192.168.3.0/24'
    # network_acl_rule_prototype_network_acl_context_model[
    #     'direction'] = 'inbound'
    # network_acl_rule_prototype_network_acl_context_model[
    #     'href'] = 'https://us-south.iaas.cloud.ibm.com/v1/network_acls/a4e28308-8ee7-46ab-8108-9f881f22bdbf/rules/8daca77a-4980-4d33-8f3e-7038797be8f9'
    # network_acl_rule_prototype_network_acl_context_model[
    #     'id'] = '8daca77a-4980-4d33-8f3e-7038797be8f9'
    # network_acl_rule_prototype_network_acl_context_model[
    #     'ip_version'] = 'ipv4'
    # network_acl_rule_prototype_network_acl_context_model[
    #     'name'] = 'my-rule-2'
    # network_acl_rule_prototype_network_acl_context_model['protocol'] = 'udp'
    # network_acl_rule_prototype_network_acl_context_model[
    #     'source'] = '192.168.3.0/24'
    # network_acl_rule_prototype_network_acl_context_model[
    #     'destination_port_max'] = 22
    # network_acl_rule_prototype_network_acl_context_model[
    #     'destination_port_min'] = 22
    # network_acl_rule_prototype_network_acl_context_model[
    #     'source_port_max'] = 65535
    # network_acl_rule_prototype_network_acl_context_model[
    #     'source_port_min'] = 49152

    # Construct a dict representation of a ResourceGroupIdentityById model
    # resource_group_identity_model = {}
    # resource_group_identity_model['id'] = 'fee82deba12e4c0fb69c3b09d1f12345'

    # Construct a dict representation of a VPCIdentityById model
    # vpc_identity_model = {}
    # vpc_identity_model['id'] = '4727d842-f94f-4a2d-824a-9bc9b02c523b'

    # Construct a dict representation of a NetworkACLPrototypeNetworkACLByRules model
    network_acl_prototype_model = {}
    network_acl_prototype_model['name'] = generate_name('nacl')
    # network_acl_prototype_model[
    #     'resource_group'] = resource_group_identity_model
    # network_acl_prototype_model['vpc'] = vpc_identity_model
    # network_acl_prototype_model['rules'] = [
    #     network_acl_rule_prototype_network_acl_context_model
    # ]
    network_acl_reference_model = {}
    network_acl_reference_model['id'] = source_nacl_id
    network_acl_prototype_model['source_network_acl'] = network_acl_reference_model

    # Set up parameter values
    network_acl_prototype = network_acl_prototype_model

    response = service.create_network_acl(
        network_acl_prototype=network_acl_prototype)
    return response

# --------------------------------------------------------
# delete_network_acl()
# --------------------------------------------------------


def delete_network_acl(service, id):
    response = service.delete_network_acl(id)
    return response

# --------------------------------------------------------
# get_network_acl()
# --------------------------------------------------------


def get_network_acl(service, id):
    response = service.get_network_acl(id)
    return response

# --------------------------------------------------------
# update_network_acl()
# --------------------------------------------------------


def update_network_acl(service, id):
    network_acl_patch_model = {}
    network_acl_patch_model['name'] = generate_name('nacl')
    network_acl_patch = network_acl_patch_model
    response = service.update_network_acl(
        id,
        network_acl_patch,
    )
    return response

# --------------------------------------------------------
# list_network_acl_rules()
# --------------------------------------------------------


def list_network_acl_rules(service, network_acl_id):
    response = service.list_network_acl_rules(network_acl_id)
    return response

# --------------------------------------------------------
# create_network_acl_rule()
# --------------------------------------------------------


def create_network_acl_rule(service, network_acl_id):

    # Construct a dict representation of a NetworkACLRuleReference model
    # network_acl_rule_reference_model = {}
    # network_acl_rule_reference_model[
    #     'href'] = 'https://us-south.iaas.cloud.ibm.com/v1/network_acls/a4e28308-8ee7-46ab-8108-9f881f22bdbf/rules/8daca77a-4980-4d33-8f3e-7038797be8f9'
    # network_acl_rule_reference_model[
    #     'id'] = '8daca77a-4980-4d33-8f3e-7038797be8f9'
    # network_acl_rule_reference_model['name'] = 'my-rule-1'

    # Construct a dict representation of a NetworkACLRulePrototypeNetworkACLRuleProtocolICMP model
    network_acl_rule_prototype_model = {}
    network_acl_rule_prototype_model['action'] = 'allow'
    # network_acl_rule_prototype_model[
    #     'before'] = network_acl_rule_reference_model
    network_acl_rule_prototype_model['destination'] = '192.168.3.0/24'
    network_acl_rule_prototype_model['direction'] = 'inbound'
    # network_acl_rule_prototype_model[
    #     'href'] = 'https://us-south.iaas.cloud.ibm.com/v1/network_acls/a4e28308-8ee7-46ab-8108-9f881f22bdbf/rules/8daca77a-4980-4d33-8f3e-7038797be8f9'
    # network_acl_rule_prototype_model[
    #     'id'] = '8daca77a-4980-4d33-8f3e-7038797be8f9'
    network_acl_rule_prototype_model['ip_version'] = 'ipv4'
    network_acl_rule_prototype_model['name'] = 'my-rule-2'
    network_acl_rule_prototype_model['protocol'] = 'icmp'
    network_acl_rule_prototype_model['source'] = '192.168.3.0/24'
    network_acl_rule_prototype_model['code'] = 0
    network_acl_rule_prototype_model['type'] = 8

    network_acl_rule_prototype = network_acl_rule_prototype_model

    response = service.create_network_acl_rule(network_acl_id,
                                               network_acl_rule_prototype)
    return response
# --------------------------------------------------------
# delete_network_acl_rule()
# --------------------------------------------------------


def delete_network_acl_rule(service, network_acl_id, id):
    response = service.delete_network_acl_rule(network_acl_id, id)
    return response

# --------------------------------------------------------
# get_network_acl_rule()
# --------------------------------------------------------


def get_network_acl_rule(service, network_acl_id, id):
    response = service.get_network_acl_rule(network_acl_id, id)
    return response

# --------------------------------------------------------
# update_network_acl_rule()
# --------------------------------------------------------


def update_network_acl_rule(service, network_acl_id, id):
    network_acl_rule_patch_model = {}
    network_acl_rule_patch_model['action'] = 'allow'
    network_acl_rule_patch_model['name'] = generate_name('nacl-rule')
    network_acl_rule_patch_model['destination'] = '192.168.3.2/32'
    network_acl_rule_patch_model['code'] = 0
    network_acl_rule_patch_model['type'] = 8
    network_acl_rule_patch = network_acl_rule_patch_model

    response = service.update_network_acl_rule(network_acl_id, id,
                                               network_acl_rule_patch)

    return response

# --------------------------------------------------------
# list_public_gateways()
# --------------------------------------------------------


def list_public_gateways(service):

    response = service.list_public_gateways()
    return response

# --------------------------------------------------------
# create_public_gateway()
# --------------------------------------------------------


def create_public_gateway(service, vpc, zone):

    # Construct a dict representation of a VPCIdentityById model
    vpc_identity_model = {}
    vpc_identity_model['id'] = vpc

    # Construct a dict representation of a ZoneIdentityByName model
    zone_identity_model = {}
    zone_identity_model['name'] = zone

    # Construct a dict representation of a PublicGatewayPrototypeFloatingIpFloatingIPIdentityFloatingIPIdentityById model
    # public_gateway_prototype_floating_ip_model = {}
    # public_gateway_prototype_floating_ip_model[
    #     'id'] = '39300233-9995-4806-89a5-3c1b6eb88689'

    # Construct a dict representation of a ResourceGroupIdentityById model
    # resource_group_identity_model = {}
    # resource_group_identity_model['id'] = 'fee82deba12e4c0fb69c3b09d1f12345'

    # Set up parameter values
    vpc = vpc_identity_model
    zone = zone_identity_model
    # floating_ip = public_gateway_prototype_floating_ip_model
    name = generate_name('pgw')
    # resource_group = resource_group_identity_model

    response = service.create_public_gateway(
        vpc,
        zone,
        # floating_ip=floating_ip,
        name=name,
        # resource_group=resource_group,
    )

    return response
# --------------------------------------------------------
# delete_public_gateway()
# --------------------------------------------------------


def delete_public_gateway(service, id):
    response = service.delete_public_gateway(id)
    return response

# --------------------------------------------------------
# get_public_gateway()
# --------------------------------------------------------


def get_public_gateway(service, id):
    response = service.get_public_gateway(id)
    return response

# --------------------------------------------------------
# update_public_gateway()
# --------------------------------------------------------


def update_public_gateway(service, id):
    public_gateway_patch = {}
    public_gateway_patch['name'] = generate_name('pgw')
    response = service.update_public_gateway(
        id,
        public_gateway_patch,
    )
    return response

# --------------------------------------------------------
# list_keys()
# --------------------------------------------------------


def list_keys(service):
    response = service.list_keys()
    return response

# --------------------------------------------------------
# create_key()
# --------------------------------------------------------


def create_key(service):
    # Construct a dict representation of a ResourceGroupIdentityById model
    # resource_group_identity_model = {}
    # resource_group_identity_model['id'] = 'fee82deba12e4c0fb69c3b09d1f12345'
    # resource_group = resource_group_identity_model

    public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCcPJwUpNQr0MplO6UM5mfV4vlvY0RpD6gcXqodzZIjsoG31+hQxoJVU9yQcSjahktHFs7Fk2Mo79jUT3wVC8Pg6A3//IDFkLjVrg/mQVpIf6+GxIYEtVg6Tk4pP3YNoksrugGlpJ4LCR3HMe3fBQTQqTzObbb0cSF6xhW5UBq8vhqIkhYKd3KLGJnnrwsIGcwb5BRk68ZFYhreAomvx4jWjaBFlH98HhE4wUEVvJLRy/qR/0w3XVjTSgOlhXywaAOEkmwye7kgSglegCpHWwYNly+NxLONjqbX9rHbFHUVRShnFKh2+M6XKE3HowT/3Y1lDd2PiVQpJY0oQmebiRxB astha.jain@ibm.com'
    name = generate_name('key')
    type = 'rsa'

    response = service.create_key(
        public_key,
        name=name,
        # resource_group=resource_group,
        type=type,
    )
    return response

# --------------------------------------------------------
# delete_key()
# --------------------------------------------------------


def delete_key(service, id):
    response = service.delete_key(id)
    return response


# --------------------------------------------------------
# get_key()
# --------------------------------------------------------
def get_key(service, id):
    response = service.get_key(id)
    return response

# --------------------------------------------------------
# update_key()
# --------------------------------------------------------


def update_key(service, id):
    key_patch = {}
    key_patch['name'] = generate_name('key')
    response = service.update_key(
        id,
        key_patch,
    )
    return response

# --------------------------------------------------------
# list_security_groups()
# --------------------------------------------------------


def list_security_groups(service):
    response = service.list_security_groups()
    return response

# --------------------------------------------------------
# create_security_group()
# --------------------------------------------------------


def create_security_group(service, vpc):

    # Construct a dict representation of a VPCIdentityById model
    vpc_identity_model = {}
    vpc_identity_model['id'] = vpc

    # Construct a dict representation of a ResourceGroupIdentityById model
    # resource_group_identity_model = {}
    # resource_group_identity_model['id'] = 'fee82deba12e4c0fb69c3b09d1f12345'

    # Construct a dict representation of a SecurityGroupRulePrototypeSecurityGroupRuleProtocolICMPRemoteIP model
    # security_group_rule_prototype_security_group_rule_protocol_icmp_remote_model = {}
    # security_group_rule_prototype_security_group_rule_protocol_icmp_remote_model[
    #     'address'] = '192.168.3.4'

    # Construct a dict representation of a SecurityGroupRulePrototypeSecurityGroupRuleProtocolICMP model
    # security_group_rule_prototype_model = {}
    # security_group_rule_prototype_model['direction'] = 'inbound'
    # security_group_rule_prototype_model['ip_version'] = 'ipv4'
    # security_group_rule_prototype_model['protocol'] = 'icmp'
    # security_group_rule_prototype_model[
    #     'remote'] = security_group_rule_prototype_security_group_rule_protocol_icmp_remote_model
    # security_group_rule_prototype_model['code'] = 0
    # security_group_rule_prototype_model['type'] = 8

    # Set up parameter values
    vpc = vpc_identity_model
    name = generate_name('sg')
    # resource_group = resource_group_identity_model
    # rules = [security_group_rule_prototype_model]

    response = service.create_security_group(
        vpc,
        name=name,
        # resource_group=resource_group,
        # rules=rules,
    )
    return response

# --------------------------------------------------------
# delete_security_group()
# --------------------------------------------------------


def delete_security_group(service, id):
    response = service.delete_security_group(id)
    return response


# --------------------------------------------------------
# get_security_group()
# --------------------------------------------------------

def get_security_group(service, id):
    response = service.get_security_group(id)
    return response

# --------------------------------------------------------
# update_security_group()
# --------------------------------------------------------


def update_security_group(service, id):
    security_group_patch = {}
    security_group_patch['name'] = generate_name('sg')
    response = service.update_security_group(
        id,
        security_group_patch,
    )
    return response

# --------------------------------------------------------
# list_security_group_network_interfaces()
# --------------------------------------------------------


def list_security_group_network_interfaces(service, security_group_id):
    response = service.list_security_group_network_interfaces(
        security_group_id)
    return response

# --------------------------------------------------------
# remove_security_group_network_interface()
# --------------------------------------------------------


def remove_security_group_network_interface(service, security_group_id, id):
    response = service.remove_security_group_network_interface(
        security_group_id, id)
    return response

# --------------------------------------------------------
# get_security_group_network_interface()
# --------------------------------------------------------


def get_security_group_network_interface(service, security_group_id, id):
    response = service.get_security_group_network_interface(
        security_group_id, id)
    return response

# --------------------------------------------------------
# add_security_group_network_interface()
# --------------------------------------------------------


def add_security_group_network_interface(service, security_group_id, id):
    response = service.add_security_group_network_interface(
        security_group_id, id)
    return response

# --------------------------------------------------------
# list_security_group_rules()
# --------------------------------------------------------


def list_security_group_rules(service, security_group_id):
    response = service.list_security_group_rules(security_group_id)
    return response

# --------------------------------------------------------
# create_security_group_rule()
# --------------------------------------------------------


def create_security_group_rule(service, sg_id):
    # Construct a dict representation of a SecurityGroupRulePrototypeSecurityGroupRuleProtocolICMPRemoteIP model
    # security_group_rule_prototype_security_group_rule_protocol_icmp_remote_model = {}
    # security_group_rule_prototype_security_group_rule_protocol_icmp_remote_model[
    #     'address'] = '192.168.3.4'

    # Construct a dict representation of a SecurityGroupRulePrototypeSecurityGroupRuleProtocolICMP model
    security_group_rule_prototype_model = {}
    security_group_rule_prototype_model['direction'] = 'inbound'
    # security_group_rule_prototype_model['ip_version'] = 'ipv4'
    # security_group_rule_prototype_model['protocol'] = 'icmp'
    # security_group_rule_prototype_model[
    #     'remote'] = security_group_rule_prototype_security_group_rule_protocol_icmp_remote_model
    # security_group_rule_prototype_model['code'] = 0
    # security_group_rule_prototype_model['type'] = 8

    security_group_id = sg_id
    security_group_rule_prototype = security_group_rule_prototype_model

    response = service.create_security_group_rule(
        security_group_id, security_group_rule_prototype)
    return response

# --------------------------------------------------------
# delete_security_group_rule()
# --------------------------------------------------------


def delete_security_group_rule(service, security_group_id, id):
    response = service.delete_security_group_rule(security_group_id, id)
    return response

# --------------------------------------------------------
# get_security_group_rule()
# --------------------------------------------------------


def get_security_group_rule(service, security_group_id, id):
    response = service.get_security_group_rule(security_group_id, id)
    return response

# --------------------------------------------------------
# update_security_group_rule()
# --------------------------------------------------------


def update_security_group_rule(service, security_group_id, id):
    security_group_rule_patch_model = {}
    security_group_rule_patch_model['code'] = 0
    security_group_rule_patch_model['type'] = 8

    security_group_rule_patch = security_group_rule_patch_model

    response = service.update_security_group_rule(
        security_group_id, id, security_group_rule_patch)
    return response

# --------------------------------------------------------
# list_subnets()
# --------------------------------------------------------


def list_subnets(service):
    response = service.list_subnets()
    return response

# --------------------------------------------------------
# create_subnet()
# --------------------------------------------------------


def create_subnet(service, vpc, zone):
    # Construct a dict representation of a NetworkACLIdentityById model
    # network_acl_identity_model = {}
    # network_acl_identity_model[
    #     'id'] = 'a4e28308-8ee7-46ab-8108-9f881f22bdbf'

    # Construct a dict representation of a PublicGatewayIdentityById model
    # public_gateway_identity_model = {}
    # public_gateway_identity_model[
    #     'id'] = 'dc5431ef-1fc6-4861-adc9-a59d077d1241'

    # Construct a dict representation of a ResourceGroupIdentityById model
    # resource_group_identity_model = {}
    # resource_group_identity_model['id'] = 'fee82deba12e4c0fb69c3b09d1f12345'

    # Construct a dict representation of a VPCIdentityById model
    vpc_identity_model = {}
    vpc_identity_model['id'] = vpc

    # Construct a dict representation of a ZoneIdentityByName model
    zone_identity_model = {}
    zone_identity_model['name'] = zone

    # Construct a dict representation of a SubnetPrototypeSubnetByTotalCount model
    subnet_prototype_model = {}
    subnet_prototype_model['ip_version'] = 'both'
    subnet_prototype_model['name'] = generate_name('subnet')
    # subnet_prototype_model['network_acl'] = network_acl_identity_model
    # subnet_prototype_model['public_gateway'] = public_gateway_identity_model
    # subnet_prototype_model['resource_group'] = resource_group_identity_model
    subnet_prototype_model['vpc'] = vpc_identity_model
    # subnet_prototype_model['total_ipv4_address_count'] = 256
    subnet_prototype_model['ipv4_cidr_block'] = '10.245.0.0/24'
    subnet_prototype_model['zone'] = zone_identity_model

    subnet_prototype = subnet_prototype_model

    response = service.create_subnet(subnet_prototype)
    return response

# --------------------------------------------------------
# delete_subnet()
# --------------------------------------------------------


def delete_subnet(service, id):
    response = service.delete_subnet(id)
    return response

# --------------------------------------------------------
# get_subnet()
# --------------------------------------------------------


def get_subnet(service, id):
    response = service.get_subnet(id)
    return response
# --------------------------------------------------------
# update_subnet()
# --------------------------------------------------------


def update_subnet(service, id):
    subnet_patch = {}
    subnet_patch['name'] = generate_name('subnet')

    response = service.update_subnet(
        id,
        subnet_patch,
    )
    return response

# --------------------------------------------------------
# get_subnet_network_acl()
# --------------------------------------------------------


def get_subnet_network_acl(service, id):
    response = service.get_subnet_network_acl(id)
    return response

# --------------------------------------------------------
# replace_subnet_network_acl()
# --------------------------------------------------------


def replace_subnet_network_acl(service, id, acl):

    # Construct a dict representation of a NetworkACLIdentityById model
    network_acl_identity_model = {}
    network_acl_identity_model[
        'id'] = acl

    network_acl_identity = network_acl_identity_model

    response = service.replace_subnet_network_acl(
        id, network_acl_identity)
    return response

# --------------------------------------------------------
# unset_subnet_public_gateway()
# --------------------------------------------------------


def unset_subnet_public_gateway(service, id):
    response = service.unset_subnet_public_gateway(id)
    return response

# --------------------------------------------------------
# get_subnet_public_gateway()
# --------------------------------------------------------


def get_subnet_public_gateway(service, id):
    response = service.get_subnet_public_gateway(id)
    return response

# --------------------------------------------------------
# set_subnet_public_gateway()
# --------------------------------------------------------


def set_subnet_public_gateway(service, id, pgw):

    # Construct a dict representation of a PublicGatewayIdentityById model
    public_gateway_identity_model = {}
    public_gateway_identity_model[
        'id'] = pgw
    public_gateway_identity = public_gateway_identity_model

    response = service.set_subnet_public_gateway(
        id, public_gateway_identity)
    return response

# --------------------------------------------------------
# vpc_service()
# --------------------------------------------------------


def list_subnet_reserved_ips(service, subnet_id):
    response = service.list_subnet_reserved_ips(subnet_id)
    return response
# --------------------------------------------------------
# create_subnet_reserved_ip()
# --------------------------------------------------------


def create_subnet_reserved_ip(service, subnet_id):
    response = service.create_subnet_reserved_ip(
        subnet_id,
        auto_delete=False,
        name='my-reserved-ip')
    return response

# --------------------------------------------------------
# get_subnet_reserved_ip()
# --------------------------------------------------------


def get_subnet_reserved_ip(service, subnet_id, id):
    response = service.get_subnet_reserved_ip(
        subnet_id, id)
    return response

# --------------------------------------------------------
# update_subnet_reserved_ip()
# --------------------------------------------------------


def update_subnet_reserved_ip(service, subnet_id, id):
    reserved_ip_patch_model = {
        'name': 'my-reserved-ip'
    }

    response = service.update_subnet_reserved_ip(
        subnet_id,
        id,
        reserved_ip_patch=reserved_ip_patch_model)
    return response
# --------------------------------------------------------
# delete_subnet_reserved_ip()
# --------------------------------------------------------


def delete_subnet_reserved_ip(service, subnet_id, id):
    response = service.delete_subnet_reserved_ip(subnet_id, id)
    return response


# --------------------------------------------------------
# list_vpcs()
# --------------------------------------------------------

def list_vpcs(service):
    response = service.list_vpcs()
    return response
# --------------------------------------------------------
# create_vpc()
# --------------------------------------------------------


def create_vpc(service):
    # Construct a dict representation of a ResourceGroupIdentityById model
    # resource_group_identity_model = {}
    # resource_group_identity_model['id'] = 'fee82deba12e4c0fb69c3b09d1f12345'

    # Set up parameter values
    address_prefix_management = 'manual'
    classic_access = False
    name = generate_name('vpc')
    # resource_group = resource_group_identity_model

    response = service.create_vpc(
        address_prefix_management=address_prefix_management,
        classic_access=classic_access,
        name=name,
        # resource_group=resource_group,
    )
    return response

# --------------------------------------------------------
# delete_vpc()
# --------------------------------------------------------


def delete_vpc(service, id):
    response = service.delete_vpc(id)
    return response

# --------------------------------------------------------
# get_vpc()
# --------------------------------------------------------


def get_vpc(service, id):
    response = service.get_vpc(id)
    return response


# --------------------------------------------------------
# update_vpc()
# --------------------------------------------------------
def update_vpc(service, id):
    vpc_patch_model = {}
    vpc_patch_model['name'] = generate_name('vpc')
    vpc_patch = vpc_patch_model
    response = service.update_vpc(
        id,
        vpc_patch,
    )
    return response

# --------------------------------------------------------
# get_vpc_default_network_acl()
# --------------------------------------------------------


def get_vpc_default_network_acl(service, id):
    response = service.get_vpc_default_network_acl(id)
    return response

# --------------------------------------------------------
# get_vpc_default_security_group()
# --------------------------------------------------------


def get_vpc_default_security_group(service, id):
    response = service.get_vpc_default_security_group(id)
    return response

# --------------------------------------------------------
# list_vpc_address_prefixes()
# --------------------------------------------------------


def list_vpc_address_prefixes(service, vpc_id):
    response = service.list_vpc_address_prefixes(vpc_id)
    return response


# --------------------------------------------------------
# create_vpc_address_prefix()
# --------------------------------------------------------

def create_vpc_address_prefix(service, vpc_id, zone):
    # Construct a dict representation of a ZoneIdentityByName model
    zone_identity_model = {}
    zone_identity_model['name'] = zone
    cidr = '10.0.0.0/24'
    zone = zone_identity_model
    is_default = True
    name = generate_name('add-pfx')

    response = service.create_vpc_address_prefix(
        vpc_id,
        cidr,
        zone,
        is_default=is_default,
        name=name,
    )
    return response

# --------------------------------------------------------
# delete_vpc_address_prefix()
# --------------------------------------------------------


def delete_vpc_address_prefix(service, vpc_id, id):
    response = service.delete_vpc_address_prefix(vpc_id, id)
    return response

# --------------------------------------------------------
# get_vpc_address_prefix()
# --------------------------------------------------------


def get_vpc_address_prefix(service, vpc_id, id):
    response = service.get_vpc_address_prefix(vpc_id, id)
    return response

# --------------------------------------------------------
# update_vpc_address_prefix()
# --------------------------------------------------------


def update_vpc_address_prefix(service, vpc_id, id):
    address_prefix_patch_model = {}
    address_prefix_patch_model['name'] = generate_name('addr-prefix')
    address_prefix_patch_model['is_default'] = False
    response = service.update_vpc_address_prefix(
        vpc_id,
        id,
        address_prefix_patch=address_prefix_patch_model,
    )
    return response

# --------------------------------------------------------
# list_vpc_routes()
# --------------------------------------------------------


def list_vpc_routes(service, vpc_id, zone_name):
    response = service.list_vpc_routes(vpc_id, zone_name=zone_name)
    return response

# --------------------------------------------------------
# list_vpc_routes()
# --------------------------------------------------------


def list_vpc_routes(service, vpc_id):
    response = service.list_vpc_routes(vpc_id)
    return response


# --------------------------------------------------------
# create_vpc_route()
# --------------------------------------------------------
def create_vpc_route(service, vpc_id, zone):
    # Construct a dict representation of a ZoneIdentityByName model
    zone_identity_model = {}
    zone_identity_model['name'] = zone

    # Construct a dict representation of a RouteNextHopPrototypeRouteNextHopIP model
    route_next_hop_prototype_model = {}
    route_next_hop_prototype_model['address'] = '10.5.0.25'

    destination = '10.168.10.0/28'
    zone = zone_identity_model
    name = generate_name('route')
    next_hop = route_next_hop_prototype_model

    response = service.create_vpc_route(
        vpc_id,
        destination,
        next_hop,
        zone,
        name=name,
    )
    return response


# --------------------------------------------------------
# delete_vpc_route()
# --------------------------------------------------------
def delete_vpc_route(service, vpc_id, id):
    response = service.delete_vpc_route(vpc_id, id)
    return response
# --------------------------------------------------------
# get_vpc_route()
# --------------------------------------------------------


def get_vpc_route(service, vpc_id, id):
    response = service.get_vpc_route(vpc_id, id)
    return response
# --------------------------------------------------------
# update_vpc_route()
# --------------------------------------------------------


def update_vpc_route(service, vpc_id, id):
    route_patch_model = {}
    route_patch_model['name'] = generate_name('route')
    response = service.update_vpc_route(
        vpc_id,
        id,
        route_patch=route_patch_model,
    )
    return response

# --------------------------------------------------------
# list_ike_policies()
# --------------------------------------------------------


def list_ike_policies(service):
    response = service.list_ike_policies()
    return response

# --------------------------------------------------------
# create_ike_policy()
# --------------------------------------------------------


def create_ike_policy(service):
    # # Construct a dict representation of a ResourceGroupIdentityById model
    # resource_group_identity_model = {}
    # resource_group_identity_model['id'] = 'fee82deba12e4c0fb69c3b09d1f12345'

    authentication_algorithm = 'md5'
    dh_group = 5
    encryption_algorithm = 'triple_des'
    ike_version = 1
    key_lifetime = 28800
    name = generate_name('ike')
    # resource_group = resource_group_identity_model

    response = service.create_ike_policy(
        authentication_algorithm,
        dh_group,
        encryption_algorithm,
        ike_version,
        key_lifetime=key_lifetime,
        name=name,
        # resource_group=resource_group,
    )
    return response


# --------------------------------------------------------
# delete_ike_policy()
# --------------------------------------------------------

def delete_ike_policy(service, id):
    response = service.delete_ike_policy(id)
    return response


# --------------------------------------------------------
# get_ike_policy()
# --------------------------------------------------------

def get_ike_policy(service, id):
    response = service.get_ike_policy(id)
    return response


# --------------------------------------------------------
# update_ike_policy()
# --------------------------------------------------------

def update_ike_policy(service, id):

    ike_policy_patch_model = {}
    ike_policy_patch_model['name'] = generate_name('ike')
    ike_policy_patch_model['authentication_algorithm'] = 'md5'

    ike_policy_patch = ike_policy_patch_model

    response = service.update_ike_policy(
        id,
        ike_policy_patch,
    )
    return response
# --------------------------------------------------------
# list_ike_policy_connections()
# --------------------------------------------------------


def list_ike_policy_connections(service, id):
    response = service.list_ike_policy_connections(id)
    return response


# --------------------------------------------------------
# list_ipsec_policies()
# --------------------------------------------------------
def list_ipsec_policies(service):
    response = service.list_ipsec_policies()
    return response

# --------------------------------------------------------
# create_ipsec_policy()
# --------------------------------------------------------


def create_ipsec_policy(service):

    # Construct a dict representation of a ResourceGroupIdentityById model
    # resource_group_identity_model = {}
    # resource_group_identity_model['id'] = 'fee82deba12e4c0fb69c3b09d1f12345'

    authentication_algorithm = 'md5'
    encryption_algorithm = 'triple_des'
    pfs = 'disabled'
    key_lifetime = 3600
    name = generate_name('ipsec')
    # resource_group = resource_group_identity_model

    response = service.create_ipsec_policy(
        authentication_algorithm,
        encryption_algorithm,
        pfs,
        key_lifetime=key_lifetime,
        name=name,
        # resource_group=resource_group,
    )
    return response

# --------------------------------

# --------------------------------------------------------
# delete_ipsec_policy()
# --------------------------------------------------------


def delete_ipsec_policy(service, id):
    response = service.delete_ipsec_policy(id)
    return response

# --------------------------------------------------------
# get_ipsec_policy()
# --------------------------------------------------------


def get_ipsec_policy(service, id):

    response = service.get_ipsec_policy(id)
    return response

# --------------------------------------------------------
# update_ipsec_policy()
# --------------------------------------------------------


def update_ipsec_policy(service, id):

    i_psec_policy_patch_model = {}
    i_psec_policy_patch_model['name'] = generate_name('ipsec')
    i_psec_policy_patch_model['authentication_algorithm'] = 'md5'

    i_psec_policy_patch = i_psec_policy_patch_model

    response = service.update_ipsec_policy(
        id,
        i_psec_policy_patch=i_psec_policy_patch_model,
    )
    return response
# --------------------------------------------------------
# list_ipsec_policy_connections()
# --------------------------------------------------------


def list_ipsec_policy_connections(service, id):
    response = service.list_ipsec_policy_connections(id)
    return response

# --------------------------------------------------------
# list_vpn_gateways()
# --------------------------------------------------------


def list_vpn_gateways(service):
    response = service.list_vpn_gateways()
    return response

# --------------------------------------------------------
# create_vpn_gateway()
# --------------------------------------------------------


def create_vpn_gateway(service, subnet):
    subnet_identity_model = {}
    subnet_identity_model['id'] = subnet

    vpn_gateway_prototype_model = {}
    vpn_gateway_prototype_model['name'] = generate_name('vpng')
    vpn_gateway_prototype_model['subnet'] = subnet_identity_model
    vpn_gateway_prototype_model['mode'] = 'route'

    # Set up parameter values
    vpn_gateway_prototype = vpn_gateway_prototype_model

    response = service.create_vpn_gateway(vpn_gateway_prototype)
    return response

# --------------------------------------------------------
# delete_vpn_gateway()
# --------------------------------------------------------


def delete_vpn_gateway(service, id):
    response = service.delete_vpn_gateway(id)
    return response

# --------------------------------------------------------
# get_vpn_gateway()
# --------------------------------------------------------


def get_vpn_gateway(service, id):
    response = service.get_vpn_gateway(id)
    return response


# --------------------------------------------------------
# update_vpn_gateway()
# --------------------------------------------------------

def update_vpn_gateway(service, id):
    vpn_gateway_patch_model = {}
    vpn_gateway_patch_model['name'] = generate_name('vpng')
    response = service.update_vpn_gateway(
        id,
        vpn_gateway_patch=vpn_gateway_patch_model,
    )
    return response

# --------------------------------------------------------
# list_vpn_gateway_connections()
# --------------------------------------------------------


def list_vpn_gateway_connections(service, vpn_gateway_id):
    response = service.list_vpn_gateway_connections(vpn_gateway_id)
    return response

# --------------------------------------------------------
# create_vpn_gateway_connection()
# --------------------------------------------------------


def create_vpn_gateway_connection(service, vpn_gateway_id):

    vpn_gateway_connection_prototype_model = {}
    vpn_gateway_connection_prototype_model['admin_state_up'] = True
    vpn_gateway_connection_prototype_model['name'] = 'my-vpn-connection'
    vpn_gateway_connection_prototype_model['peer_address'] = '169.21.50.5'
    vpn_gateway_connection_prototype_model['psk'] = 'lkj14b1oi0alcniejkso'
    vpn_gateway_connection_prototype_model['routing_protocol'] = 'none'

    response = service.create_vpn_gateway_connection(
        vpn_gateway_id,
        vpn_gateway_connection_prototype=vpn_gateway_connection_prototype_model,
    )
    return response
# --------------------------------------------------------
# delete_vpn_gateway_connection()
# --------------------------------------------------------


def delete_vpn_gateway_connection(service, vpn_gateway_id, id):
    response = service.delete_vpn_gateway_connection(vpn_gateway_id, id)
    return response
# --------------------------------------------------------
# get_vpn_gateway_connection()
# --------------------------------------------------------


def get_vpn_gateway_connection(service, vpn_gateway_id, id):
    response = service.get_vpn_gateway_connection(vpn_gateway_id, id)
    return response

# --------------------------------------------------------
# update_vpn_gateway_connection()
# --------------------------------------------------------


def update_vpn_gateway_connection(service, vpn_gateway_id, id):
    vpn_gateway_connection_patch_model = {}
    vpn_gateway_connection_patch_model['name'] = generate_name('vpn-con')

    response = service.update_vpn_gateway_connection(
        vpn_gateway_id,
        id,
        vpn_gateway_connection_patch=vpn_gateway_connection_patch_model,
    )
    return response

# --------------------------------------------------------
# list_vpn_gateway_connection_local_cidrs()
# --------------------------------------------------------


def list_vpn_gateway_connection_local_cidrs(service, vpn_gateway_id, id):
    response = service.list_vpn_gateway_connection_local_cidrs(
        vpn_gateway_id, id)
    return response

# --------------------------------------------------------
# remove_vpn_gateway_connection_local_cidr()
# --------------------------------------------------------


def remove_vpn_gateway_connection_local_cidr(service, vpn_gateway_id, id, prefix_address, prefix_length):
    response = service.remove_vpn_gateway_connection_local_cidr(
        vpn_gateway_id, id, prefix_address, prefix_length)
    return response

# --------------------------------------------------------
# check_vpn_gateway_connection_local_cidr()
# --------------------------------------------------------


def check_vpn_gateway_connection_local_cidr(service, vpn_gateway_id, id, prefix_address, prefix_length):
    response = service.check_vpn_gateway_connection_local_cidr(
        vpn_gateway_id, id, prefix_address, prefix_length)
    return response
# --------------------------------------------------------
# add_vpn_gateway_connection_local_cidr()
# --------------------------------------------------------


def add_vpn_gateway_connection_local_cidr(service, vpn_gateway_id, id, prefix_address, prefix_length):
    response = service.add_vpn_gateway_connection_local_cidr(
        vpn_gateway_id, id, prefix_address, prefix_length)
    return response
# --------------------------------------------------------
# list_vpn_gateway_connection_peer_cidrs()
# --------------------------------------------------------


def list_vpn_gateway_connection_peer_cidrs(service, vpn_gateway_id, id):
    response = service.list_vpn_gateway_connection_peer_cidrs(
        vpn_gateway_id, id)
    return response

# --------------------------------------------------------
# remove_vpn_gateway_connection_peer_cidr()
# --------------------------------------------------------


def remove_vpn_gateway_connection_peer_cidr(service, vpn_gateway_id, id, prefix_address, prefix_length):
    response = service.remove_vpn_gateway_connection_peer_cidr(
        vpn_gateway_id, id, prefix_address, prefix_length)
    return response

# --------------------------------------------------------
# check_vpn_gateway_connection_peer_cidr()
# --------------------------------------------------------


def check_vpn_gateway_connection_peer_cidr(service, vpn_gateway_id, id, prefix_address, prefix_length):
    response = service.check_vpn_gateway_connection_peer_cidr(
        vpn_gateway_id, id, prefix_address, prefix_length)
    return response
# --------------------------------------------------------
# add_vpn_gateway_connection_peer_cidr()
# --------------------------------------------------------


def add_vpn_gateway_connection_peer_cidr(service, vpn_gateway_id, id, prefix_address, prefix_length):
    response = service.add_vpn_gateway_connection_peer_cidr(
        vpn_gateway_id, id, prefix_address, prefix_length)
    return response

# --------------------------------------------------------
# list_volume_profiles()
# --------------------------------------------------------


def list_volume_profiles(service):
    response = service.list_volume_profiles()
    return response

# --------------------------------------------------------
# get_volume_profile()
# --------------------------------------------------------


def get_volume_profile(service, name):
    response = service.get_volume_profile(name)
    return response
# --------------------------------------------------------
# list_volumes()
# --------------------------------------------------------


def list_volumes(service):
    response = service.list_volumes()
    return response
# --------------------------------------------------------
# create_volume()
# --------------------------------------------------------


def create_volume(service, zone):
    # Construct a dict representation of a ResourceGroupIdentityById model
    # resource_group_identity_model = {}
    # resource_group_identity_model['id'] = 'fee82deba12e4c0fb69c3b09d1f12345'

    # Construct a dict representation of a VolumeProfileIdentityByName model
    volume_profile_identity_model = {}
    volume_profile_identity_model['name'] = 'general-purpose'

    # Construct a dict representation of a ZoneIdentityByName model
    zone_identity_model = {}
    zone_identity_model['name'] = zone

    # Construct a dict representation of a VolumePrototypeVolumeByCapacity model
    volume_prototype_model = {}
    volume_prototype_model['iops'] = 10000
    volume_prototype_model['name'] = 'my-volume'
    volume_prototype_model['profile'] = volume_profile_identity_model
    # volume_prototype_model['resource_group'] = resource_group_identity_model
    volume_prototype_model['zone'] = zone_identity_model
    volume_prototype_model['capacity'] = 100

    volume_prototype = volume_prototype_model
    response = service.create_volume(volume_prototype)
    return response

# --------------------------------------------------------
# delete_volume()
# --------------------------------------------------------


def delete_volume(service, id):
    response = service.delete_volume(id)
    return response

# --------------------------------------------------------
# get_volume()
# --------------------------------------------------------


def get_volume(service, id):
    response = service.get_volume(id)
    return response
# --------------------------------------------------------
# update_volume()
# --------------------------------------------------------


def update_volume(service, id):
    volume_patch_model = {}
    volume_patch_model['name'] = generate_name('vol')
    response = service.update_volume(
        id,
        volume_patch=volume_patch_model,
    )
    return response

# --------------------------------------------------------
# list_flow_log_collectors()
# --------------------------------------------------------


def list_flow_log_collectors(service):
    response = service.list_flow_log_collectors()
    return response

# --------------------------------------------------------
# create_flow_log_collector()
# --------------------------------------------------------


def create_flow_log_collector(service, target_id):

    # Construct a dict representation of a CloudObjectStorageBucketIdentityByName model
    cloud_object_storage_bucket_identity_model = {}
    cloud_object_storage_bucket_identity_model[
        'name'] = generate_name('cos-bucket')

    # Construct a dict representation of a FlowLogCollectorPrototypeTargetNetworkInterfaceIdentityNetworkInterfaceIdentityById model
    flow_log_collector_prototype_target_model = {}
    flow_log_collector_prototype_target_model[
        'id'] = target_id

    # Construct a dict representation of a ResourceGroupIdentityById model
    # resource_group_identity_model = {}
    # resource_group_identity_model['id'] = 'fee82deba12e4c0fb69c3b09d1f12345'

    # Set up parameter values
    storage_bucket = cloud_object_storage_bucket_identity_model
    target = flow_log_collector_prototype_target_model
    active = False
    name = generate_name('flow-log')
    # resource_group = resource_group_identity_model

    response = service.create_flow_log_collector(
        storage_bucket,
        target,
        active=active,
        name=name,
        # resource_group=resource_group,
    )
    return response

# --------------------------------------------------------
# delete_flow_log_collector()
# --------------------------------------------------------


def delete_flow_log_collector(service, id):
    response = service.delete_flow_log_collector(id)
    return response

# --------------------------------------------------------
# get_flow_log_collector()
# --------------------------------------------------------


def get_flow_log_collector(service, id):
    response = service.get_flow_log_collector(id)
    return response

# --------------------------------------------------------
# update_flow_log_collector()
# --------------------------------------------------------


def update_flow_log_collector(service, id):
    flow_log_collector_patch_model = {}
    flow_log_collector_patch_model['name'] = generate_name('flow-log')
    response = service.update_flow_log_collector(id,
                                                 flow_log_collector_patch=flow_log_collector_patch_model,
                                                 )
    return response

# --------------------------------------------------------
# list_instance_templates()
# --------------------------------------------------------


def list_instance_templates(service):
    response = service.list_instance_templates()
    return response

# --------------------------------------------------------
# create_instance_template()
# --------------------------------------------------------


def create_instance_template(service, vpc, profile, zone, image, subnet):
    # Construct a dict representation of a SubnetIdentityById model
    subnet_identity_model = {}
    subnet_identity_model['id'] = subnet

    # Construct a dict representation of a ImageIdentityById model
    image_identity_model = {}
    image_identity_model['id'] = image

    # Construct a dict representation of a InstanceProfileIdentityByName model
    instance_profile_identity_model = {}
    instance_profile_identity_model['name'] = profile

    # Construct a dict representation of a NetworkInterfacePrototype model
    network_interface_prototype_model = {}

    network_interface_prototype_model['subnet'] = subnet_identity_model

    # Construct a dict representation of a VPCIdentityById model
    vpc_identity_model = {}
    vpc_identity_model['id'] = vpc

    # Construct a dict representation of a ZoneIdentityByName model
    zone_identity_model = {}
    zone_identity_model['name'] = zone

    instance_template_prototype_model = {}
    instance_template_prototype_model['name'] = generate_name('template')

    instance_template_prototype_model['profile'] = instance_profile_identity_model

    instance_template_prototype_model['vpc'] = vpc_identity_model

    instance_template_prototype_model['image'] = image_identity_model
    instance_template_prototype_model[
        'primary_network_interface'] = network_interface_prototype_model
    instance_template_prototype_model['zone'] = zone_identity_model

    instance_template_prototype = instance_template_prototype_model

    # Invoke method
    response = service.create_instance_template(instance_template_prototype)
    return response

# --------------------------------------------------------
# delete_instance_template()
# --------------------------------------------------------


def delete_instance_template(service, id):
    response = service.delete_instance_template(id)
    return response

# --------------------------------------------------------
# get_instance_template()
# --------------------------------------------------------


def get_instance_template(service, id):
    response = service.get_instance_template(id)
    return response

# --------------------------------------------------------
# update_instance_template()
# --------------------------------------------------------


def update_instance_template(service, id):
    instance_template_patch_model = {}
    instance_template_patch_model['name'] = generate_name("template")
    response = service.update_instance_template(
        id,
        instance_template_patch=instance_template_patch_model,
    )
    return response

# --------------------------------------------------------
# list_instance_groups()
# --------------------------------------------------------


def list_instance_groups(service):
    response = service.list_instance_groups()
    return response

# --------------------------------------------------------
# create_instance_groups()
# --------------------------------------------------------


def create_instance_group(service, instance_template, subnet):

    # Construct a dict representation of a InstanceTemplateIdentityById model
    instance_template_identity_model = {}
    instance_template_identity_model[
        'id'] = instance_template

    # Construct a dict representation of a SubnetIdentityById model
    subnet_identity_model = {}
    subnet_identity_model['id'] = subnet

    # Set up parameter values
    instance_template = instance_template_identity_model
    subnets = [subnet_identity_model]
    name = generate_name("instance-group")
    membership_count = 2

    # Invoke method
    response = service.create_instance_group(
        instance_template,
        subnets,
        name=name,
        membership_count=membership_count,
    )
    return response
# --------------------------------------------------------
# delete_instance_group)
# --------------------------------------------------------


def delete_instance_group(service, id):
    response = service.delete_instance_group(id)
    return response

# --------------------------------------------------------
# get_instance_group()
# --------------------------------------------------------


def get_instance_group(service, id):
    response = service.get_instance_group(id)
    return response

# --------------------------------------------------------
# update_instance_group()
# --------------------------------------------------------


def update_instance_group(service, id):
    instance_group_patch_model = {}
    instance_group_patch_model['name'] = generate_name("instance-group")
    response = service.update_instance_group(
        id, instance_group_patch=instance_group_patch_model)
    return response
# --------------------------------------------------------
# delete_instance_group_load_balancer()
# --------------------------------------------------------


def delete_instance_group_load_balancer(service, instance_group_id):
    response = service.delete_instance_group_load_balancer(
        instance_group_id)
    return response
# --------------------------------------------------------
# list_instance_group_managers()
# --------------------------------------------------------


def list_instance_group_managers(service, instance_group_id):
    response = service.list_instance_group_managers(instance_group_id)
    return response
# --------------------------------------------------------
# create_instance_group_manager()
# --------------------------------------------------------


def create_instance_group_manager(service, id):
    # Construct a dict representation of a InstanceGroupManagerPrototypeInstanceGroupManagerAutoScalePrototype model
    instance_group_manager_prototype_model = {}
    instance_group_manager_prototype_model[
        'name'] = generate_name("manager")
    instance_group_manager_prototype_model['management_enabled'] = True
    instance_group_manager_prototype_model['aggregation_window'] = 120
    instance_group_manager_prototype_model['cooldown'] = 300
    instance_group_manager_prototype_model['max_membership_count'] = 2
    instance_group_manager_prototype_model['min_membership_count'] = 1
    instance_group_manager_prototype_model['manager_type'] = 'autoscale'

    # Set up parameter values
    instance_group_id = id
    instance_group_manager_prototype = instance_group_manager_prototype_model

    # Invoke method
    response = service.create_instance_group_manager(
        instance_group_id, instance_group_manager_prototype)
    return response
# --------------------------------------------------------
# delete_instance_group_manager()
# --------------------------------------------------------


def delete_instance_group_manager(service, instance_group_id, id):
    response = service.delete_instance_group_manager(instance_group_id,
                                                     id)
    return response
# --------------------------------------------------------
# get_instance_group_manager()
# --------------------------------------------------------


def get_instance_group_manager(service, instance_group_id, id):
    response = service.get_instance_group_manager(instance_group_id,
                                                  id)
    return response
# --------------------------------------------------------
# update_instance_group_manager()
# --------------------------------------------------------


def update_instance_group_manager(service, instance_group_id, id):
    instance_group_manager_patch_model = {}
    instance_group_manager_patch_model['cooldown'] = 210
    response = service.update_instance_group_manager(
        instance_group_id,
        id,
        instance_group_manager_patch=instance_group_manager_patch_model,
    )
    return response
# --------------------------------------------------------
# list_instance_group_manager_policies()
# --------------------------------------------------------


def list_instance_group_manager_policies(service,
                                         instance_group_id, instance_group_manager_id):

    # Invoke method
    response = service.list_instance_group_manager_policies(
        instance_group_id, instance_group_manager_id)
    return response
# --------------------------------------------------------
# create_instance_group_manager_policy()
# --------------------------------------------------------


def create_instance_group_manager_policy(service, instance_group_id,
                                         instance_group_manager_id):

    instance_group_manager_policy_prototype_model = {}
    instance_group_manager_policy_prototype_model['name'] = generate_name(
        "mpolicy")
    instance_group_manager_policy_prototype_model['metric_type'] = 'cpu'
    instance_group_manager_policy_prototype_model['metric_value'] = 38
    instance_group_manager_policy_prototype_model['policy_type'] = 'target'

    # Set up parameter values
    instance_group_manager_policy_prototype = instance_group_manager_policy_prototype_model

    # Invoke method
    response = service.create_instance_group_manager_policy(
        instance_group_id,
        instance_group_manager_id,
        instance_group_manager_policy_prototype)
    return response
# --------------------------------------------------------
# delete_instance_group_manager_policy()
# --------------------------------------------------------


def delete_instance_group_manager_policy(service, instance_group_id, instance_group_manager_id, id):
    response = service.delete_instance_group_manager_policy(
        instance_group_id, instance_group_manager_id, id)
    return response
# --------------------------------------------------------
# get_instance_group_manager_policy()
# --------------------------------------------------------


def get_instance_group_manager_policy(service, instance_group_id, instance_group_manager_id, id):
    # Invoke method
    response = service.get_instance_group_manager_policy(
        instance_group_id, instance_group_manager_id, id)
    return response
# --------------------------------------------------------
# update_instance_group_manager_policy()
# --------------------------------------------------------


def update_instance_group_manager_policy(service, instance_group_id, instance_group_manager_id, id):

    instance_group_manager_policy_patch_model = {}
    instance_group_manager_policy_patch_model['metric_type'] = 'cpu'
    instance_group_manager_policy_patch_model['metric_value'] = 38

    # Invoke method
    response = service.update_instance_group_manager_policy(
        instance_group_id,
        instance_group_manager_id,
        id,
        instance_group_manager_policy_patch=instance_group_manager_policy_patch_model,
    )
    return response
# --------------------------------------------------------
# delete_instance_group_memberships()
# --------------------------------------------------------


def delete_instance_group_memberships(service, instance_group_id):
    # Invoke method
    response = service.delete_instance_group_memberships(instance_group_id)
    return response
# --------------------------------------------------------
# list_instance_group_memberships()
# --------------------------------------------------------


def list_instance_group_memberships(service, instance_group_id):
    response = service.list_instance_group_memberships(instance_group_id)
    return response
# --------------------------------------------------------
# delete_instance_group_membership()
# --------------------------------------------------------


def delete_instance_group_membership(service, instance_group_id, id):
    response = service.delete_instance_group_membership(instance_group_id,
                                                        id)
    return response
# --------------------------------------------------------
# get_instance_group_membership()
# --------------------------------------------------------


def get_instance_group_membership(service, instance_group_id, id):
    response = service.get_instance_group_membership(instance_group_id,
                                                     id)
    return response
# --------------------------------------------------------
# update_instance_group_membership()
# --------------------------------------------------------


def update_instance_group_membership(service, instance_group_id, id):
    instance_group_membership_patch_model = {}
    instance_group_membership_patch_model[
        'name'] = generate_name("member")
    response = service.update_instance_group_membership(instance_group_id,
                                                        id,
                                                        instance_group_membership_patch=instance_group_membership_patch_model,
                                                        )
    return response

# --------------------------------------------------------
# list_endpoint_gateways()
# --------------------------------------------------------


def list_endpoint_gateways(service):
    response = service.list_endpoint_gateways()
    return response

# --------------------------------------------------------
# create_endpoint_gateway()
# --------------------------------------------------------


def create_endpoint_gateway(service, vpcId):
    endpoint_gateway_target_prototype_model = {}
    endpoint_gateway_target_prototype_model['resource_type'] = 'provider_infrastructure_service'
    endpoint_gateway_target_prototype_model['name'] = 'ibm-ntp-server'

    vpc_identity_model = {}
    vpc_identity_model['id'] = vpcId

    response = service.create_endpoint_gateway(
        target=endpoint_gateway_target_prototype_model,
        vpc=vpc_identity_model,
    )
    return response
# --------------------------------------------------------
# delete_endpoint_gateway()
# --------------------------------------------------------


def delete_endpoint_gateway(service, id):
    response = service.delete_endpoint_gateway(id)
    return response

# --------------------------------------------------------
# get_endpoint_gateway()
# --------------------------------------------------------


def get_endpoint_gateway(service, id):
    response = service.get_endpoint_gateway(id)
    return response

# --------------------------------------------------------
# get_endpoint_gateway()
# --------------------------------------------------------


def update_endpoint_gateway(service, id):
    endpoint_gateway_patch_model = {}
    endpoint_gateway_patch_model['name'] = generate_name("endpoint-gateway")
    response = service.update_endpoint_gateway(id,
                                               endpoint_gateway_patch=endpoint_gateway_patch_model)
    return response

# --------------------------------------------------------
# list_endpoint_gateway_ips()
# --------------------------------------------------------


def list_endpoint_gateway_ips(service, id):
    response = service.list_endpoint_gateway_ips(endpoint_gateway_id=id)
    return response

# --------------------------------------------------------
# remove_endpoint_gateway_ip()
# --------------------------------------------------------


def remove_endpoint_gateway_ip(service, endpoint_gateway_id, id):
    response = service.remove_endpoint_gateway_ip(
        endpoint_gateway_id=endpoint_gateway_id, id=id)
    return response

# --------------------------------------------------------
# get_endpoint_gateway_ip()
# --------------------------------------------------------


def get_endpoint_gateway_ip(service, endpoint_gateway_id, id):
    response = service.get_endpoint_gateway_ip(
        endpoint_gateway_id=endpoint_gateway_id, id=id)
    return response

# --------------------------------------------------------
# add_endpoint_gateway_ip()
# --------------------------------------------------------


def add_endpoint_gateway_ip(service, endpoint_gateway_id, id):
    response = service.add_endpoint_gateway_ip(endpoint_gateway_id, id)
    return response

# --------------------------------------------------------
# get_vpc_default_routing_table()
# --------------------------------------------------------


def get_vpc_default_routing_table(service, id):
    response = service.get_vpc_default_routing_table(id=id)
    return response

# --------------------------------------------------------
# get_subnet_routing_table()
# --------------------------------------------------------


def get_subnet_routing_table(service, id):
    response = service.get_subnet_routing_table(id=id)
    return response
# --------------------------------------------------------
# replace_subnet_routing_table()
# --------------------------------------------------------


def replace_subnet_routing_table(service, routing_table_id, id):
    routing_table_identity_model = {}
    routing_table_identity_model['id'] = routing_table_id
    response = service.replace_subnet_routing_table(id=id,
                                                    routing_table_identity=routing_table_identity_model)
    return response

# --------------------------------------------------------
# list_vpc_routing_tables()
# --------------------------------------------------------


def list_vpc_routing_tables(service, vpc_id):
    response = service.list_vpc_routing_tables(vpc_id=vpc_id)
    return response

# --------------------------------------------------------
# create_vpc_routing_table()
# --------------------------------------------------------


def create_vpc_routing_table(service, vpc_id, zoneName):
    route_next_hop_prototype_model = {'address': '192.168.3.4'}

    zone_identity_model = {}
    zone_identity_model['zone'] = zoneName

    route_prototype_model = {
        'action': 'delegate',
        'destination': '192.168.3.0/24',
        'name': 'my-route-2',
        'next_hop': route_next_hop_prototype_model,
        'zone': zone_identity_model
    }
    response = service.create_vpc_routing_table(
        vpc_id=vpc_id,
        name=generate_name('my-route'),
        routes=[route_prototype_model],
    )
    return response
# --------------------------------------------------------
# delete_vpc_routing_table()
# --------------------------------------------------------


def delete_vpc_routing_table(service, vpc_id, id):
    response = service.delete_vpc_routing_table(vpc_id, id)
    return response

# --------------------------------------------------------
# get_vpc_routing_table()
# --------------------------------------------------------


def get_vpc_routing_table(service, vpc_id, id):
    response = service.get_vpc_routing_table(vpc_id, id)
    return response

# --------------------------------------------------------
# update_vpc_routing_table()
# --------------------------------------------------------


def update_vpc_routing_table(service, vpc_id, id):
    routing_table_patch_model = {}
    routing_table_patch_model['name'] = generate_name("routing-table")
    response = service.update_vpc_routing_table(vpc_id, id,
                                                routing_table_patch=routing_table_patch_model)
    return response

# --------------------------------------------------------
# list_vpc_routing_table_routes()
# --------------------------------------------------------


def list_vpc_routing_table_routes(service, vpc_id, routing_table_id):
    response = service.list_vpc_routing_table_routes(
        vpc_id=vpc_id, routing_table_id=routing_table_id)
    return response

# --------------------------------------------------------
# create_vpc_routing_table_route()
# --------------------------------------------------------


def create_vpc_routing_table_route(service, vpc_id, routing_table_id, zoneName):
    route_next_hop_prototype_model = {'address': '192.168.3.4'}

    zone_identity_model = {}
    zone_identity_model['name'] = zoneName

    response = service.create_vpc_routing_table_route(
        vpc_id=vpc_id,
        routing_table_id=routing_table_id,
        destination='192.168.3.0/24',
        next_hop=route_next_hop_prototype_model,
        zone=zone_identity_model,
        action='delegate',
        name=generate_name('my-route'),
    )
    return response
# --------------------------------------------------------
# delete_vpc_routing_table_route()
# --------------------------------------------------------


def delete_vpc_routing_table_route(service, vpc_id, routing_table_id, id):
    response = service.delete_vpc_routing_table_route(
        vpc_id, routing_table_id, id)
    return response

# --------------------------------------------------------
# get_vpc_routing_table_route()
# --------------------------------------------------------


def get_vpc_routing_table_route(service, vpc_id, routing_table_id, id):
    response = service.get_vpc_routing_table_route(
        vpc_id, routing_table_id, id)
    return response

# --------------------------------------------------------
# update_vpc_routing_table()
# --------------------------------------------------------


def update_vpc_routing_table_route(service, vpc_id, table_id, id):
    route_patch_model = {}
    route_patch_model['name'] = generate_name("route")
    response = service.update_vpc_routing_table_route(vpc_id, table_id, id,
                                                      route_patch=route_patch_model)
    return response

# --------------------------------------------------------
# dedicated host
# --------------------------------------------------------


def list_dedicated_host_groups(service):
    response = service.list_dedicated_host_groups()
    return response


def create_dedicated_host_group(service):
    zone_identity_model = {}
    zone_identity_model['name'] = store['zone']

    response = service.create_dedicated_host_group(
        class_='mx2',
        family='balanced',
        zone=zone_identity_model,
        name='my-dedicated-host',
    )
    return response


def get_dedicated_host_group(service, id):
    get_dedicated_host_group_response = service.get_dedicated_host_group(id)
    return get_dedicated_host_group_response


def update_dedicated_host_group(service, id):

    dedicated_host_group_patch_model = {'name': 'my-host-group-modified'}

    update_dedicated_host_group_response = service.update_dedicated_host_group(
        id,
        dedicated_host_group_patch=dedicated_host_group_patch_model)
    return update_dedicated_host_group_response


def list_dedicated_host_profiles(service):
    list_dedicated_host_profiles_response = service.list_dedicated_host_profiles()
    return list_dedicated_host_profiles_response


def get_dedicated_host_profile(service, name):
    get_dedicated_host_profile_response = service.get_dedicated_host_profile(
        name)
    return get_dedicated_host_profile_response


def list_dedicated_hosts(service):
    list_dedicated_hosts_response = service.list_dedicated_hosts()
    return list_dedicated_hosts_response


def create_dedicated_host(service, profileName, groupId):
    dedicated_host_profile_identity_model = {}
    dedicated_host_profile_identity_model['name'] = profileName

    # Construct a dict representation of a DedicatedHostGroupIdentityById model
    dedicated_host_group_identity_model = {
        'id': groupId
    }

    # Construct a dict representation of a DedicatedHostPrototypeDedicatedHostByGroup model
    dedicated_host_prototype_model = {
        'name': 'my-host',
        'profile': dedicated_host_profile_identity_model,
        'group': dedicated_host_group_identity_model
    }

    create_dedicated_host_response = service.create_dedicated_host(
        dedicated_host_prototype=dedicated_host_prototype_model)
    return create_dedicated_host_response


def get_dedicated_host(service, id):
    get_dedicated_host_response = service.get_dedicated_host(id)
    return get_dedicated_host_response


def update_dedicated_host(service, id):
    dedicated_host_patch_model = {
        'name': 'my-host'
    }
    update_dedicated_host_response = service.update_dedicated_host(
        id, dedicated_host_patch=dedicated_host_patch_model)
    return update_dedicated_host_response


def delete_dedicated_host_group(service, id):
    delete_dedicated_host_group_response = service.delete_dedicated_host_group(
        id)
    return delete_dedicated_host_group_response


def delete_dedicated_host(service, id):
    delete_dedicated_host_response = service.delete_dedicated_host(id)
    return delete_dedicated_host_response



# --------------------------------------------------------
# placement groups
# --------------------------------------------------------


def create_placement_group(service, name):
    placement_group = service.create_placement_group(
        strategy='host_spread',
        name=name,
    )
    return placement_group

def list_placement_groups(service):
    placement_group_collection = service.list_placement_groups()
    return placement_group_collection

def get_placement_group(service, pgid):
    placement_group = service.get_placement_group(pgid)
    return placement_group

def update_placement_group(service, pgid, name):
    placement_group_patch_model = {
    'name': name
    }

    placement_group = service.update_placement_group(
        pgid,
        placement_group_patch=placement_group_patch_model
    )
    return placement_group

def delete_placement_group(service, pgid):
    response = service.delete_placement_group(pgid)
    return response


# --------------------------------------------------------
# Utils
# --------------------------------------------------------


def generate_name(r_type):
    return "psdk-" + namegenerator.gen() + "-" + r_type


def assertListResponse(output, rType):
    response = output.get_result()
    assert output.status_code == 200
    assert response[rType] is not None

#


def assertGetPatchResponse(output):
    response = output.get_result()
    assert output.status_code == 200
    # assert response['name'] is not None
    assert response['id'] is not None


def assertCreateResponse(output):
    response = output.get_result()
    assert output.status_code == 201
    assert response['name'] is not None
    assert response['id'] is not None


def assertDeleteResponse(output):
    response = output.get_result()
    assert output.status_code == 204
