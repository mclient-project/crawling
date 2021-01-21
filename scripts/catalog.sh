#!/bin/bash
portals=`sparql-integrate --jq opendataportals-2.ttl --w=trig/pretty $SPARQL_DIR/portal-by-catalog.sparql spo.sparql | jq -c '.[]'`
echo "$portals" | while read portalline; do
	portal_url=`echo $portalline | jq -r '.url.id'`
	echo $portal_url
	portal_label=`echo $portalline | jq -r '.label' | tr ' ' '_'`
	curl $portal_url --output $TARGET/$portal_label.rdf
	new_url=`echo $portal_url | sed 's/catalog.xml//g'`
	echo $new_url
	rapper -i rdfxml -o ntriples -I $new_url $TARGET/$portal_label.rdf > $TARGET/$portal_label.nt
	rapper -i ntriples -o ntriples $TARGET/$portal_label.nt > /dev/null 2> $TARGET/$portal_label-parse
	test=$(cat $TARGET/$portal_label-parse | grep -c "Error")
	echo $portal_label
	echo $test 
	while [ "$test" -gt 0 ]
	do
		line=`cat $TARGET/$portal_label-parse | sed -n '3p' | cut -d ":" -f4 | cut -d " " -f1` 
		echo $line
		sed -i "${line}d" $TARGET/$portal_label.nt
		rapper -i ntriples -o ntriples $TARGET/$portal_label.nt > /dev/null 2> $TARGET/$portal_label-parse
		test=$(cat $TARGET/$portal_label-parse | grep -c "Error")
	done
	rapper -i ntriples -o turtle $TARGET/$portal_label.nt > $TARGET/$portal_label.ttl
	rm $TARGET/$portal_label.rdf
	rm $TARGET/$portal_label-parse
	rm $TARGET/$portal_label.nt
	sparql-integrate --io=$TARGET/$portal_label.ttl --w=trig/pretty cwd=$(pwd) prefixes.ttl $SPARQL_DIR/catalog-rules/04-add-to-meta.sparql spo.sparql
done

