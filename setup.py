# Copyright 2014 DreamHost, LLC
#
# Author: DreamHost, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


from setuptools import setup, find_packages


setup(
    name='akanda-quantum',
    version='0.1.4',
    description='OpenStack L3 User-Facing REST API for Quantum',
    author='DreamHost',
    author_email='dev-community@dreamhost.com',
    url='http://github.com/dreamhost/akanda',
    license='BSD',
    install_requires=[
        'mock'
    ],
    namespace_packages=['akanda'],
    packages=find_packages(exclude=['test', 'smoke']),
    include_package_data=True,
    zip_safe=False,
)
