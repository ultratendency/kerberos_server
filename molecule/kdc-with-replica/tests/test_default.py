import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


# tests on each kdc
def test_kdc_conf(host):
    kdc_conf = host.file("/var/kerberos/krb5kdc/kdc.conf")

    assert kdc_conf.exists
    assert kdc_conf.is_file
    assert kdc_conf.user == 'root'
    assert kdc_conf.group == 'root'
    assert oct(kdc_conf.mode) == '0o600'


def test_krb5_conf(host):
    krb5_conf = host.file("/etc/krb5.conf")

    assert krb5_conf.exists
    assert krb5_conf.is_file
    assert krb5_conf.user == 'root'
    assert krb5_conf.group == 'root'
    assert oct(krb5_conf.mode) == '0o644'
