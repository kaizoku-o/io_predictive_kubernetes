#!/bin/bash
#title           :unit-test-tetris-predictor.sh
#description     :Query tetris-predictor for all three workloads.
#author		 :Vasudev Bongale (vabongal@ncsu.edu)
#date            :2019-04-28
#usage		 :bash unit-test-tetris-predictor.sh
#==============================================================================


echo ""
echo "********* IO *********"
iorequest='{"apiName":"predictWorkload","model":"io","time":60}'
echo "Request:"
echo ${iorequest} | jq .
time curl --silent -d ${iorequest} -H "Content-Type: application/json" -X POST http://172.31.7.88:9580/api | jq .

echo ""
echo "********* CPU *********"
cpurequest='{"apiName":"predictWorkload","model":"cpu","time":60}'
echo "Request:"
echo ${cpurequest} | jq .
time curl --silent -d ${cpurequest} -H "Content-Type: application/json" -X POST http://172.31.7.88:9580/api | jq .

echo ""
echo "********* MEMORY *********"
memrequest='{"apiName":"predictWorkload","model":"mem","time":60}'
echo "Request:"
echo ${memrequest} | jq .
time curl --silent -d ${memrequest} -H "Content-Type: application/json" -X POST http://172.31.7.88:9580/api | jq .
