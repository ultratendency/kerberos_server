import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('kdc_replica')

kdc_master_1 = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('kdc_master')[0]


@pytest.mark.parametrize('svc', [
  'krb5kdc',
  'kprop'
])
def test_services(host, svc):
    service = host.service(svc)

    assert service.is_running
    assert service.is_enabled


def test_kpropd_acl(host):
    kpropd_acl = host.file("/var/kerberos/krb5kdc/kpropd.acl")

    assert kpropd_acl.exists
    assert kpropd_acl.is_file
    assert kpropd_acl.user == 'root'
    assert kpropd_acl.group == 'root'


@pytest.mark.parametrize('content', [
    "host/"+kdc_master_1+"@",
])
def test_kpropd_acl_content(host, content):
    kpropd_acl = host.file("/var/kerberos/krb5kdc/kpropd.acl")

    assert kpropd_acl.contains(content)
