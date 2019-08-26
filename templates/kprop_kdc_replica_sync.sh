#!/bin/bash
kdclist="{{ kerberos_server_kdcs[1:] | join(' ') }}"

/sbin/kdb5_util dump /var/kerberos/krb5kdc/slave_datatrans
for kdc in $kdclist
do
    /sbin/kprop -f /var/kerberos/krb5kdc/slave_datatrans $kdc 2>&1 | tee -a /var/log/kprop_kdc_replica_sync.log
done
