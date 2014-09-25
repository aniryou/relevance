#!/bin/bash

set -e

#currently indexs amazon only records, uncomment else part below for other stores
#columns: id,imageurl,product_title,breadcrumb,catpred,ignore1,ignore2,raw_catpred,ignore3,ignore4
COLLECTION=$1
SOLR_FIELDS=$2
for file in `ls $3/*`
do
	file_abs=$(readlink -f $file)
	echo "indexing $file_abs"
	curl "http://localhost:8983/solr/$COLLECTION/update/csv?commit=true&fieldnames=id,imageurl,product_title,c0,cl,raw_catpred,sku,store_id&separator=%09&escape=%1B&stream.file=$file_abs&stream.contentType=text/plain;charset=utf-8"
done
rm -rf $1/*
curl "http://localhost:8983/solr/relevance/update/csv?commit=true"
