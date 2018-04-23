#!/bin/bash 

export PSQL_HOME=/Library/PostgreSQL/10.3
export PATH=/Library/PostgreSQL/10.3/bin:$PATH
export PGPASSWORD=cjmash
psql -U postgres -c create database test_db

