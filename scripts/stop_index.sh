for i in {1..1}
do
	x=$i
        while [ ${#x} -ne 2 ]; do x="0"$x; done
        echo "Indexing $x"
	ssh solr$x.perf.indix.tv "pid=\$(ps aux | grep 'index_newfields' | awk '{print \$2}' | head -1); echo \$pid |xargs kill"
done
