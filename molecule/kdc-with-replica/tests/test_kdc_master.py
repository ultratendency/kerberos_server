import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('kdc_master')

kdc_replica_1 = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('kdc_replica')[0]


@pytest.mark.parametrize('svc', [
  'krb5kdc',
  'kadmin'
])
def test_services(host, svc):
    service = host.service(svc)

    assert service.is_running
    assert service.is_enabled


def test_kprop_kdump_file_written(host):
    kprop_kdump_file = host.file("/var/kerberos/krb5kdc/slave_datatrans")

    assert kprop_kdump_file.exists
    assert kprop_kdump_file.user == 'root'
    assert kprop_kdump_file.group == 'root'
    assert oct(kprop_kdump_file.mode) == '0o600'


@pytest.mark.parametrize('content', [
    "Database propagation to "+kdc_replica_1+": SUCCEEDED",
])
def test_kprop_kdc_replica_sync_successful(host, content):
    kprop_kdc_replica_sync_log = host.file("/var/log/kprop_kdc_replica_sync.log")

    assert kprop_kdc_replica_sync_log.exists
    assert kprop_kdc_replica_sync_log.contains(content)
