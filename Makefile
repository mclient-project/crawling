SPARQL_DIR=sparql
TARGET=target
PORTAL_FILE=opendataportals-2.ttl
CATALOG_NS=http://mclient-project.github.io/catalog/
SOURCE_NS=http://aksw.org/mclient/

export SPARQL_DIR
export TARGET
export PORTAL_FILE
export CATALOG_NS
export SOURCE_NS

SCRIPTS_DIR=scripts

CATALOG_DIR=catalog
CATALOG_FILE=$(CATALOG_DIR)/catalog.ttl
CATALOG_LOAD_DIR=$(CATALOG_DIR)/toLoad

CWD = $(shell pwd)

SELF := $(dir $(lastword $(MAKEFILE_LIST)))

SHELL := /bin/bash

## crawl dkan portals
crawl-dkan: target
	export PORTAL_TYPE="dkan"; \
	echo $(CATALOG_NS); \
	chmod +x $(SELF)/$(SCRIPTS_DIR)/crawl.sh && $(SELF)/$(SCRIPTS_DIR)/crawl.sh

## crawl ckan portals
crawl-ckan: target
	export PORTAL_TYPE="ckan"; \
	chmod +x $(SELF)/$(SCRIPTS_DIR)/crawl.sh && $(SELF)/$(SCRIPTS_DIR)/crawl.sh

## crawl the bielefeld portal separately
crawl-bielefeld: target
	export PORTAL="Bielefeld"; \
	chmod +x $(SELF)/$(SCRIPTS_DIR)/crawl-bielefeld.sh && $(SELF)/$(SCRIPTS_DIR)/crawl-bielefeld.sh
##
curl-catalogs: target
	chmod +x $(SELF)/$(SCRIPTS_DIR)/catalog.sh && $(SELF)/$(SCRIPTS_DIR)/catalog.sh

curl-big-cat: target
	chmod +x $(SELF)/$(SCRIPTS_DIR)/big-cat.sh && $(SELF)/$(SCRIPTS_DIR)/big-cat.sh

curl-mcloud: target
	chmod +x $(SELF)/$(SCRIPTS_DIR)/mcloud.sh && $(SELF)/$(SCRIPTS_DIR)/mcloud.sh

#crawl-all: crawl-ckan crawl-dkan crawl-bielefeld

#curl-all: curl-catalogs curl-govdata

#get-data: crawl-all curl-all

generate-cat:
	cp target/*.ttl $(CATALOG_LOAD_DIR)/
	find $(CATALOG_LOAD_DIR)/ -exec rapper -e -i guess -o ntriples {} \; | sort -u | rapper -i ntriples -o turtle - http://www.example.org/ > $(CATALOG_FILE)

deploy-cat:
	git add $(CATALOG_FILE) && git commit -m 'update catalog' && git push

## create the target folder for crawled data
target:
	[ -d $(TARGET) ] || mkdir -p $(TARGET) 

clean:
	rm -rf target
