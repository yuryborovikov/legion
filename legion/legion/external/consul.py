#
#    Copyright 2017 EPAM Systems
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
"""
Consul client
"""

import consul


def register_model_service(consul_host, consul_port, service, host, port):
    """
    Register application in Consul

    :param consul_host: Consul address
    :type consul_host: str
    :param consul_port: Consul port
    :type consul_port: int
    :param service: Service name
    :type service: str
    :param host: Consul address
    :type host: str
    :param port: Consul port
    :type port: int
    :return: None
    """
    client = consul.Consul(host=consul_host, port=consul_port)

    print('Registering model %s located at %s:%d on http://%s:%s' % (service, host, port, consul_host, consul_port))

    client.agent.service.register(
        service,
        address=host,
        port=port,
        tags=['legion', 'model'],
        check=consul.Check.http('http://%s:%d/healthcheck' % (host, port), '2s')
    )
