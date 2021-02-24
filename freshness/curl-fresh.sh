#!/bin/bash
#PORTAL=govdata
PORTAL=mcloud
CATALOG=https://mcloud.de
#ATALOG=https://ckan.govdata.de
TIMES=1
OFFSET=1
for (( i=1; i<=$TIMES; i++ )) ;
do
	sed -e "s#\$MAPPING#$OFFSET#" fresh.sparql > tmp-mapping.sparql
	sed -e "s#\$URL#$CATALOG#" tmp-mapping.sparql > tmp-mapping-2.sparql
	#cat tmp-mapping.sparql
	curl -H "Accept: text/csv" --data-urlencode 'query@tmp-mapping-2.sparql' http://localhost:8890/sparql > data/$PORTAL/$OFFSET.csv
	let "OFFSET=$OFFSET+10000"
	echo $OFFSET
done
rm tmp-mapping.sparql
rm tmp-mapping-2.sparql
	

