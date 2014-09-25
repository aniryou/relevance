#!/bin/bash

set -e

TEMP='/tmp/relevanceconf'
CONF_SOLRHOST='../conf/solrhost.txt'
CONF_ZKHOST='../conf/zkhost.txt'
CONF_COLLECTION='../conf/collection.txt'
SOLR_HOSTS=$(cat $CONF_SOLRHOST)
ZKHOSTS=$(cat $CONF_ZKHOST)
COLLECTION=$(cat $CONF_COLLECTION | awk 'NR==1{print}')
NUM_SHARDS=$(cat $CONF_COLLECTION | awk 'NR==2{print}')
REPLICATION_FACTOR=$(cat $CONF_COLLECTION | awk 'NR==3{print}')

if [ -d "$TEMP" ]; then rm -rf $TEMP; fi
mkdir $TEMP

cp -r ../conf/solr-4.6.0/* $TEMP
cp ../conf/$COLLECTION/* $TEMP

./upconfig.sh \"$ZKHOSTS\" $TEMP $COLLECTION
solr_host=$(echo $SOLR_HOSTS | tr ' ' '\n' | head -1)
curl "http://$solr_host:8983/solr/admin/collections?action=RELOAD&name=$COLLECTION"
