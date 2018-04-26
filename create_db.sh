#!/bin/bash
sed -i 's/127.0.0.1/0.0.0.0/g' /etc/postgresql/9.5/main/pg_hba.conf
sed -i 's/32/0/g' /etc/postgresql/9.5/main/pg_hba.conf
sed -i 's/peer/trust/g' /etc/postgresql/9.5/main/pg_hba.conf
sed -i 's/md5/trust/g' /etc/postgresql/9.5/main/pg_hba.conf
sed -i '/listen_address/s/^#//g' /etc/postgresql/9.5/main/postgresql.conf
sed -i '/unix_socket_permissions/s/^#//g' /etc/postgresql/9.5/main/postgresql.conf
sed -i 's/localhost/*/g' /etc/postgresql/9.5/main/postgresql.conf
service postgresql restart

