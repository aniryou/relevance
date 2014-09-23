#!/bin/bash

for file in `ls $1/*`
do
file_abs=$(readlink -f $file)
echo "indexing $file_abs"
curl "http://localhost:8983/solr/relevance/update/csv?commit=true&fieldnames=id,url,imageurl,product_title,c0,cl&separator=%09&escape=%1B&stream.file=$file_abs&stream.contentType=text/plain;charset=utf-8"
done
curl "http://localhost:8983/solr/relevance/update/csv?commit=true"
