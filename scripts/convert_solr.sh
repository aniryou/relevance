#!/bin/bash

set -e

#currently indexs amazon only records, uncomment else part below for other stores
#columns: id,imageurl,product_title,breadcrumb,catpred,ignore1,ignore2,raw_catpred,ignore3,ignore4
for file in `ls $1/*`
do
	indexfile="$file.idx"
	#select and process relevant columns
	cat $file | awk -F'\t' '{
		n=split($5,cat,">");
		$11=cat[1]; #top-cat
		$12=cat[n]; #leaf-cat
		m=split($1,arr1,"/");
		split(arr1[m],arr2,"?");
		$13=arr1[3]; #domain
		$14=arr2[1]; #sku
		if ($13 == "www.amazon.com")
			print $1"\t"$2"\t"$3"\t"$11"\t"$12"\t"$8"\t"$14"\t24";
		#else
		#	print $1"\t"$2"\t"$3"\t"$11"\t"$12"\t"$8"\t\t";
	}' > $indexfile
	rm $file
done
