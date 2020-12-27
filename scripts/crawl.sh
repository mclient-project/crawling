#!/bin/bash
portals=`sparql-integrate --jq opendataportals-2.ttl --w=trig/pretty $SPARQL_DIR/portal-by-type.sparql spo.sparql | jq -c '.[]'`
echo "$portals" | while read portalline; do
	portal_url=`echo $portalline | jq -r '.url'`
	portal_label=`echo $portalline | jq -r '.label' | tr ' ' '_'`
	portal=$TARGET/$portal_label.ttl
	dcat import $PORTAL_TYPE --url $portal_url --all > $portal
	if [ -s $portal ]
		then
			rapper -i turtle -o turtle $portal > /dev/null 2> $portal-parse
			if ! grep -q ERROR $portal-parse; then
				export PORTAL=`echo $(basename $portal .ttl) | tr '_' ' '`
				sparql-integrate --io=$portal --w=trig/pretty cwd=$(pwd) prefixes.ttl $SPARQL_DIR/catalog-rules/*.sparql spo.sparql
			else
				rm $portal && echo '***WARNING: Could not parse file for portal '$portal'***'
		  	fi
		  	rm $portal-parse
		else
			echo " file does not exist, or is empty "
	fi
done
