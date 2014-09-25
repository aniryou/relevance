#!/bin/bash

cat $1 | while read host
do
	ssh $host "pid=\$(ps aux | grep 'index\.sh.*split_files' | awk '{print \$2}' | head -1); echo \$pid |xargs kill"
done
