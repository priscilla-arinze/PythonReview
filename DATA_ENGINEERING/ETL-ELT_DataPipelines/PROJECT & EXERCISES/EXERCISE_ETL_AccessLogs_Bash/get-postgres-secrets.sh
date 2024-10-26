#!/bin/bash

SECRETS_FILE=../../../SECRETS.txt
KEYUSERNAME="PostgreSQL Username"
KEYPASSWORD="PostgreSQL Password"
KEYHOST="PostgreSQL Host"
KEYPORT="PostgreSQL Port"

while read -r line; do
    #echo "$line"
    if [[ $line =~ ^$KEYUSERNAME.* ]]; then
        VALUEUSERNAME=$line
    fi

    if [[ $line =~ ^$KEYPASSWORD.* ]]; then
        VALUEPASSWORD=$line
    fi

    if [[ $line =~ ^$KEYHOST.* ]]; then
        VALUEHOST=$line
    fi

    if [[ $line =~ ^$KEYPORT.* ]]; then
        VALUEPORT=$line
    fi
done < $SECRETS_FILE

POSTGRESUSERNAME_NO_TRIM=${VALUEUSERNAME##*= }
POSTGRESPASSWORD_NO_TRIM=${VALUEPASSWORD##*= }
POSTGRESHOST_NO_TRIM=${VALUEHOST##*= }
POSTGRESPORT_NO_TRIM=${VALUEPORT##*= }

export POSTGRESUSERNAME="$(echo -e "${POSTGRESUSERNAME_NO_TRIM}" | tr -d '[:space:]')"
export POSTGRESPASSWORD="$(echo -e "${POSTGRESPASSWORD_NO_TRIM}" | tr -d '[:space:]')"
export POSTGRESHOST="$(echo -e "${POSTGRESHOST_NO_TRIM}" | tr -d '[:space:]')"
export POSTGRESPORT="$(echo -e "${POSTGRESPORT_NO_TRIM}" | tr -d '[:space:]')"