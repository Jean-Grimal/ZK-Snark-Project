#!/bin/bash

BEFORE=$(($(date +%s%N)/1000000))

zokrates compile -i $1 -o $2
zokrates setup -i $2 -p $3 -v $4
zokrates export-verifier -i $4 -o $5

AFTER=$(($(date +%s%N)/1000000))
ELAPSED=$(($AFTER-$BEFORE))
echo $ELAPSED