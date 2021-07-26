#!/usr/bin/env bash

python task_queue.py > task_queue.log 2>&1 &
sleep 1
python company_node.py > company_node.log 2>&1 &
sleep 1

for i in `seq 10`:
do
python data_node.py $i > data_node${i}.log 2>&1 &
sleep 1
done

sleep 5
python consensus_node.py 6001 > consensus_node1.log 2>&1 &
python consensus_node.py 6002 > consensus_node2.log 2>&1 &
