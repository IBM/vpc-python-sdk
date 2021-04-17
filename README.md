[![Build Status](https://travis-ci.com/IBM/vpc-python-sdk.svg?branch=master)](https://travis-ci.com/IBM/vpc-python-sdk)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![semantic-release](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg)](https://github.com/semantic-release/semantic-release)

# IBM Cloud Virtual Private Cloud (VPC) Python SDK Version 0.5.1

Python client library to interact with various [IBM Cloud Virtual Private Cloud (VPC) Service APIs](https://cloud.ibm.com/apidocs/vpc).

This SDK uses [Semantic Versioning](https://semver.org), and as such there may be backward-incompatible changes for any new `0.y.z` version.

**Note** As IBM continues to invest and innovate on the IBM Cloud Virtual Private Cloud (gen 2 compute) infrastructure, we're focusing on delivering maximum value in a single VPC Infrastructure platform. To support this effort, generation 1 compute infrastructure is being deprecated. The end of service date is 26 February 2021. For more information, see the [Start your migration](https://www.ibm.com/cloud/blog/announcements/start-your-vpc-gen1-to-vpc-gen2-migration) blog.

## Table of Contents

<!--
  The TOC below is generated using the `markdown-toc` node package.

      https://github.com/jonschlinkert/markdown-toc

  You should regenerate the TOC after making changes to this file.

      npx markdown-toc -i README.md
  -->

<!-- toc -->

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Using the SDK](#using-the-sdk)
- [Setting up VPC service](#setting-up-vpc-service)
- [Setting up VPC on Classic service](#setting-up-vpc-on-classic-service)
- [Questions](#questions)
- [Issues](#issues)
- [Open source @ IBM](#open-source--ibm)
- [Contributing](#contributing)
- [License](#license)

<!-- tocstop -->

## Overview

The IBM Cloud Virtual Private Cloud (VPC) Python SDK allows developers to programmatically interact with the following
IBM Cloud services:

Service Name | Imported Class Name
--- | ---
[VPC](https://cloud.ibm.com/apidocs/vpc) | VpcV1
[VPC Gen 1](https://cloud.ibm.com/apidocs/vpc-on-classic) | VpcClassicV1

## Prerequisites

[ibm-cloud-onboarding]: https://cloud.ibm.com/registration

* An [IBM Cloud][ibm-cloud-onboarding] account.
* An IAM API key to allow the SDK to access your account. Create one [here](https://cloud.ibm.com/iam/apikeys).
* Python 3.5.3 or above.

## Installation

To install, use `pip` or `easy_install`:

```bash
pip install --upgrade "ibm-vpc>=0.5.1"
```

or

```bash
easy_install --upgrade "ibm-vpc>=0.5.1"
```

## Using the SDK
For general SDK usage information, please see [this link](https://github.com/IBM/ibm-cloud-sdk-common/blob/master/README.md)

## Setting up VPC service
```python
from ibm_vpc import VpcV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core import ApiException

authenticator = IAMAuthenticator("YOUR_IBMCLOUD_API_KEY")
service = VpcV1('2020-06-02', authenticator=authenticator)

#  Listing VPCs
print("List VPCs")
try:
    vpcs = service.list_vpcs().get_result()['vpcs']
except ApiException as e:
  print("List VPC failed with status code " + str(e.code) + ": " + e.message)
for vpc in vpcs:
    print(vpc['id'], "\t",  vpc['name'])

#  Listing Subnets
print("List Subnets")
try:
    subnets = service.list_subnets().get_result()['subnets']
except ApiException as e:
  print("List subnets failed with status code " + str(e.code) + ": " + e.message)
for subnet in subnets:
    print(subnet['id'], "\t",  subnet['name'])

#  Listing Instances
print("List Instances")
try:
    instances = service.list_instances().get_result()['instances']
except ApiException as e:
  print("List instances failed with status code " + str(e.code) + ": " + e.message)
for instance in instances:
    print(instance['id'], "\t",  instance['name'])

instanceId = instances[0]['id']
instanceName = instances[0]['name']

#  Updating Instance
print("Updated Instance")
try:
    newInstanceName = instanceName + "-1"
    instance = service.update_instance(
        id=instanceId,
        name=newInstanceName,
    ).get_result()
except ApiException as e:
    print("Update instance failed with status code " + str(e.code) + ": " + e.message)
print(instance['id'], "\t",  instance['name'])

```


## Setting up VPC on Classic service
```python
from ibm_vpc import VpcClassicV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core import ApiException

authenticator = IAMAuthenticator("YOUR_IBMCLOUD_API_KEY")
service = VpcClassicV1('2020-06-02', authenticator=authenticator)

#  Listing VPCs
print("List VPCs")
try:
    vpcs = service.list_vpcs().get_result()['vpcs']
except ApiException as e:
  print("List VPC failed with status code " + str(e.code) + ": " + e.message)
for vpc in vpcs:
    print(vpc['id'], "\t",  vpc['name'])
print("\n")

#  Listing Subnets
print("List Subnets")
try:
    subnets = service.list_subnets().get_result()['subnets']
except ApiException as e:
  print("List subnets failed with status code " + str(e.code) + ": " + e.message)
for subnet in subnets:
    print(subnet['id'], "\t",  subnet['name'])

#  Listing Instances
print("List Instances")
try:
    instances = service.list_instances().get_result()['instances']
except ApiException as e:
  print("List instances failed with status code " + str(e.code) + ": " + e.message)
for instance in instances:
    print(instance['id'], "\t",  instance['name'])

instanceId = instances[0]['id']
instanceName = instances[0]['name']

#  Updating Instance
print("Updated Instance")
try:
    newInstanceName = instanceName + "-1"
    instance = service.update_instance(
        id=instanceId,
        name=newInstanceName,
    ).get_result()
except ApiException as e:
  print("Update instance failed with status code " + str(e.code) + ": " + e.message)
print(instance['id'], "\t",  instance['name'])

```

## Questions

If you are having difficulties using this SDK or have a question about the IBM Cloud services,
please ask a question
[Stack Overflow](http://stackoverflow.com/questions/ask?tags=ibm-cloud).

## Issues
If you encounter an issue with the project, you are welcome to submit a
[bug report](https://github.com/IBM/vpc-python-sdk/issues).
Before that, please search for similar issues. It's possible that someone has already reported the problem.

## Open source @ IBM
Find more open source projects on the [IBM Github Page](http://ibm.github.io/)

## Contributing
See [CONTRIBUTING](https://github.com/IBM/vpc-python-sdk/blob/master/CONTRIBUTING.md).

## License

This SDK is released under the Apache 2.0 license.
The license's full text can be found in [LICENSE](https://github.com/IBM/vpc-python-sdk/blob/master/LICENSE).
