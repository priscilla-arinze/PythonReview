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

export POSTGRESUSERNAME=${VALUEUSERNAME##*= }
export POSTGRESPASSWORD=${VALUEPASSWORD##*= }
export POSTGRESHOST=${VALUEHOST##*= }
export POSTGRESPORT=${VALUEPORT##*= }