#!/bin/bash

set -e

USAGE="usage: $0 base_directory"
CONF_SOLR_HOSTS='../conf/solrhost.txt'
CONF_COLLECTION='../conf/collection.txt'
SOLR_HOSTS=$(cat $CONF_SOLR_HOSTS | sed '/^\s*$/d')
COLLECTION=$(cat $CONF_COLLECTION | awk 'NR==1{print}')
NUM_SHARDS=$(cat $CONF_COLLECTION | awk 'NR==2{print}')
SOLR_FIELDS=$(cat $CONF_COLLECTION | awk 'NR==4{print}')
BASE_DIR=$1

assert_params() {
	if [ "$1" -lt 1 ]; then echo $USAGE; exit; fi
}

assert_params $#

assert_dir_exists() {
	echo $1 $2
	if [ ! -d "$2" ]; then echo "$1 not found"; exit; fi
}

echo_mkdir_conditional() {
	echo "if [ ! -d $1 ]; then mkdir $1; fi"
}

echo_rmdir_conditional() {
	echo "if [ -d $1 ]; then rm -rf $1; fi"
}

#round robin over solr hosts
num_hosts=$(echo $SOLR_HOSTS |  tr ' ' '\n' | wc -l)
counter=1
get_next_host() {
	host=$(echo $SOLR_HOSTS | tr ' ' '\n' | awk 'NR=='"$counter"'{print}')
	((counter=(counter % $num_hosts)+1))
}


#latest predictions
classifier_dir=$BASE_DIR"/$(ls -1 $BASE_DIR | grep -e "classifier_2[0-9]\{7\}" | sort | tail -1)"
assert_dir_exists "classification directory" $classifier_dir
prediction_files=$(ls -lrt -d -1 $classifier_dir/* | grep -e "full_predictions" | awk '{print $NF}' | sort)
echo "BASE DIRECTORY: $BASE_DIR"
echo "CLASSIFICATION DATA DIRECTORY: $classifier_dir"
echo "PREDICTION FILES: $prediction_files"
echo ""


#iterate over prediction files and index
for file in $prediction_files
do
	filename=$(basename $file)
	prefix=$(IN=$filename; arrIN=(${IN//./ }); echo ${arrIN[1]})
	echo "Indexing $file"

	index_script="index.sh"
	convert_script="convert_solr.sh"
	remote_basedir="~/index"
	remote_split_basedir="$remote_basedir/split_files"
	remote_file="$remote_basedir/$filename"
	remote_split_currdir="$remote_split_basedir/$prefix"
	remote_index_script="$remote_basedir/$index_script"
	remote_convert_script="$remote_basedir/$convert_script"
	log_remote_out="out_$filename"
	log_remote_err="err_$filename"

	get_next_host
	echo $host

	create_basedir_conditional=$(echo_mkdir_conditional $remote_basedir)
	create_split_basedir_conditional=$(echo_mkdir_conditional $remote_split_basedir)
	create_split_currdir_conditional=$(echo_mkdir_conditional $remote_split_currdir)
	cleanup_split_currdir_conditional=$(echo_rmdir_conditional $remote_split_currdir)
	cmd_cleanup_dirs="$cleanup_split_currdir_conditional"
	cmd_create_dirs="$create_basedir_conditional && $create_split_basedir_conditional && $create_split_currdir_conditional"
	cmd_split="split -a 4 -d -l 50000 $remote_file $remote_split_currdir/"
	cmd_convert="$remote_convert_script $remote_split_currdir"
	cmd_index="$remote_index_script $COLLECTION $SOLR_FIELDS $remote_split_currdir"
	
	ssh -oStrictHostKeyChecking=no $host "$cmd_cleanup_dirs && $cmd_create_dirs"
	scp -oStrictHostKeyChecking=no $file $host:$remote_file
	scp -oStrictHostKeyChecking=no $index_script $host:$remote_index_script
	scp -oStrictHostKeyChecking=no $convert_script $host:$remote_convert_script
	ssh -oStrictHostKeyChecking=no $host "chmod +x $remote_index_script $remote_convert_script"
	ssh -oStrictHostKeyChecking=no $host "nohup bash -c '$cmd_split && $cmd_convert && $cmd_index' > $log_remote_out 2> $log_remote_err &"
done

