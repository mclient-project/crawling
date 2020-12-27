#!/bin/bash
dcat import dkan --url 'https://open-data.bielefeld.de/' --all --alt > $TARGET/Bielefeld.ttl
sparql-integrate --io=$TARGET/Bielefeld.ttl --w=trig/pretty cwd=$(pwd) prefixes.ttl $SPARQL_DIR/catalog-rules/*.sparql spo.sparql
