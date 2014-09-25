Configuration files:
  ../conf/solrhost.txt 
    format: hostname for solr servers, one per line
  ../conf/zkhost.txt
    format: comma-separated list of zookeeperserver:port
  ../conf/collection.txt
    collection name
    
Create a new collection
  1. update above configuration files
  2. run setup.sh
  
Index prediction data from classifier directory
  1. update above configuration files
  2. run start_index.sh <base_dir>
    where base_dir is prediction data base directory (e.g. /ebs1-data/sriram on cam-dev01)
    the script looks for classifier_yyyymmdd file under base directory and indexes all files with name full_prediction*
  3. to stop indexing on all solr servers, run stop_index.sh (looks for and kills process with name index.sh.*split_files)

Create and Index new collection, all in one step
  1. update above configuration files
  2. run all.sh
  
Refresh collection schema
  1. update above configuration files
  2. run refresh.sh
  

  
