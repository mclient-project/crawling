#!/bin/bash
TIMES=68
OFFSET=1
for (( i=1; i<=$TIMES; i++ )) ;
do
	sed -e "s#\$MAPPING#$OFFSET#" keyword.sparql > tmp-mapping.sparql
	queryText=`cat tmp-mapping.sparql`
	cat tmp-mapping.sparql
	curl -H "Accept: text/csv" --data-urlencode 'query@tmp-mapping.sparql' http://localhost:8890/sparql > data/data$OFFSET.csv
	let "OFFSET=$OFFSET+10000"
	echo $OFFSET
done
rm tmp-mapping.sparql
	

