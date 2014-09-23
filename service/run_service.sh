#!/bin/bash

#TODO:
# Change this script to support start/stop/status messages
BASEDIR=$(dirname $0)

cd $(dirname {BASEDIR})
echo $(dirname {BASEDIR})
export TAXONOMY_URL="http://cam-dev01.production-mr.indix.tv:21007/api/classify"
export SOLR_URL="http://solr01.perf.indix.tv:8983/solr/relevance/select?"
export SERVER_TYPE="${SERVER_TYPE:-gevent}"

python2.7 -m bottle --server ${SERVER_TYPE} --bind 0.0.0.0:21008 'Service:app'
