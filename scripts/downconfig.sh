#!/bin/bash

assert_params() {
        if [ "$1" -lt 3 ]; then echo "usage: $0 zkhost configdir_local configname"; exit; fi
}

assert_params $#

java -classpath "../lib/ext/*" org.apache.solr.cloud.ZkCLI -cmd downconfig -zkhost $1 -confdir $2 -confname $3
