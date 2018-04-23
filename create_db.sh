#!/bin/bash 
pg_config --version
export PSQL_HOME=/Library/PostgreSQL/10.3
export PATH=/Library/PostgreSQL/10.3/bin:$PATH
export PGPASSWORD=cjmash
echo "we are here "
psql -U postgres -c create database test_db

