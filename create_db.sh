#!/bin/bash 

export PSQL_HOME=/Library/PostgreSQL/10.3
export PATH=/Library/PostgreSQL/10.3/bin:$PATH
export PGPASSWORD=cjmash
createdb test_db${BUILD_NUMBER} --owner=cjmash --username=postgres

