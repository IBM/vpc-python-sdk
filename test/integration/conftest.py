# coding: utf-8

# (C) Copyright IBM Corp. 2020.
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
import pytest
import os
import os.path
from ibm_vpc.vpc_classic_v1 import VpcClassicV1
from ibm_vpc.vpc_v1 import VpcV1

# Read config file
configFile = 'vpc.env'

def loadConfigFile():
    if os.path.exists(configFile):
        os.environ['IBM_CREDENTIALS_FILE'] = configFile
    else:
        pytest.skip('External configuration not available, skipping...')

@pytest.fixture(scope="session")
def createGen1Service():
    loadConfigFile()
    service = VpcClassicV1.new_instance()
    headers = {
        'Accept': 'application/json'
    }
    service.set_default_headers(headers)
    print('Setup complete.')
    return service

@pytest.fixture(scope="session")
def createGen2Service():
    loadConfigFile()
    service = VpcV1.new_instance()
    headers = {
        'Accept': 'application/json'
    }
    service.set_default_headers(headers)
    print('Setup complete.')
    return service

def pytest_addoption(parser):
    parser.addoption("--env", action="store", help="Run test on dev environment")

@pytest.fixture()
def env(request):
    val = request.config.getoption("--env")
    if val == 'true':
        print('Test on dev env -', val)
        return True
    return False

