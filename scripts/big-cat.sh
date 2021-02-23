#!/bin/bash
#seed='https://ckan.govdata.de/catalog.rdf?page=1'
declare -a seedArr=("https://ckan.govdata.de/catalog.rdf?page=1" )
seedArrLength==${#seedArr[@]}
new_url=https://ckan.govdata.de
for (( i=1; i<${seedArrLength}+1; i++ ));
do
	nextPage=1
	counter=1
	seed=${seedArr[$i-1]}
	name=$(sed -E 's|.*(@\|://)([^:/]+).*|\2|g' <<< $seed)
	echo $name
	while [ $nextPage -eq 1 ]
	do
		curl $seed --output $TARGET/$name-$counter.rdf
		rapper -i rdfxml -o ntriples -I $new_url $TARGET/$name-$counter.rdf > $TARGET/$name-$counter.nt
		rapper -i ntriples -o turtle $TARGET/$name-$counter.nt > $TARGET/$name-$counter.ttl
		rm $TARGET/$name-$counter.rdf
		rm $TARGET/$name-$counter.nt
		seed=`sparql-integrate --w=trig/pretty --jq cwd=$(pwd) prefixes.ttl $TARGET/$name-$counter.ttl sparql/next-page.sparql spo.sparql | jq -r '.[].nextPage'`
		echo $seed
		if [ $counter -eq 1 ]; then
			sparql-integrate --io=$TARGET/$name-$counter.ttl --w=trig/pretty cwd=$(pwd) prefixes.ttl $SPARQL_DIR/catalog-rules/04-add-to-meta.sparql spo.sparql
		fi
		let "counter+=1" ;
		if [ -z $seed ]; then nextPage=0; fi
	done
done
