#!/bin/bash
# PORTAL_TYPE defaults to ckan
PORTAL_TYPE="${PORTAL_TYPE:=ckan}"
export PORTAL_TYPE
SPARQL_DIR=sparql
echo $PORTAL_TYPE
[ -d $PORTAL_TYPE ] || mkdir $PORTAL_TYPE
portals=`sparql-integrate --jq opendataportals.ttl --w=trig/pretty $SPARQL_DIR/portal-by-type.sparql spo.sparql | jq -c '.[]'`
echo "$portals" | while read portalline; do
	portal_url=`echo $portalline | jq -r '.url'`
	portal_label=`echo $portalline | jq -r '.label' | tr ' ' '_'` 
	dcat import $PORTAL_TYPE --url $portal_url --all > $PORTAL_DIR/$portal_label.ttl
done



