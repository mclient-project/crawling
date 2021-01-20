#!/bin/bash
url="https://mcloud.de/export/datasets?page=1&pageSize=10000"
curl $url --output $TARGET/mcloud.rdf
rapper -i rdfxml -o turtle $TARGET/mcloud.rdf > $TARGET/mcloud.ttl
rm $TARGET/mcloud.rdf
touch $TARGET/mcloud-meta.ttl
sparql-integrate --io=$TARGET/mcloud-meta.ttl --w=trig/pretty cwd=$(pwd) prefixes.ttl $SPARQL_DIR/add-mcloud.sparql spo.sparql
