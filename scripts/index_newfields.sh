for file in `ls $1/*`
do
	file_abs=$(readlink -f $file)
	echo "indexing $file_abs"
	#curl "http://localhost:8983/solr/relevance/update/csv?commit=true&fieldnames=id,raw_catpred,store,sku&separator=%09&escape=%1B&stream.file=$file_abs&stream.contentType=text/plain;charset=utf-8"
	echo "<add>" > $file_abs".idx"
	cat $file | awk -F'\t' '{gsub("&","&amp;");print "<doc><field name=\"id\">"$1"</field><field name=\"raw_catpred\" update=\"set\">"$2"</field><field name=\"store\" update=\"set\">"$3"</field><field name=\"sku\" update=\"set\">"$4"</field></doc>"}' >> $file".idx"
	echo "</add>" >> $file".idx"
	curl 'http://localhost:8983/solr/relevance/update?commit=true' -H "Content-Type: text/xml" --data-binary @$file".idx"
done

