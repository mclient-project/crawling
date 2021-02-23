#!/bin/bash
url="https://mcloud.de/export/datasets?page=1&pageSize=10000"
new_url="https://mcloud.de/"
curl $url --output $TARGET/mcloud.rdf
rapper -i rdfxml -o ntriples -I $new_url $TARGET/mcloud.rdf > $TARGET/mcloud.nt
rapper -i ntriples -o turtle $TARGET/mcloud.nt > $TARGET/mcloud.ttl
rm $TARGET/mcloud.rdf
rm $TARGET/mcloud.nt
touch $TARGET/mcloud-meta.ttl
sparql-integrate --io=$TARGET/mcloud-meta.ttl --w=trig/pretty cwd=$(pwd) prefixes.ttl $SPARQL_DIR/add-mcloud.sparql spo.sparql
