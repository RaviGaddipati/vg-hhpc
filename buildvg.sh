#!/bin/bash
set -x
COUNTER=16000001
COUNTERB=16500000
while [ $COUNTERB -le 52000000 ]
do
	nice ../../vg/vg construct -r ../hs37d5_22.fa -v ../chr22.vcf.gz -R 22:$COUNTER-$COUNTERB -t 8 >"$COUNTER.vg"
	COUNTER=$(($COUNTER+500000))
	COUNTERB=$(($COUNTERB+500000))
done
