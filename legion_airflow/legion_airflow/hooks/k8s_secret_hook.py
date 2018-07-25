"""K8S Connections hook package."""
import os
import json
import base64

from airflow import LoggingMixin
from airflow.hooks.base_hook import BaseHook
from airflow.models import Connection
from kubernetes import client, config
from kubernetes.client.rest import ApiException

# from legion.k8s import K8SConfigMapStorage


class K8SSecretHook(BaseHook):
    """Hook for looking connections/credentials in K8S first than Airflow."""\

    LOG = LoggingMixin().log
    CONNECTIONS_SECRET = 'airflow-connections'

    @classmethod
    def get_connection(cls, conn_id: str):
        """
        Return connection by connection id.

        :param conn_id: connection id
        :type conn_id: str
        :return: :py:class:`airflow.models.Connection` -- connection
        """
        try:
            conf = config.load_incluster_config()
        except config.config_exception.ConfigException:
            conf = config.load_kube_config()
        core_api = client.CoreV1Api()
        namespace = os.environ['NAMESPACE']
        try:
            # secret = K8SConfigMapStorage(name=cls.CONNECTIONS_CONFIG_MAP, namespace=namespace)
            secret = core_api.read_namespaced_secret(name=cls.CONNECTIONS_SECRET, namespace=namespace)
            if conn_id in secret.data:
                conn_data = secret.data.get(conn_id)
                if conn_data:
                    conn_data = base64.b64decode(conn_data).decode('utf-8')
                    conn = json.loads(conn_data)
                    cls.LOG.info("Return connection {} from K8S secret {}".format(conn_id, cls.CONNECTIONS_SECRET))
                    cls.LOG.info("{}-{}-{}-{}".format(conn['conn_id'], conn['conn_type'], conn['login'], conn['extra']))
                    return Connection(conn_id=conn['conn_id'], conn_type=conn['conn_type'], host=conn['host'],
                                      login=conn['login'], password=conn['password'], schema=conn['schema'],
                                      port=conn['port'], extra=conn['extra'], uri=conn['uri'])
            else:
                cls.LOG.info("{} not found in K8S secrets {}".format(conn_id, cls.CONNECTIONS_SECRET))
        except ApiException as ex:
            cls.LOG.info("Can't use connections K8S secret {} because of {}".format(cls.CONNECTIONS_SECRET, str(ex)))
        return super().get_connection(conn_id)
