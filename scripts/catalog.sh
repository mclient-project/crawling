#!/bin/bash
portals=`sparql-integrate --jq opendataportals-2.ttl --w=trig/pretty $SPARQL_DIR/portal-by-catalog.sparql spo.sparql | jq -c '.[]'`
echo "$portals" | while read portalline; do
	portal_url=`echo $portalline | jq -r '.url.id'`
	portal_label=`echo $portalline | jq -r '.label' | tr ' ' '_'`
	curl $portal_url --output $TARGET/$portal_label.rdf
	rapper -i rdfxml -o turtle $TARGET/$portal_label.rdf > $TARGET/$portal_label.ttl
	rm $TARGET/$portal_label.rdf
	sparql-integrate --io=$TARGET/$portal_label.ttl --w=trig/pretty cwd=$(pwd) prefixes.ttl $SPARQL_DIR/catalog-rules/04-add-to-meta.sparql spo.sparql
done
