#!/bin/bash
PORTAL_FILE=opendataportals.ttl
SPARQL_DIR=sparql
CATALOG_DIR=catalog
PORTAL_DIR="${PORTAL_DIR:=ckanportals}"
CATALOG_NS="${CATALOG_NS:=http://mclient-project.github.io/catalog/}"
SOURCE_NS="${SOURCE_NS:=http://aksw.org/mclient/}"
export CATALOG_NS
export PORTAL_FILE 
export SOURCE_NS

# create a meta-catalog if it does not exist
# [ -f meta.ttl ] || `touch meta.ttl && sparql-integrate prefixes.ttl --io=meta.ttl --w=trig/pretty $SPARQL_DIR/catalog-entry.sparql spo.sparql`
for portal in $PORTAL_DIR/*.ttl
do
	echo $portal
	if [ -s "$portal" ]
	then
		rapper -i turtle -o turtle $portal > /dev/null 2> $portal-parse
		export PORTAL=`echo $(basename $portal .ttl) | tr '_' ' '`
   		sparql-integrate --io=$portal --w=trig/pretty cwd=$(pwd) prefixes.ttl $SPARQL_DIR/catalog-rules/*.sparql spo.sparql
		cp $portal $CATALOG_DIR/toLoad/`echo $(basename $portal)`
	else
   		echo " file does not exist, or is empty "
	fi
done
#mv meta.ttl $PORTAL_DIR/meta.ttl 
#find $PORTAL_DIR -exec rapper -e -i guess -o ntriples {} \; | sort -u | rapper -i ntriples -o turtle - http://www.example.org/ > $CATALOG_FILE


