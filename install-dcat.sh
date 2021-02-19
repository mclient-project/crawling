#!/bin/bash
git clone https://github.com/SmartDataAnalytics/dcat-suite.git
git checkout develop
mvn clean install -DskipTests=true
./reinstall-debs.sh
cp /usr/bin/dcat /usr/local/bin/dcat 
