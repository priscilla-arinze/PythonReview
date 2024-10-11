#!/bin/bash

. ./get-postgres-secrets.sh

# echo $POSTGRESUSERNAME
# echo $POSTGRESPASSWORD
# echo $POSTGRESHOST
# echo $POSTGRESPORT

## EXTRACT
echo "Extracting data..."

# Extract the columns 1 (timestamp), 2 (latitude), 3 (longitude) and 4 (visitorid)
cut -d"#" -f1-4 ./web-server-access-log.txt > extracted-data.txt

## TRANSFORM
echo "Transforming data..."

# Convert extracted data to CSV (',' delimited)
tr "#" "," < extracted-data.txt > transformed-data.csv

## LOAD
echo "Loading data to Postgres database..."
# export PGPASSWORD=$POSTGRESPASSWORD

# echo "\c etl_exercises;\COPY access_logs FROM './transformed-data.csv' DELIMITERS ',' CSV HEADER;" | psql --username=postgres --host=localhost