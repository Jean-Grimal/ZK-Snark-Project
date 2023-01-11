#!/bin/bash
RM='/bin/rm'
FTP='/usr/bin/ftp'
DATE='/bin/date'

BEFORE=$(($(date +%s%N)/1000000))

zokrates compute-witness -i $1 -a $2
zokrates generate-proof -i $1 -p $3

AFTER=$(($(date +%s%N)/1000000))
ELAPSED=$(($AFTER-$BEFORE))
echo $ELAPSED
