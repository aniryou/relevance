for i in {2..5}
do
	x=$i
	while [ ${#x} -ne 2 ]; do x="0"$x; done
	echo "Indexing $x"
	ssh solr$x.perf.indix.tv "mkdir index"
	scp cam-dev01.production-mr.indix.tv:/ebs1-data/anil/predictions/amazon/x$x solr$x.perf.indix.tv:/home/ec2-user/index/x$x
	ssh solr$x.perf.indix.tv "rm -rf index/split_files$x && mkdir index/split_files$x"
	ssh solr$x.perf.indix.tv "split -a 4 -d -l 50000 index/x$x index/split_files$x/x$x."
	scp cam-dev01.production-mr.indix.tv:/ebs1-data/anil/predictions/index.sh solr$x.perf.indix.tv:/home/ec2-user/index.sh
	ssh solr$x.perf.indix.tv "chmod +x index.sh"
	ssh solr$x.perf.indix.tv "nohup ./index.sh index/split_files$x > out_$x.txt 2> err_$x.txt &"
done

